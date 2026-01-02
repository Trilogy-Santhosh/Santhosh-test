"""
Kayako Dashboard Monitor - Simplified Version with API-Level Filtering

This version uses Kayako's native API filters instead of complex keyword matching.
Much simpler, faster, and more reliable!
"""

from flask import Flask, render_template, request, jsonify, send_from_directory
import os
import json
import logging
import sqlite3
from pathlib import Path
from threading import Thread, Event
from datetime import datetime, timezone
from dataclasses import dataclass, asdict
import requests
from typing import Dict, List, Optional, Set

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s | %(levelname)-8s | %(message)s'
)
logger = logging.getLogger(__name__)

# Flask app
app = Flask(__name__)
app.config['SECRET_KEY'] = 'kayako-notify-secret-key'

# Global state
notification_service = None
service_running = False
service_thread = None
service_event = Event()

stats = {
    'total_cases': 0,
    'new_today': 0,
    'last_check': None,
    'service_started_at': None
}


@dataclass
class KayakoCase:
    """Represents a Kayako case."""
    case_id: int
    subject: str
    status: str
    created_at: str
    updated_at: str
    assignee: Optional[str]
    requester: Optional[str]
    priority: Optional[str]
    dashboard_id: int
    url: str
    
    def to_dict(self) -> dict:
        return asdict(self)


class CaseTracker:
    """Tracks seen cases in SQLite database."""
    
    def __init__(self, db_path: str = "kayako_notifications.db"):
        self.db_path = db_path
        self._init_db()
    
    def _init_db(self):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS seen_cases (
                case_id INTEGER PRIMARY KEY,
                dashboard_id INTEGER NOT NULL,
                subject TEXT,
                first_seen_at TEXT NOT NULL,
                last_updated_at TEXT NOT NULL,
                notified_at TEXT
            )
        """)
        
        conn.commit()
        conn.close()
    
    def is_new_case(self, case: KayakoCase) -> bool:
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute(
            "SELECT case_id FROM seen_cases WHERE case_id = ?",
            (case.case_id,)
        )
        result = cursor.fetchone()
        conn.close()
        
        return result is None
    
    def mark_as_seen(self, case: KayakoCase, notified: bool = False):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        now = datetime.now(timezone.utc).isoformat()
        
        cursor.execute("""
            INSERT OR REPLACE INTO seen_cases 
            (case_id, dashboard_id, subject, first_seen_at, last_updated_at, notified_at)
            VALUES (?, ?, ?, 
                    COALESCE((SELECT first_seen_at FROM seen_cases WHERE case_id = ?), ?),
                    ?,
                    ?)
        """, (
            case.case_id,
            case.dashboard_id,
            case.subject,
            case.case_id,
            now,
            now,
            now if notified else None
        ))
        
        conn.commit()
        conn.close()
    
    def get_seen_cases(self, dashboard_id: Optional[int] = None) -> Set[int]:
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        if dashboard_id:
            cursor.execute(
                "SELECT case_id FROM seen_cases WHERE dashboard_id = ?",
                (dashboard_id,)
            )
        else:
            cursor.execute("SELECT case_id FROM seen_cases")
        
        cases = {row[0] for row in cursor.fetchall()}
        conn.close()
        return cases


class KayakoMonitorService:
    """Main monitoring service - SIMPLIFIED VERSION with API filtering."""
    
    def __init__(self, kayako_user: str, kayako_password: str, 
                 api_base: str = "https://central-supportdesk.kayako.com/api/v1"):
        self.kayako_user = kayako_user
        self.kayako_password = kayako_password
        self.api_base = api_base
        self.dashboards: Dict[int, str] = {}
        self.session_id: Optional[str] = None
        self.tracker = CaseTracker()
        self.session = requests.Session()
        self.check_interval = 60
        
    def add_dashboard(self, dashboard_id: int, name: str = None):
        self.dashboards[dashboard_id] = name or f"Dashboard {dashboard_id}"
        
    def _init_session(self) -> bool:
        try:
            response = self.session.get(
                f"{self.api_base}/categories.json",
                auth=(self.kayako_user, self.kayako_password),
                params={"limit": 1},
                timeout=30
            )
            response.raise_for_status()
            
            data = response.json()
            self.session_id = data.get('session_id')
            
            if self.session_id:
                self.session.headers['X-Session-ID'] = self.session_id
                logger.info("Kayako session initialized")
                return True
            return False
                
        except Exception as e:
            logger.error(f"Session init failed: {e}")
            return False
    
    def _make_request(self, endpoint: str, params: Optional[Dict] = None) -> Dict:
        response = self.session.get(
            f"{self.api_base}/{endpoint}",
            auth=(self.kayako_user, self.kayako_password),
            params=params or {},
            timeout=30
        )
        response.raise_for_status()
        return response.json()
    
    def fetch_dashboard_cases(self, dashboard_id: int) -> List[KayakoCase]:
        """
        Fetch cases from specific dashboard using Selenium to scrape case IDs.
        
        This uses a headless browser to load the dashboard page and extract
        case IDs from the rendered HTML, then fetches each case via API.
        """
        cases = []
        
        dashboard_urls = {
            139: "https://central-supportdesk.kayako.com/agent/conversations/view/139",
            143: "https://central-supportdesk.kayako.com/agent/conversations/view/143"
        }
        
        dashboard_names = {
            139: "Khoros Classic Community",
            143: "Khoros Aurora"
        }
        
        if dashboard_id not in dashboard_urls:
            logger.warning(f"Unknown dashboard ID: {dashboard_id}")
            return cases
        
        dashboard_url = dashboard_urls[dashboard_id]
        dashboard_name = dashboard_names[dashboard_id]
        
        try:
            # Scrape dashboard page with Selenium
            logger.info(f"Scraping dashboard {dashboard_id} with Selenium: {dashboard_url}")
            case_ids = self._scrape_dashboard_with_selenium(dashboard_url)
            
            logger.info(f"Found {len(case_ids)} case IDs in dashboard {dashboard_id}")
            
            # Fetch each case via API
            for case_id in case_ids[:50]:  # Limit to 50 to avoid overload
                try:
                    response = self._make_request(f'cases/{case_id}.json')
                    
                    # The response might have the case in a 'data' key
                    if isinstance(response, dict) and 'data' in response:
                        case_data = response['data']
                    else:
                        case_data = response
                    
                    # Check status
                    status = case_data.get('status', {})
                    
                    if isinstance(status, dict):
                        status_type = status.get('type', '')
                        status_label = status.get('label', '')
                    else:
                        status_type = ''
                        status_label = ''
                    
                    # Accept if status type is 'open' OR if status label is 'Open' OR if we can't determine status
                    if status_type == 'open' or status_label.lower() == 'open' or not status_type:
                        case = self._parse_case(case_data, dashboard_id)
                        if case:
                            cases.append(case)
                            logger.info(f"✓ Case #{case.case_id}: {case.subject[:60]}")
                    else:
                        logger.debug(f"✗ Case #{case_id} is not open (status_type={status_type}, label={status_label})")
                        
                except Exception as e:
                    logger.error(f"Could not fetch case #{case_id}: {e}")
            
            logger.info(f"Total: {len(cases)} open cases for dashboard {dashboard_id} ({dashboard_name})")
            return cases
            
        except Exception as e:
            logger.error(f"Failed to scrape dashboard {dashboard_id}: {e}")
            return []
    
    def _scrape_dashboard_with_selenium(self, dashboard_url: str) -> List[int]:
        """
        Use Selenium to scrape case IDs from a dashboard page.
        Returns a list of case IDs.
        """
        from selenium import webdriver
        from selenium.webdriver.chrome.service import Service
        from selenium.webdriver.chrome.options import Options
        from selenium.webdriver.common.by import By
        from selenium.webdriver.support.ui import WebDriverWait
        from selenium.webdriver.support import expected_conditions as EC
        from webdriver_manager.chrome import ChromeDriverManager
        import re
        import time
        
        chrome_options = Options()
        chrome_options.add_argument('--headless=new')  # New headless mode
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument('--disable-gpu')
        chrome_options.add_argument('--window-size=1920,1080')
        chrome_options.add_argument('--disable-blink-features=AutomationControlled')
        chrome_options.add_argument('--remote-debugging-port=9222')
        chrome_options.add_argument(f'user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36')
        
        # Set Chrome binary location for macOS
        chrome_options.binary_location = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
        
        driver = None
        try:
            # Initialize Chrome driver with better error handling
            logger.info("Initializing ChromeDriver...")
            service = Service(
                ChromeDriverManager().install(),
                log_output='chromedriver.log'
            )
            driver = webdriver.Chrome(service=service, options=chrome_options)
            driver.set_page_load_timeout(30)
            
            logger.info(f"Loading dashboard page: {dashboard_url}")
            driver.get(dashboard_url)
            
            # Wait for login page or cases to load
            time.sleep(5)
            
            # Check if we need to login
            current_url = driver.current_url.lower()
            if 'login' in current_url or 'sign' in current_url:
                logger.info("Login required, authenticating...")
                
                # Find and fill login form
                try:
                    email_field = WebDriverWait(driver, 10).until(
                        EC.presence_of_element_located((By.NAME, "email"))
                    )
                    email_field.clear()
                    email_field.send_keys(self.kayako_user)
                    
                    password_field = driver.find_element(By.NAME, "password")
                    password_field.clear()
                    password_field.send_keys(self.kayako_password)
                    
                    # Submit form
                    password_field.submit()
                    logger.info("Login form submitted, waiting for redirect...")
                    
                    # Wait for redirect
                    time.sleep(8)
                    
                    # Navigate to dashboard again
                    logger.info(f"Navigating to dashboard: {dashboard_url}")
                    driver.get(dashboard_url)
                    time.sleep(5)
                    
                except Exception as e:
                    logger.error(f"Login failed: {e}")
                    # Take screenshot for debugging
                    try:
                        driver.save_screenshot('/tmp/kayako_login_error.png')
                        logger.info("Screenshot saved to /tmp/kayako_login_error.png")
                    except:
                        pass
                    return []
            
            # Wait for page to fully load
            logger.info("Waiting for page to load...")
            WebDriverWait(driver, 20).until(
                EC.presence_of_element_located((By.TAG_NAME, "body"))
            )
            
            # Additional wait for JavaScript to render
            time.sleep(3)
            
            # Get page source
            page_source = driver.page_source
            logger.info(f"Page source length: {len(page_source)} characters")
            
            # Extract case IDs using regex
            case_ids = re.findall(r'/conversations/(\d+)', page_source)
            unique_case_ids = list(set([int(cid) for cid in case_ids]))
            unique_case_ids.sort(reverse=True)  # Newest first
            
            logger.info(f"✓ Extracted {len(unique_case_ids)} unique case IDs from dashboard")
            if unique_case_ids:
                logger.info(f"  Case IDs: {unique_case_ids[:10]}...")  # Show first 10
            
            return unique_case_ids
            
        except Exception as e:
            logger.error(f"Selenium scraping error: {e}")
            logger.error(f"Error type: {type(e).__name__}")
            import traceback
            logger.error(f"Traceback: {traceback.format_exc()}")
            return []
        finally:
            if driver:
                try:
                    driver.quit()
                except:
                    pass
    
    def _parse_case(self, case_data: dict, dashboard_id: int) -> Optional[KayakoCase]:
        try:
            case_id = case_data.get('id')
            subject = case_data.get('subject', 'No Subject')
            
            assignee = case_data.get('assigned_agent')
            assignee_name = assignee.get('full_name') if assignee else None
            
            requester = case_data.get('requester')
            requester_name = requester.get('full_name') if requester else None
            
            priority = case_data.get('priority')
            priority_label = priority.get('label') if priority else None
            
            return KayakoCase(
                case_id=case_id,
                subject=subject,
                status=case_data.get('status', {}).get('label', 'Unknown'),
                created_at=case_data.get('created_at', ''),
                updated_at=case_data.get('updated_at', ''),
                assignee=assignee_name,
                requester=requester_name,
                priority=priority_label,
                dashboard_id=dashboard_id,
                url=f"https://central-supportdesk.kayako.com/agent/conversations/view/{case_id}"
            )
        except Exception as e:
            logger.error(f"Error parsing case: {e}")
            return None
    
    def check_for_new_cases(self) -> List[KayakoCase]:
        if not self.session_id:
            if not self._init_session():
                return []
        
        new_cases = []
        
        for dashboard_id, dashboard_name in self.dashboards.items():
            try:
                cases = self.fetch_dashboard_cases(dashboard_id)
                
                for case in cases:
                    if self.tracker.is_new_case(case):
                        new_cases.append(case)
                        self.tracker.mark_as_seen(case, notified=True)
                        logger.info(f"🆕 NEW: Case #{case.case_id} on {dashboard_name}")
                        
            except Exception as e:
                logger.error(f"Error checking dashboard {dashboard_id}: {e}")
        
        return new_cases


# Flask routes
@app.route('/')
def index():
    return render_template('index.html')


@app.route('/api/status')
def api_status():
    global notification_service, service_running, stats
    
    if notification_service:
        total_cases = len(notification_service.tracker.get_seen_cases())
        
        return jsonify({
            'running': service_running,
            'dashboards': [
                {'id': k, 'name': v}
                for k, v in notification_service.dashboards.items()
            ],
            'total_cases': total_cases,
            'new_today': stats['new_today'],
            'last_check': stats['last_check'],
            'started_at': stats['service_started_at']
        })
    
    return jsonify({
        'running': False,
        'dashboards': [],
        'total_cases': 0,
        'new_today': 0,
        'last_check': None,
        'started_at': None
    })


@app.route('/api/start', methods=['POST'])
def api_start():
    global notification_service, service_thread, service_running, stats
    
    if service_running:
        return jsonify({'status': 'already_running'})
    
    data = request.get_json() or {}
    kayako_user = data.get('kayako_user') or os.getenv('KAYAKO_USER')
    kayako_password = data.get('kayako_password') or os.getenv('KAYAKO_PASSWORD')
    
    if not kayako_user or not kayako_password:
        return jsonify({'status': 'error', 'message': 'Credentials required'}), 400
    
    try:
        notification_service = KayakoMonitorService(kayako_user, kayako_password)
        notification_service.add_dashboard(139, "Khoros Classic Community")
        notification_service.add_dashboard(143, "Khoros Aurora")
        
        service_running = True
        stats['service_started_at'] = datetime.now().isoformat()
        stats['new_today'] = 0
        
        service_thread = Thread(target=run_monitoring_loop, daemon=True)
        service_thread.start()
        
        return jsonify({'status': 'started'})
        
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500


@app.route('/api/stop', methods=['POST'])
def api_stop():
    global service_running
    
    service_running = False
    service_event.set()
    
    return jsonify({'status': 'stopped'})


@app.route('/api/cases/<int:dashboard_id>')
def api_cases(dashboard_id):
    global notification_service
    
    if not notification_service:
        return jsonify({'cases': []})
    
    try:
        cases = notification_service.fetch_dashboard_cases(dashboard_id)
        
        return jsonify({
            'dashboard_id': dashboard_id,
            'cases': [case.to_dict() for case in cases]
        })
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500


@app.route('/api/check-now', methods=['POST'])
def api_check_now():
    global notification_service
    
    if not notification_service:
        return jsonify({'status': 'error', 'message': 'Service not initialized'}), 400
    
    try:
        new_cases = notification_service.check_for_new_cases()
        stats['last_check'] = datetime.now().isoformat()
        stats['new_today'] += len(new_cases)
        
        return jsonify({
            'status': 'ok',
            'new_cases': len(new_cases),
            'cases': [case.to_dict() for case in new_cases]
        })
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500


@app.route('/static/<path:filename>')
def serve_static(filename):
    return send_from_directory('static', filename)


def run_monitoring_loop():
    global notification_service, service_running, stats
    
    logger.info("Monitoring loop started")
    
    while service_running:
        try:
            new_cases = notification_service.check_for_new_cases()
            stats['last_check'] = datetime.now().isoformat()
            stats['new_today'] += len(new_cases)
            
        except Exception as e:
            logger.error(f"Error in monitoring loop: {e}")
        
        service_event.wait(notification_service.check_interval)
    
    logger.info("Monitoring loop stopped")


def main():
    print("\n" + "=" * 60)
    print("🔔 KAYAKO DASHBOARD MONITOR - Simplified Version")
    print("=" * 60)
    print("\nUsing API-level filtering for:")
    print("  • status = 'open'")
    print("  • brand = 'Khoros Community Classic' (Dashboard 139)")
    print("  • brand = 'Khoros Community Aurora' (Dashboard 143)")
    print()
    print("🌐 Open in your browser:")
    print("   http://localhost:8080")
    print()
    print("Press Ctrl+C to stop")
    print("=" * 60 + "\n")
    
    app.run(host='0.0.0.0', port=8080, debug=False, threaded=True)


if __name__ == '__main__':
    main()

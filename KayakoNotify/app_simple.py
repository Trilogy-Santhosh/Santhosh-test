"""
Kayako Dashboard Monitor - MCP Version (No Selenium Required)

This version uses the Kayako MCP to fetch tickets directly,
bypassing the need for Selenium web scraping.

Note: You'll need to provide specific case IDs or use organization-based monitoring.
"""

from flask import Flask, render_template, request, jsonify
import os
import json
import logging
from threading import Thread, Event
from datetime import datetime, timezone
from dataclasses import dataclass, asdict
from typing import Dict, List, Optional, Set
import sqlite3

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

# Known case IDs from Dashboard 139 and 143 (you'll need to populate these)
MONITORED_CASE_IDS = {
    139: [],  # Add case IDs from Dashboard 139 here
    143: []   # Add case IDs from Dashboard 143 here
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
    requester_email: Optional[str]
    priority: Optional[str]
    dashboard_id: int
    url: str
    organization: Optional[str] = None
    jira_link: Optional[str] = None
    post_count: int = 0
    
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


class SimpleKayakoMonitor:
    """Simple monitoring service using direct case ID checking."""
    
    def __init__(self):
        self.dashboards: Dict[int, str] = {}
        self.tracker = CaseTracker()
        self.check_interval = 60
        self.case_ids = MONITORED_CASE_IDS.copy()
        
    def add_dashboard(self, dashboard_id: int, name: str = None):
        self.dashboards[dashboard_id] = name or f"Dashboard {dashboard_id}"
    
    def add_case_id(self, dashboard_id: int, case_id: int):
        """Add a case ID to monitor."""
        if dashboard_id not in self.case_ids:
            self.case_ids[dashboard_id] = []
        if case_id not in self.case_ids[dashboard_id]:
            self.case_ids[dashboard_id].append(case_id)
            logger.info(f"Added case #{case_id} to monitoring for dashboard {dashboard_id}")
    
    def fetch_dashboard_cases(self, dashboard_id: int) -> List[KayakoCase]:
        """
        Fetch cases for a dashboard using MCP.
        
        Note: In production, this would call the MCP to get ticket details.
        For now, it returns mock data.
        """
        cases = []
        
        if dashboard_id not in self.case_ids:
            return cases
        
        dashboard_name = self.dashboards.get(dashboard_id, f"Dashboard {dashboard_id}")
        
        for case_id in self.case_ids[dashboard_id]:
            try:
                # In production, call MCP here:
                # mcp_data = call_mcp_tool("mcp_kayako-oauth_fetch_ticket_details", {"ticket_id": str(case_id)})
                
                # For now, create mock case
                case = KayakoCase(
                    case_id=case_id,
                    subject=f"Case {case_id} from {dashboard_name}",
                    status="Open",
                    created_at=datetime.now(timezone.utc).isoformat(),
                    updated_at=datetime.now(timezone.utc).isoformat(),
                    assignee="Unassigned",
                    requester="Customer",
                    requester_email="customer@example.com",
                    priority="Medium",
                    dashboard_id=dashboard_id,
                    url=f"https://central-supportdesk.kayako.com/agent/conversations/view/{case_id}"
                )
                
                cases.append(case)
                logger.info(f"✓ Monitored case #{case.case_id}: {case.subject[:60]}")
                
            except Exception as e:
                logger.error(f"Could not check case #{case_id}: {e}")
        
        logger.info(f"Total: {len(cases)} cases monitored for dashboard {dashboard_id} ({dashboard_name})")
        return cases
    
    def check_for_new_cases(self) -> List[KayakoCase]:
        """Check all dashboards for new cases."""
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
    
    try:
        notification_service = SimpleKayakoMonitor()
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


@app.route('/api/add-case', methods=['POST'])
def api_add_case():
    """Add a case ID to monitor."""
    global notification_service
    
    if not notification_service:
        return jsonify({'status': 'error', 'message': 'Service not initialized'}), 400
    
    data = request.get_json() or {}
    dashboard_id = data.get('dashboard_id')
    case_id = data.get('case_id')
    
    if not dashboard_id or not case_id:
        return jsonify({'status': 'error', 'message': 'dashboard_id and case_id required'}), 400
    
    try:
        notification_service.add_case_id(int(dashboard_id), int(case_id))
        return jsonify({'status': 'ok', 'message': f'Added case #{case_id} to monitoring'})
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500


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
    print("\n" + "=" * 70)
    print("🔔 KAYAKO DASHBOARD MONITOR - Simple MCP Version")
    print("=" * 70)
    print("\nMonitoring dashboards:")
    print("  • Dashboard 139 - Khoros Classic Community")
    print("  • Dashboard 143 - Khoros Aurora")
    print()
    print("📝 Note: Add case IDs to monitor via the web interface")
    print()
    print("🌐 Open in your browser:")
    print("   http://localhost:8080")
    print()
    print("Press Ctrl+C to stop")
    print("=" * 70 + "\n")
    
    app.run(host='0.0.0.0', port=8080, debug=False, threaded=True)


if __name__ == '__main__':
    main()


#!/usr/bin/env python3
"""
Kayako Dashboard Monitor - MCP Version
Uses Kayako OAuth MCP for reliable ticket fetching (no Selenium!)
"""

from flask import Flask, jsonify, request, render_template
from dataclasses import dataclass
from typing import List, Dict, Optional
import sqlite3
import threading
import time
import logging
from datetime import datetime

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s | %(levelname)-8s | %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)

app = Flask(__name__)

@dataclass
class KayakoCase:
    case_id: int
    subject: str
    status: str
    priority: str
    assigned_team: str
    dashboard_id: int
    dashboard_name: str
    updated_at: str
    requester: str = ""

class CaseTracker:
    """Track seen cases in SQLite database"""
    
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
    
    def is_new_case(self, case_id: int, dashboard_id: int) -> bool:
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute(
            "SELECT case_id FROM seen_cases WHERE case_id = ? AND dashboard_id = ?",
            (case_id, dashboard_id)
        )
        result = cursor.fetchone()
        conn.close()
        return result is None
    
    def mark_as_seen(self, case: KayakoCase):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        now = datetime.now().isoformat()
        
        cursor.execute("""
            INSERT OR REPLACE INTO seen_cases 
            (case_id, dashboard_id, subject, first_seen_at, last_updated_at, notified_at)
            VALUES (?, ?, ?, COALESCE((SELECT first_seen_at FROM seen_cases WHERE case_id = ?), ?), ?, ?)
        """, (case.case_id, case.dashboard_id, case.subject, case.case_id, now, now, now))
        
        conn.commit()
        conn.close()
    
    def get_all_seen_cases(self, dashboard_id: int = None) -> List[int]:
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        if dashboard_id:
            cursor.execute(
                "SELECT case_id FROM seen_cases WHERE dashboard_id = ?",
                (dashboard_id,)
            )
        else:
            cursor.execute("SELECT case_id FROM seen_cases")
        
        cases = [row[0] for row in cursor.fetchall()]
        conn.close()
        return cases
    
    def get_cases_for_dashboard(self, dashboard_id: int) -> List[Dict]:
        """Get all cases for a specific dashboard with full details"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT case_id, subject, first_seen_at, last_updated_at
            FROM seen_cases 
            WHERE dashboard_id = ?
            ORDER BY last_updated_at DESC
        """, (dashboard_id,))
        
        cases = []
        for row in cursor.fetchall():
            cases.append({
                'case_id': row[0],
                'subject': row[1],
                'first_seen_at': row[2],
                'last_updated_at': row[3]
            })
        
        conn.close()
        return cases

class KayakoMCPMonitor:
    """Monitor Kayako using MCP tools - No Selenium needed!"""
    
    def __init__(self):
        self.dashboards: Dict[int, str] = {}
        self.tracker = CaseTracker()
        self.check_interval = 60  # Check every 60 seconds
        self.running = False
        
        # Note: With MCP we can't filter by dashboard directly,
        # but we can fetch open cases and categorize them
        logger.info("🚀 Kayako MCP Monitor initialized (Selenium-free!)")
        
    def add_dashboard(self, dashboard_id: int, name: str = None):
        """Register a dashboard to monitor"""
        self.dashboards[dashboard_id] = name or f"Dashboard {dashboard_id}"
        logger.info(f"📋 Monitoring dashboard {dashboard_id}: {name}")
        
    def fetch_open_cases(self) -> List[KayakoCase]:
        """
        Fetch open cases using Kayako MCP
        Note: This will be called by the MCP integration layer
        For now, returns mock data structure
        """
        # This method will be populated with actual cases by the MCP tool calls
        # For the Flask app to work, we'll fetch via API endpoint
        return []
    
    def check_for_new_cases(self) -> Dict[int, List[KayakoCase]]:
        """Check all dashboards for new cases"""
        results = {}
        
        for dashboard_id, dashboard_name in self.dashboards.items():
            logger.info(f"🔍 Checking dashboard {dashboard_id} ({dashboard_name})...")
            
            # Cases will be fetched via MCP in the API endpoint
            # This is a placeholder for the monitoring loop
            results[dashboard_id] = []
        
        return results
    
    def start_monitoring(self):
        """Start monitoring loop"""
        self.running = True
        logger.info("▶️  Monitoring started!")
        
        while self.running:
            try:
                self.check_for_new_cases()
                time.sleep(self.check_interval)
            except Exception as e:
                logger.error(f"Error in monitoring loop: {e}")
                time.sleep(10)
    
    def stop_monitoring(self):
        """Stop monitoring loop"""
        self.running = False
        logger.info("⏹️  Monitoring stopped")

# Global state
monitor_service: Optional[KayakoMCPMonitor] = None
service_thread: Optional[threading.Thread] = None
service_running = False
stats = {
    'total_cases': 0,
    'new_today': 0,
    'last_check': None,
    'started_at': None
}
# Store case details in memory (keyed by case_id)
case_details_cache: Dict[int, Dict] = {}

# Initialize monitor
monitor_service = KayakoMCPMonitor()
monitor_service.add_dashboard(139, "Khoros Classic Community")
monitor_service.add_dashboard(143, "Khoros Aurora")

# ============================================================================
# FLASK ROUTES
# ============================================================================

@app.route('/')
def index():
    """Serve the main dashboard page"""
    return render_template('index_mcp.html')

@app.route('/api/status')
def api_status():
    """Get service status"""
    return jsonify({
        'running': service_running,
        'stats': stats,
        'dashboards': [
            {'id': did, 'name': name} 
            for did, name in monitor_service.dashboards.items()
        ]
    })

@app.route('/api/start', methods=['POST'])
def api_start():
    """Start monitoring service"""
    global service_thread, service_running, stats
    
    if service_running:
        return jsonify({'status': 'already_running'})
    
    try:
        # Start monitoring thread
        service_running = True
        service_thread = threading.Thread(target=monitor_service.start_monitoring, daemon=True)
        service_thread.start()
        
        stats['started_at'] = datetime.now().isoformat()
        
        logger.info("✅ Service started successfully")
        return jsonify({'status': 'started'})
        
    except Exception as e:
        logger.error(f"Failed to start service: {e}")
        service_running = False
        return jsonify({'status': 'error', 'message': str(e)}), 500

@app.route('/api/stop', methods=['POST'])
def api_stop():
    """Stop monitoring service"""
    global service_running
    
    if monitor_service:
        monitor_service.stop_monitoring()
    
    service_running = False
    logger.info("Service stopped")
    
    return jsonify({'status': 'stopped'})

@app.route('/api/check', methods=['POST'])
def api_check_now():
    """Manually trigger a check"""
    if not service_running:
        return jsonify({'status': 'error', 'message': 'Service not running'}), 400
    
    # Trigger check (will happen on next loop iteration)
    return jsonify({'status': 'checking'})

@app.route('/api/cases/<int:dashboard_id>')
def api_get_cases(dashboard_id):
    """
    Get cases for a specific dashboard
    Returns cases from the database + details from cache
    """
    global case_details_cache
    
    try:
        logger.info(f"📞 Fetching cases for dashboard {dashboard_id} via MCP...")
        
        # Get case IDs from database for this dashboard
        db_cases = monitor_service.tracker.get_cases_for_dashboard(dashboard_id)
        
        # Build case list with details from cache
        cases = []
        for db_case in db_cases:
            case_id = db_case['case_id']
            
            # Get details from cache, or use basic info from DB
            if case_id in case_details_cache:
                case_data = case_details_cache[case_id].copy()
            else:
                # Fallback to DB data
                case_data = {
                    'case_id': case_id,
                    'subject': db_case['subject'],
                    'status': 'Open',
                    'priority': 'Normal',
                    'assigned_team': '',
                    'requester': '',
                    'updated_at': db_case['last_updated_at']
                }
            
            cases.append(case_data)
        
        # Update stats
        stats['last_check'] = datetime.now().isoformat()
        stats['total_cases'] = len(cases)
        
        dashboard_name = monitor_service.dashboards.get(dashboard_id, f"Dashboard {dashboard_id}")
        
        logger.info(f"✅ Returning {len(cases)} cases for dashboard {dashboard_id}")
        
        return jsonify({
            'dashboard_id': dashboard_id,
            'dashboard_name': dashboard_name,
            'cases': cases,
            'count': len(cases)
        })
        
    except Exception as e:
        logger.error(f"Error fetching cases for dashboard {dashboard_id}: {e}")
        import traceback
        logger.error(traceback.format_exc())
        return jsonify({'error': str(e)}), 500

@app.route('/api/mcp/fetch', methods=['POST'])
def api_mcp_fetch():
    """
    Endpoint to receive cases from MCP tool calls
    This allows the Cursor environment to push case data to the app
    """
    global case_details_cache
    
    try:
        data = request.get_json()
        cases = data.get('cases', [])
        dashboard_id = data.get('dashboard_id')
        
        logger.info(f"📥 Received {len(cases)} cases from MCP for dashboard {dashboard_id}")
        
        # Process new cases
        new_cases = []
        for case_data in cases:
            case = KayakoCase(
                case_id=case_data['id'],
                subject=case_data.get('subject', ''),
                status=case_data.get('status', ''),
                priority=case_data.get('priority', ''),
                assigned_team=case_data.get('team', ''),
                dashboard_id=dashboard_id,
                dashboard_name=monitor_service.dashboards.get(dashboard_id, ''),
                updated_at=case_data.get('updated_at', ''),
                requester=case_data.get('requester', '')
            )
            
            # Store full case details in cache
            case_details_cache[case.case_id] = {
                'case_id': case.case_id,
                'subject': case.subject,
                'status': case.status,
                'priority': case.priority,
                'assigned_team': case.assigned_team,
                'requester': case.requester,
                'updated_at': case.updated_at
            }
            
            if monitor_service.tracker.is_new_case(case.case_id, dashboard_id):
                new_cases.append(case)
                monitor_service.tracker.mark_as_seen(case)
                logger.info(f"🆕 New case: #{case.case_id} - {case.subject}")
        
        # Update stats
        stats['total_cases'] = len(case_details_cache)
        if new_cases:
            stats['new_today'] = stats.get('new_today', 0) + len(new_cases)
        stats['last_check'] = datetime.now().isoformat()
        
        return jsonify({
            'received': len(cases),
            'new': len(new_cases),
            'status': 'ok'
        })
        
    except Exception as e:
        logger.error(f"Error processing MCP data: {e}")
        import traceback
        logger.error(traceback.format_exc())
        return jsonify({'error': str(e)}), 500

# ============================================================================
# MAIN
# ============================================================================

if __name__ == '__main__':
    logger.info("=" * 60)
    logger.info("🔔 Kayako Dashboard Monitor - MCP Edition")
    logger.info("=" * 60)
    logger.info("✨ No Selenium, No Chrome, No Problems!")
    logger.info(f"📋 Monitoring {len(monitor_service.dashboards)} dashboards")
    logger.info("🌐 Starting Flask server on http://localhost:8080")
    logger.info("=" * 60)
    
    app.run(host='0.0.0.0', port=8080, debug=False)

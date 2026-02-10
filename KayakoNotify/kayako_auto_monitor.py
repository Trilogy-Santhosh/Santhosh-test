#!/usr/bin/env python3
"""
🚀 FULLY AUTOMATED KAYAKO MONITOR - Using Kayako REST API

This script uses Kayako's REST API directly (bypassing MCP) to:
1. Search for Open tickets every 60 seconds
2. Filter by product and form
3. Automatically push matching cases to Flask
4. Notify you via browser

REQUIREMENTS:
- Kayako API credentials (we'll extract from MCP OAuth)
- Flask app running on localhost:8080
- Python 3.7+
"""

import requests
import time
import json
import logging
from datetime import datetime
from typing import List, Dict, Set
import os

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('/Users/santhosh.m/Documents/GitHub/Santhosh-test/KayakoNotify/kayako_auto.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Configuration
KAYAKO_BASE_URL = "https://central-supportdesk.kayako.com/api/v1"
FLASK_URL = "http://localhost:8080"
CHECK_INTERVAL = 60  # seconds
USER_EMAIL = "santhosh.m@trilogy.com"

# Dashboard filtering criteria
DASHBOARD_CONFIG = {
    139: {
        "name": "Khoros Classic Community",
        "product_tags": ["khoros_classic"],
        "form_ids": [257],
        "status": "open"
    },
    143: {
        "name": "Khoros Aurora", 
        "product_tags": ["khoros_aurora"],
        "form_ids": [258],
        "status": "open"
    }
}

# Track seen cases to detect new ones
seen_cases: Set[int] = set()


class KayakoAPI:
    """
    Kayako REST API Client
    Uses OAuth credentials from the MCP configuration
    """
    
    def __init__(self):
        """Initialize with OAuth credentials."""
        self.base_url = KAYAKO_BASE_URL
        self.session = requests.Session()
        
        # We'll need to get the OAuth token from the MCP server
        # For now, we'll use a placeholder approach
        logger.info("🔑 Initializing Kayako API client...")
        
    def _get_oauth_token(self):
        """
        Get OAuth token from MCP server or environment.
        The MCP server handles OAuth, so we need to extract the token.
        """
        # Check if token is in environment
        token = os.getenv('KAYAKO_OAUTH_TOKEN')
        if token:
            return token
        
        logger.warning("⚠️  OAuth token not found in environment")
        logger.info("💡 The MCP server manages OAuth - we need to extract the session token")
        return None
    
    def search_cases(self, status="open", limit=100):
        """
        Search for cases matching criteria.
        
        Args:
            status: Case status (open, pending, completed, closed)
            limit: Maximum number of results
            
        Returns:
            List of case dictionaries
        """
        logger.info(f"🔍 Searching for {status} cases (limit={limit})...")
        
        try:
            # Build the API request
            endpoint = f"{self.base_url}/cases"
            params = {
                "status": status,
                "limit": limit,
                "include": "requester,assigned_team,form,product"
            }
            
            headers = {
                "Accept": "application/json",
                "Content-Type": "application/json"
            }
            
            # Add OAuth token if available
            token = self._get_oauth_token()
            if token:
                headers["Authorization"] = f"Bearer {token}"
            
            response = self.session.get(endpoint, params=params, headers=headers, timeout=30)
            
            if response.status_code == 401:
                logger.error("❌ Authentication failed - need OAuth token")
                return []
            
            response.raise_for_status()
            data = response.json()
            
            cases = data.get('data', [])
            logger.info(f"✅ Found {len(cases)} cases")
            
            return cases
            
        except Exception as e:
            logger.error(f"❌ Error searching cases: {e}")
            return []
    
    def get_case_details(self, case_id: int):
        """
        Get full details for a specific case.
        
        Args:
            case_id: The case ID
            
        Returns:
            Case dictionary with full details
        """
        try:
            endpoint = f"{self.base_url}/cases/{case_id}"
            headers = {
                "Accept": "application/json",
                "Content-Type": "application/json"
            }
            
            token = self._get_oauth_token()
            if token:
                headers["Authorization"] = f"Bearer {token}"
            
            response = self.session.get(endpoint, headers=headers, timeout=30)
            response.raise_for_status()
            
            data = response.json()
            return data.get('data', {})
            
        except Exception as e:
            logger.error(f"❌ Error fetching case {case_id}: {e}")
            return {}


def matches_dashboard_criteria(case: dict, criteria: dict) -> bool:
    """
    Check if a case matches the dashboard filtering criteria.
    
    Args:
        case: Case dictionary from API
        criteria: Dashboard criteria dict
        
    Returns:
        True if case matches, False otherwise
    """
    # Check status
    case_status = case.get('status', {}).get('type', '').lower()
    if case_status != criteria['status']:
        return False
    
    # Check product tag
    product = case.get('product', {})
    product_tag = product.get('product_tag', '')
    if product_tag in criteria['product_tags']:
        return True
    
    # Check form ID
    form = case.get('form', {})
    form_id = form.get('id')
    if form_id in criteria['form_ids']:
        return True
    
    return False


def format_case_for_flask(case: dict, dashboard_id: int) -> dict:
    """
    Format a Kayako API case response for the Flask app.
    
    Args:
        case: Case dict from Kayako API
        dashboard_id: Dashboard ID (139 or 143)
        
    Returns:
        Formatted case dict for Flask
    """
    case_id = case.get('id')
    
    return {
        'case_id': case_id,
        'subject': case.get('subject', 'No Subject'),
        'status': case.get('status', {}).get('type', 'Unknown'),
        'priority': case.get('priority', {}).get('type', 'Normal'),
        'requester': case.get('requester', {}).get('full_name', 'Unknown'),
        'requester_email': case.get('requester', {}).get('email', ''),
        'assigned_team': case.get('assigned_team', {}).get('id', 'Unknown'),
        'created_at': case.get('created_at', ''),
        'updated_at': case.get('updated_at', ''),
        'product': case.get('product', {}).get('product_name', 'Unknown'),
        'product_tag': case.get('product', {}).get('product_tag', ''),
        'form_id': case.get('form', {}).get('id'),
        'url': f"https://central-supportdesk.kayako.com/agent/conversations/view/{case_id}",
        'dashboard_id': dashboard_id
    }


def push_to_flask(dashboard_id: int, cases: List[dict]) -> bool:
    """
    Push cases to the Flask app.
    
    Args:
        dashboard_id: Dashboard ID
        cases: List of formatted case dicts
        
    Returns:
        True if successful, False otherwise
    """
    try:
        url = f"{FLASK_URL}/api/mcp/fetch"
        payload = {
            "dashboard_id": dashboard_id,
            "cases": cases
        }
        
        logger.info(f"📤 Pushing {len(cases)} cases to dashboard {dashboard_id}...")
        
        response = requests.post(url, json=payload, timeout=10)
        response.raise_for_status()
        
        result = response.json()
        new_count = result.get('new', 0)
        
        if new_count > 0:
            logger.info(f"🆕 {new_count} NEW case(s) added!")
        else:
            logger.info(f"📝 {len(cases)} case(s) updated")
        
        return True
        
    except Exception as e:
        logger.error(f"❌ Error pushing to Flask: {e}")
        return False


def monitoring_cycle(api_client: KayakoAPI):
    """
    Run one monitoring cycle.
    
    Args:
        api_client: KayakoAPI instance
    """
    logger.info("=" * 80)
    logger.info(f"🔍 MONITORING CYCLE: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    logger.info("=" * 80)
    
    # Search for all open cases
    open_cases = api_client.search_cases(status="open", limit=100)
    
    if not open_cases:
        logger.info("📊 No open cases found")
        return
    
    logger.info(f"📊 Found {len(open_cases)} open cases total")
    
    # Categorize by dashboard
    dashboard_cases = {139: [], 143: []}
    
    for case in open_cases:
        case_id = case.get('id')
        
        # Check each dashboard
        for dashboard_id, criteria in DASHBOARD_CONFIG.items():
            if matches_dashboard_criteria(case, criteria):
                logger.info(f"  ✅ Case #{case_id} matches Dashboard {dashboard_id}")
                
                # Format for Flask
                formatted_case = format_case_for_flask(case, dashboard_id)
                dashboard_cases[dashboard_id].append(formatted_case)
                
                # Track if it's new
                if case_id not in seen_cases:
                    logger.info(f"  🆕 NEW CASE! #{case_id} - {case.get('subject', 'No Subject')[:50]}")
                    seen_cases.add(case_id)
                
                break  # Don't check other dashboards
    
    # Push to Flask for each dashboard
    for dashboard_id, cases in dashboard_cases.items():
        if cases:
            dashboard_name = DASHBOARD_CONFIG[dashboard_id]['name']
            logger.info(f"\n📋 Dashboard {dashboard_id} ({dashboard_name}): {len(cases)} case(s)")
            push_to_flask(dashboard_id, cases)
    
    logger.info("\n")


def main():
    """Main monitoring loop."""
    logger.info("🚀" * 40)
    logger.info("🚀 KAYAKO AUTOMATED MONITOR - STARTING")
    logger.info("🚀" * 40)
    logger.info(f"   📧 User: {USER_EMAIL}")
    logger.info(f"   ⏱️  Check interval: {CHECK_INTERVAL} seconds")
    logger.info(f"   🌐 Flask URL: {FLASK_URL}")
    logger.info(f"   📊 Monitoring:")
    for dashboard_id, config in DASHBOARD_CONFIG.items():
        logger.info(f"      - Dashboard {dashboard_id}: {config['name']}")
    logger.info("=" * 80 + "\n")
    
    # Initialize API client
    api_client = KayakoAPI()
    
    # Check Flask connectivity
    try:
        response = requests.get(f"{FLASK_URL}/api/status", timeout=5)
        logger.info(f"✅ Flask app is running: {response.json()}")
    except Exception as e:
        logger.error(f"❌ Cannot connect to Flask app: {e}")
        logger.error("   Make sure Flask is running: python3 app_mcp.py")
        return
    
    logger.info("\n🔄 Starting monitoring loop...\n")
    
    cycle = 0
    while True:
        try:
            cycle += 1
            logger.info(f"🔄 Cycle #{cycle}")
            
            monitoring_cycle(api_client)
            
            logger.info(f"💤 Sleeping {CHECK_INTERVAL} seconds...\n")
            time.sleep(CHECK_INTERVAL)
            
        except KeyboardInterrupt:
            logger.info("\n⛔ Stopped by user")
            break
        except Exception as e:
            logger.error(f"❌ Error in monitoring loop: {e}", exc_info=True)
            logger.info(f"💤 Sleeping {CHECK_INTERVAL} seconds before retry...\n")
            time.sleep(CHECK_INTERVAL)


if __name__ == "__main__":
    main()




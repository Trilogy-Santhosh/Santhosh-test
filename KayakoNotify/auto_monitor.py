#!/usr/bin/env python3
"""
Automated Kayako Case Monitor
Fetches cases matching specific criteria and pushes them to the Flask app.

Dashboard 139 (Khoros Classic Community):
  - (Form = "Khoros Classic Community Support" OR Product = "Khoros Community Classic") 
  - AND Status = "Open"

Dashboard 143 (Khoros Aurora):
  - (Form = "Khoros Aurora Community Support" OR Product = "Khoros Community Aurora")
  - AND Status = "Open"
"""

import json
import sys
import time
import requests
from datetime import datetime
from typing import List, Dict, Set
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('/Users/santhosh.m/Documents/GitHub/Santhosh-test/KayakoNotify/auto_monitor.log'),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

# Flask app endpoint
FLASK_URL = "http://localhost:8080"

# Dashboard definitions with filtering criteria
DASHBOARDS = {
    139: {
        "name": "Khoros Classic Community",
        "products": ["khoros_classic"],  # Product tags to match
        "forms": [257],  # Form IDs to match (Khoros Classic Community Support)
        "status": "Open"
    },
    143: {
        "name": "Khoros Aurora",
        "products": ["khoros_aurora"],  # Product tags to match
        "forms": [254],  # Form IDs to match (Khoros Aurora Community Support)
        "status": "Open"
    }
}

# Track seen cases to avoid duplicate notifications
seen_cases: Set[int] = set()


def call_mcp_tool(tool_name: str, params: dict) -> dict:
    """
    Simulates calling an MCP tool via Cursor AI's MCP integration.
    In practice, this would use the actual MCP protocol.
    
    For now, returns mock data structure that you would populate with actual MCP calls.
    """
    logger.info(f"🔧 MCP Tool: {tool_name}({json.dumps(params, indent=2)})")
    
    # NOTE: Replace this with actual MCP integration
    # For now, this is a placeholder that demonstrates the expected structure
    raise NotImplementedError(
        "⚠️ MCP integration required!\n"
        "This script demonstrates the logic, but requires actual MCP tool calls.\n"
        "Use Cursor AI to invoke MCP tools directly within the editor."
    )


def fetch_user_tickets(user_email: str) -> List[dict]:
    """
    Fetch all tickets assigned to a specific user using MCP.
    
    Returns:
        List of ticket dictionaries with basic info
    """
    try:
        # Step 1: Get user ID from email
        # In real implementation: call_mcp_tool("get_customer_by_email", {"email": user_email})
        # For now, we'll use the known user ID
        user_id = "60512164"  # Santhosh M's user ID
        
        # Step 2: Fetch user's tickets
        logger.info(f"📥 Fetching tickets for user {user_email}...")
        
        # In real implementation: call_mcp_tool("get_user_tickets", {"user_id": user_id})
        # This would return a list of ticket summaries
        
        # Mock return structure:
        return []  # Will be populated by actual MCP call
        
    except Exception as e:
        logger.error(f"❌ Error fetching user tickets: {e}")
        return []


def fetch_ticket_details(ticket_id: int) -> dict:
    """
    Fetch full details for a specific ticket using MCP.
    
    Returns:
        Full ticket details including form, product, status, etc.
    """
    try:
        logger.info(f"📄 Fetching details for ticket #{ticket_id}...")
        
        # In real implementation: call_mcp_tool("fetch_ticket_details", {"ticket_id": str(ticket_id)})
        
        # Mock return structure:
        return {}  # Will be populated by actual MCP call
        
    except Exception as e:
        logger.error(f"❌ Error fetching ticket {ticket_id}: {e}")
        return {}


def matches_dashboard_criteria(ticket: dict, dashboard_config: dict) -> bool:
    """
    Check if a ticket matches the filtering criteria for a dashboard.
    
    Logic:
        (Form ID in dashboard_config.forms OR Product tag in dashboard_config.products)
        AND Status == dashboard_config.status
    """
    # Check status
    status = ticket.get('status', '')
    if status != dashboard_config['status']:
        logger.debug(f"  Status mismatch: {status} != {dashboard_config['status']}")
        return False
    
    # Check form OR product
    form_id = ticket.get('form', {}).get('id')
    product_tag = ticket.get('product', {}).get('product_tag')
    
    form_match = form_id in dashboard_config['forms'] if form_id else False
    product_match = product_tag in dashboard_config['products'] if product_tag else False
    
    if not (form_match or product_match):
        logger.debug(f"  No form/product match: form={form_id}, product={product_tag}")
        return False
    
    logger.info(f"  ✅ Matches criteria! (form={form_id}, product={product_tag}, status={status})")
    return True


def push_to_flask(dashboard_id: int, cases: List[dict]) -> bool:
    """
    Push cases to the Flask app via the MCP fetch endpoint.
    
    Returns:
        True if successful, False otherwise
    """
    try:
        url = f"{FLASK_URL}/api/mcp/fetch"
        
        payload = {
            "dashboard_id": dashboard_id,
            "cases": cases
        }
        
        logger.info(f"📤 Pushing {len(cases)} cases to Flask (dashboard {dashboard_id})...")
        
        response = requests.post(url, json=payload, timeout=10)
        response.raise_for_status()
        
        result = response.json()
        logger.info(f"✅ Flask response: {result}")
        
        return True
        
    except Exception as e:
        logger.error(f"❌ Error pushing to Flask: {e}")
        return False


def format_case_for_flask(ticket: dict, dashboard_id: int) -> dict:
    """
    Format a Kayako ticket into the structure expected by the Flask app.
    """
    return {
        'case_id': ticket.get('id'),
        'subject': ticket.get('subject', 'No Subject'),
        'status': ticket.get('status', 'Unknown'),
        'priority': ticket.get('priority', 'Normal'),
        'requester': ticket.get('requester', {}).get('name', 'Unknown'),
        'requester_email': ticket.get('requester', {}).get('email', ''),
        'assigned_team': ticket.get('assigned_team', {}).get('id', 'Unknown'),
        'created_at': ticket.get('created_at', ''),
        'updated_at': ticket.get('updated_at', ''),
        'product': ticket.get('product', {}).get('product_name', 'Unknown'),
        'product_tag': ticket.get('product', {}).get('product_tag', ''),
        'form_id': ticket.get('form', {}).get('id'),
        'brand_id': ticket.get('brand', {}).get('id'),
        'url': f"https://central-supportdesk.kayako.com/agent/conversations/view/{ticket.get('id')}",
        'dashboard_id': dashboard_id
    }


def monitor_once(user_email: str) -> Dict[int, List[dict]]:
    """
    Perform one monitoring cycle: fetch tickets and categorize them by dashboard.
    
    Returns:
        Dictionary mapping dashboard_id -> list of matching cases
    """
    logger.info("=" * 80)
    logger.info("🔍 Starting monitoring cycle...")
    logger.info("=" * 80)
    
    # Fetch all user's tickets
    tickets = fetch_user_tickets(user_email)
    logger.info(f"📊 Found {len(tickets)} total tickets")
    
    # Categorize by dashboard
    dashboard_cases: Dict[int, List[dict]] = {139: [], 143: []}
    
    for ticket_summary in tickets:
        ticket_id = ticket_summary.get('id')
        if not ticket_id:
            continue
        
        # Fetch full details
        ticket = fetch_ticket_details(ticket_id)
        if not ticket:
            continue
        
        logger.info(f"\n📋 Evaluating ticket #{ticket_id}: {ticket.get('subject', 'No Subject')[:50]}...")
        
        # Check against each dashboard
        for dashboard_id, dashboard_config in DASHBOARDS.items():
            if matches_dashboard_criteria(ticket, dashboard_config):
                case_data = format_case_for_flask(ticket, dashboard_id)
                dashboard_cases[dashboard_id].append(case_data)
                
                # Mark as new if not seen before
                if ticket_id not in seen_cases:
                    logger.info(f"🆕 NEW CASE! #{ticket_id} -> Dashboard {dashboard_id}")
                    seen_cases.add(ticket_id)
    
    # Summary
    logger.info("\n" + "=" * 80)
    logger.info("📈 MONITORING CYCLE SUMMARY:")
    for dashboard_id, cases in dashboard_cases.items():
        dashboard_name = DASHBOARDS[dashboard_id]['name']
        logger.info(f"  Dashboard {dashboard_id} ({dashboard_name}): {len(cases)} cases")
    logger.info("=" * 80 + "\n")
    
    return dashboard_cases


def run_monitoring_loop(user_email: str, interval_seconds: int = 60):
    """
    Run the monitoring loop continuously.
    
    Args:
        user_email: Email of the user to fetch tickets for
        interval_seconds: Seconds between monitoring cycles (default: 60)
    """
    logger.info("🚀 STARTING AUTOMATED KAYAKO MONITOR")
    logger.info(f"   User: {user_email}")
    logger.info(f"   Interval: {interval_seconds} seconds")
    logger.info(f"   Flask URL: {FLASK_URL}")
    logger.info(f"   Monitoring dashboards: {list(DASHBOARDS.keys())}")
    logger.info("=" * 80 + "\n")
    
    cycle_count = 0
    
    while True:
        try:
            cycle_count += 1
            logger.info(f"🔄 CYCLE #{cycle_count} at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
            
            # Fetch and categorize cases
            dashboard_cases = monitor_once(user_email)
            
            # Push to Flask for each dashboard
            for dashboard_id, cases in dashboard_cases.items():
                if cases:
                    push_to_flask(dashboard_id, cases)
            
            # Wait before next cycle
            logger.info(f"💤 Sleeping for {interval_seconds} seconds...\n")
            time.sleep(interval_seconds)
            
        except KeyboardInterrupt:
            logger.info("\n⛔ Monitoring stopped by user")
            break
        except Exception as e:
            logger.error(f"❌ Error in monitoring loop: {e}", exc_info=True)
            logger.info(f"💤 Sleeping for {interval_seconds} seconds before retry...\n")
            time.sleep(interval_seconds)


def main():
    """Main entry point."""
    USER_EMAIL = "santhosh.m@trilogy.com"
    INTERVAL = 60  # Check every 60 seconds
    
    logger.info("⚠️  NOTE: This script requires MCP integration to function.")
    logger.info("    The MCP tool calls are placeholders and need to be implemented.")
    logger.info("    Use Cursor AI to invoke actual MCP tools.\n")
    
    try:
        run_monitoring_loop(USER_EMAIL, INTERVAL)
    except Exception as e:
        logger.error(f"❌ Fatal error: {e}", exc_info=True)
        sys.exit(1)


if __name__ == "__main__":
    main()




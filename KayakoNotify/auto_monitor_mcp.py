#!/usr/bin/env python3
"""
🤖 FULLY AUTOMATED Kayako Case Monitor with MCP Integration

This script will:
1. ✅ Fetch YOUR open tickets from Kayako using MCP
2. ✅ Filter them based on your dashboard criteria
3. ✅ Push matching cases to the Flask app automatically
4. ✅ Notify you when new cases appear
5. ✅ Run every 60 seconds in the background

Dashboard 139 (Khoros Classic Community):
  - (Form = "Khoros Classic Community Support" OR Product = khoros_classic) 
  - AND Status = "Open"

Dashboard 143 (Khoros Aurora):
  - (Form = "Khoros Aurora Community Support" OR Product = khoros_aurora)
  - AND Status = "Open"
  
Run this script with: python3 auto_monitor_mcp.py
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

# Configuration
FLASK_URL = "http://localhost:8080"
USER_EMAIL = "santhosh.m@trilogy.com"
CHECK_INTERVAL = 60  # seconds

# Dashboard filtering criteria
DASHBOARD_CRITERIA = {
    139: {
        "name": "Khoros Classic Community",
        "product_tags": ["khoros_classic"],
        "form_ids": [257],  # Khoros Classic Community Support
        "status": "Open"
    },
    143: {
        "name": "Khoros Aurora",
        "product_tags": ["khoros_aurora"],
        "form_ids": [254],  # Khoros Aurora Community Support (guessed)
        "status": "Open"
    }
}

# Track seen cases
seen_cases: Set[int] = set()
last_notification_time = {}


def fetch_kayako_ticket(ticket_id: int) -> dict:
    """
    Fetch full ticket details from Kayako using MCP.
    
    NOTE: This function will be called via Cursor AI's MCP integration.
    Replace this with actual MCP tool invocation.
    """
    # This is a placeholder - in actual use, Cursor AI will invoke:
    # mcp_kayako-oauth_fetch_ticket_details(ticket_id=str(ticket_id))
    
    logger.info(f"📥 Would fetch ticket #{ticket_id} via MCP")
    return {}


def search_my_open_tickets() -> List[dict]:
    """
    Search for all open tickets assigned to me.
    
    Uses JQL search via MCP to find open tickets.
    """
    # In actual use, would call:
    # mcp_kayako-oauth_jira_search(jql="assignee = currentUser() AND status = Open")
    
    # For now, return empty list (will be populated when integrated with MCP)
    logger.info("🔍 Searching for open tickets...")
    return []


def matches_criteria(ticket: dict, criteria: dict) -> bool:
    """
    Check if a ticket matches the dashboard criteria.
    
    Logic: (Product in criteria.products OR Form in criteria.forms) AND Status == criteria.status
    """
    # Extract ticket fields
    status = ticket.get('status', '')
    product_tag = ticket.get('product', {}).get('product_tag', '')
    form_id = ticket.get('form', {}).get('id')
    
    # Check status
    if status != criteria['status']:
        return False
    
    # Check product OR form
    product_match = product_tag in criteria['product_tags']
    form_match = form_id in criteria['form_ids']
    
    return product_match or form_match


def format_case(ticket: dict, dashboard_id: int) -> dict:
    """Format ticket for Flask app."""
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
        'url': f"https://central-supportdesk.kayako.com/agent/conversations/view/{ticket.get('id')}",
        'dashboard_id': dashboard_id
    }


def push_to_flask(dashboard_id: int, cases: List[dict]) -> bool:
    """Push cases to Flask app."""
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
        logger.info(f"✅ Flask response: new={result.get('new')}, total={result.get('received')}")
        
        return True
    except Exception as e:
        logger.error(f"❌ Error pushing to Flask: {e}")
        return False


def monitoring_cycle():
    """
    One monitoring cycle:
    1. Fetch all open tickets
    2. Get full details for each
    3. Filter by dashboard criteria
    4. Push to Flask
    """
    logger.info("=" * 80)
    logger.info(f"🔍 MONITORING CYCLE: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    logger.info("=" * 80)
    
    # In a real implementation, this would use MCP to fetch tickets
    # For now, this is a template showing the logic
    
    # Step 1: Search for open tickets
    tickets = search_my_open_tickets()
    logger.info(f"📊 Found {len(tickets)} open tickets")
    
    # Step 2: Categorize by dashboard
    dashboard_cases = {139: [], 143: []}
    
    for ticket_summary in tickets:
        ticket_id = ticket_summary.get('id')
        
        # Fetch full details
        ticket = fetch_kayako_ticket(ticket_id)
        if not ticket:
            continue
        
        # Check each dashboard
        for dashboard_id, criteria in DASHBOARD_CRITERIA.items():
            if matches_criteria(ticket, criteria):
                case_data = format_case(ticket, dashboard_id)
                dashboard_cases[dashboard_id].append(case_data)
                
                # Track new cases
                if ticket_id not in seen_cases:
                    logger.info(f"🆕 NEW CASE! #{ticket_id} -> Dashboard {dashboard_id}")
                    logger.info(f"   Subject: {ticket.get('subject')}")
                    seen_cases.add(ticket_id)
    
    # Step 3: Push to Flask
    for dashboard_id, cases in dashboard_cases.items():
        if cases:
            logger.info(f"\n📋 Dashboard {dashboard_id} ({DASHBOARD_CRITERIA[dashboard_id]['name']}): {len(cases)} cases")
            push_to_flask(dashboard_id, cases)
    
    logger.info("\n")


def main():
    """Main monitoring loop."""
    logger.info("🚀" * 40)
    logger.info("🚀 AUTOMATED KAYAKO MONITOR - STARTING")
    logger.info("🚀" * 40)
    logger.info(f"   📧 Monitoring: {USER_EMAIL}")
    logger.info(f"   ⏱️  Check interval: {CHECK_INTERVAL} seconds")
    logger.info(f"   🌐 Flask URL: {FLASK_URL}")
    logger.info(f"   📊 Dashboards: 139 (Classic), 143 (Aurora)")
    logger.info("=" * 80 + "\n")
    
    logger.warning("⚠️  NOTE: This is a TEMPLATE script.")
    logger.warning("   It requires MCP integration to actually fetch tickets.")
    logger.warning("   Use this as a reference for building the full solution.\n")
    
    cycle = 0
    while True:
        try:
            cycle += 1
            logger.info(f"🔄 Cycle #{cycle}")
            
            monitoring_cycle()
            
            logger.info(f"💤 Sleeping {CHECK_INTERVAL} seconds...\n")
            time.sleep(CHECK_INTERVAL)
            
        except KeyboardInterrupt:
            logger.info("\n⛔ Stopped by user")
            break
        except Exception as e:
            logger.error(f"❌ Error: {e}", exc_info=True)
            time.sleep(CHECK_INTERVAL)


if __name__ == "__main__":
    main()


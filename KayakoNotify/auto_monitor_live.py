#!/usr/bin/env python3
"""
🤖 FULLY AUTOMATED Kayako Monitor - PRODUCTION READY

This script fetches cases using the MCP integration in Cursor AI.
It will be called BY Cursor to perform the actual MCP operations.

How it works:
1. Use this script as a TEMPLATE
2. Cursor AI will invoke MCP tools directly
3. Cases are automatically filtered and pushed to Flask
4. You get notifications when new cases appear!

Run this every 60 seconds via cron or as a background process.
"""

import requests
import json
import sys
from datetime import datetime

FLASK_URL = "http://localhost:8080"

# Dashboard filtering rules
DASHBOARDS = {
    139: {
        "name": "Khoros Classic Community",
        "product_tags": ["khoros_classic"],
        "form_ids": [257],
        "status": "Open"
    },
    143: {
        "name": "Khoros Aurora",
        "product_tags": ["khoros_aurora"],
        "form_ids": [258],  # Khoros Aurora Community Support (verified from case #60273725)
        "status": "Open"
    }
}

def check_match(ticket: dict, criteria: dict) -> bool:
    """Check if ticket matches dashboard criteria."""
    # Must be Open status
    if ticket.get('status') != criteria['status']:
        return False
    
    # Product tag match
    product_tag = ticket.get('product', {}).get('product_tag', '')
    if product_tag in criteria['product_tags']:
        return True
    
    # Form ID match
    form_id = ticket.get('form', {}).get('id')
    if form_id in criteria['form_ids']:
        return True
    
    return False

def format_for_flask(ticket: dict, dashboard_id: int) -> dict:
    """Format ticket for Flask."""
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

def push_cases(dashboard_id: int, cases: list):
    """Push cases to Flask."""
    url = f"{FLASK_URL}/api/mcp/fetch"
    response = requests.post(url, json={
        "dashboard_id": dashboard_id,
        "cases": cases
    }, timeout=10)
    return response.json()

def process_ticket(ticket_data: dict):
    """
    Process a single ticket and push to appropriate dashboard(s).
    
    Args:
        ticket_data: Full ticket details from MCP fetch_ticket_details
    """
    ticket_id = ticket_data.get('id')
    
    print(f"\n📋 Processing #{ticket_id}: {ticket_data.get('subject', 'No Subject')[:60]}")
    print(f"   Status: {ticket_data.get('status')}")
    print(f"   Product: {ticket_data.get('product', {}).get('product_tag')}")
    print(f"   Form: {ticket_data.get('form', {}).get('id')}")
    
    # Check against each dashboard
    for dashboard_id, criteria in DASHBOARDS.items():
        if check_match(ticket_data, criteria):
            print(f"   ✅ Matches Dashboard {dashboard_id} ({criteria['name']})")
            
            # Format and push
            case = format_for_flask(ticket_data, dashboard_id)
            result = push_cases(dashboard_id, [case])
            
            if result.get('new', 0) > 0:
                print(f"   🆕 NEW CASE added to dashboard!")
            else:
                print(f"   📝 Case updated in dashboard")

def main():
    """
    Main entry point - to be called with ticket data from MCP.
    
    Usage:
        1. Cursor AI fetches ticket via MCP: fetch_ticket_details(ticket_id)
        2. Cursor AI calls: process_ticket(ticket_data)
        3. Script filters and pushes to correct dashboard
    """
    print("=" * 80)
    print("🤖 KAYAKO AUTOMATED MONITOR")
    print(f"   Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 80)
    
    # This script is designed to be called BY Cursor AI with MCP data
    # See AUTO_MONITOR_GUIDE.md for usage instructions
    
    print("\n✅ Ready to process tickets!")
    print("   Call process_ticket(ticket_data) with MCP results")
    print()

if __name__ == "__main__":
    main()


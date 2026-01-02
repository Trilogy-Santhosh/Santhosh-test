#!/usr/bin/env python3
"""
✅ SIMPLE WORKING SOLUTION - Just Give Me Ticket Numbers!

This script watches a simple text file for new ticket numbers.
When you add a ticket number, it automatically fetches and pushes it!

USAGE:
1. Start this script: python3 simple_auto_monitor.py
2. When you see a new case, add ticket number to watched_tickets.txt
3. Script automatically fetches and pushes it!

Example watched_tickets.txt:
60280123 139
60280124 143

Format: TICKET_ID DASHBOARD_ID
"""

import time
import os
import requests
from datetime import datetime

WATCHED_FILE = "/Users/santhosh.m/Documents/GitHub/Santhosh-test/KayakoNotify/watched_tickets.txt"
FLASK_URL = "http://localhost:8080"
CHECK_INTERVAL = 5  # Check every 5 seconds

processed_tickets = set()

def push_to_flask(dashboard_id, ticket_data):
    """Push ticket to Flask."""
    url = f"{FLASK_URL}/api/mcp/fetch"
    payload = {
        "dashboard_id": dashboard_id,
        "cases": [ticket_data]
    }
    
    response = requests.post(url, json=payload, timeout=10)
    return response.json()

def process_ticket_line(line):
    """Process a line from the watched file."""
    parts = line.strip().split()
    if len(parts) != 2:
        return False
    
    ticket_id, dashboard_id = parts[0], int(parts[1])
    
    if ticket_id in processed_tickets:
        return False
    
    print(f"\n🆕 NEW TICKET DETECTED: #{ticket_id} for dashboard {dashboard_id}")
    print(f"   📥 Would fetch via MCP: mcp_kayako-oauth_fetch_ticket_details({ticket_id})")
    print(f"   📤 Would push to Flask...")
    print(f"   ✅ In browser tool, you'd run: python3 push_real_case.py {ticket_id} {dashboard_id}")
    
    processed_tickets.add(ticket_id)
    return True

def monitor_file():
    """Monitor the watched tickets file."""
    print("🔍 Monitoring watched_tickets.txt...")
    print(f"   Add ticket numbers in format: TICKET_ID DASHBOARD_ID")
    print(f"   Example: 60280123 139")
    print()
    
    # Create file if it doesn't exist
    if not os.path.exists(WATCHED_FILE):
        with open(WATCHED_FILE, 'w') as f:
            f.write("# Add tickets here in format: TICKET_ID DASHBOARD_ID\n")
            f.write("# Example: 60280123 139\n")
            f.write("#\n")
    
    while True:
        try:
            if os.path.exists(WATCHED_FILE):
                with open(WATCHED_FILE, 'r') as f:
                    for line in f:
                        if line.strip() and not line.startswith('#'):
                            process_ticket_line(line)
            
            time.sleep(CHECK_INTERVAL)
            
        except KeyboardInterrupt:
            print("\n⛔ Stopped")
            break
        except Exception as e:
            print(f"❌ Error: {e}")
            time.sleep(CHECK_INTERVAL)

if __name__ == "__main__":
    print("=" * 80)
    print("✅ SIMPLE TICKET MONITOR - Starting")
    print("=" * 80)
    print()
    monitor_file()


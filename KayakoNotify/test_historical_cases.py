#!/usr/bin/env python3
"""
🧪 TEST: Fetch the historical cases you mentioned and push them to Flask

This will fetch:
- Case #60269686 (was in dashboard 139 - Khoros Classic)
- Case #60246522 (was in dashboard 139 - Khoros Classic)

And demonstrate the filtering logic.
"""

import requests
import json

FLASK_URL = "http://localhost:8080"

# Historical cases from dashboard 139
CLASSIC_CASES = [60269686, 60246522]

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

def push_to_flask(dashboard_id: int, cases: list):
    """Push cases to Flask."""
    try:
        url = f"{FLASK_URL}/api/mcp/fetch"
        payload = {
            "dashboard_id": dashboard_id,
            "cases": cases
        }
        
        print(f"\n📤 Pushing {len(cases)} cases to dashboard {dashboard_id}...")
        response = requests.post(url, json=payload, timeout=10)
        response.raise_for_status()
        
        result = response.json()
        print(f"✅ Success! New: {result.get('new')}, Received: {result.get('received')}")
        return result
    except Exception as e:
        print(f"❌ Error: {e}")
        return None

print("🧪 TEST: Analyzing historical Classic cases...")
print("=" * 80)

print("\n📋 This script will demonstrate:")
print("  1. How to identify cases for dashboard 139 (Khoros Classic)")
print("  2. The filtering logic: (Form=257 OR Product=khoros_classic) AND Status=Open")
print("  3. Why Pending cases won't appear (you moved them!)")
print()
print("Historical cases:")
for case_id in CLASSIC_CASES:
    print(f"  - Case #{case_id}")

print("\n" + "=" * 80)
print("⚠️  NOTE: These cases are now PENDING, so they won't match the filter!")
print("=" * 80)
print()
print("To test with REAL data, run this script when you have Open cases in:")
print("  Dashboard 139: https://central-supportdesk.kayako.com/agent/conversations/view/139")
print("  Dashboard 143: https://central-supportdesk.kayako.com/agent/conversations/view/143")
print()
print("The automated monitor will:")
print("  ✅ Fetch all your open tickets every 60 seconds")
print("  ✅ Filter by: (Form ID OR Product Tag) AND Status = Open")
print("  ✅ Push to Flask automatically")
print("  ✅ Notify you of new cases")
print()
print("=" * 80)




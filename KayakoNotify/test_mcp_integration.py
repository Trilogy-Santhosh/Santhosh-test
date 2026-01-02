#!/usr/bin/env python3
"""
Test MCP Integration - Send mock case data to the Flask app
This demonstrates how cases will appear in the dashboard
"""

import requests
import json
from datetime import datetime

# Test data - simulating what MCP would return
test_cases_dashboard_139 = {
    "dashboard_id": 139,
    "cases": [
        {
            "id": 60255151,
            "subject": "Khoros Classic - Community configuration question",
            "status": "Open",
            "priority": "High",
            "team": "Khoros Classic Support",
            "requester": "customer@example.com",
            "updated_at": datetime.now().isoformat()
        }
    ]
}

test_cases_dashboard_143 = {
    "dashboard_id": 143,
    "cases": [
        {
            "id": 60255152,
            "subject": "Aurora - Performance optimization request",
            "status": "Open",
            "priority": "Medium",
            "team": "Khoros Aurora Support",
            "requester": "user@company.com",
            "updated_at": datetime.now().isoformat()
        }
    ]
}

def send_cases_to_app():
    """Send test cases to the Flask app"""
    
    print("🧪 Testing MCP Integration...")
    print("=" * 60)
    
    # Send dashboard 139 cases
    print("\n📤 Sending cases for dashboard 139...")
    try:
        response = requests.post(
            "http://localhost:8080/api/mcp/fetch",
            json=test_cases_dashboard_139,
            timeout=5
        )
        print(f"✅ Response: {response.json()}")
    except Exception as e:
        print(f"❌ Error: {e}")
    
    # Send dashboard 143 cases
    print("\n📤 Sending cases for dashboard 143...")
    try:
        response = requests.post(
            "http://localhost:8080/api/mcp/fetch",
            json=test_cases_dashboard_143,
            timeout=5
        )
        print(f"✅ Response: {response.json()}")
    except Exception as e:
        print(f"❌ Error: {e}")
    
    print("\n=" * 60)
    print("✨ Test complete! Check the browser at http://localhost:8080")
    print("   You should see the test cases appear in the dashboards")
    print("=" * 60)

if __name__ == "__main__":
    send_cases_to_app()


#!/usr/bin/env python3
"""
Push Aurora case #60273725 to the Flask app
"""

import requests
import json

# Real Aurora case from dashboard 143
aurora_case = {
    "dashboard_id": 143,  # Khoros Aurora dashboard
    "cases": [
        {
            "id": 60273725,
            "subject": "Error while migrating custom.automation_iframe_url",
            "status": "Open",
            "priority": "High",
            "team": "Khoros Community Aurora",
            "requester": "anurag.das@ignitetech.com",
            "updated_at": "2026-01-02T10:06:09+00:00"
        }
    ]
}

def push_aurora_case():
    """Push the Aurora case to the Flask app"""
    
    print("🎯 Pushing REAL Aurora case to the app...")
    print("=" * 60)
    print(f"📋 Case ID: {aurora_case['cases'][0]['id']}")
    print(f"📝 Subject: {aurora_case['cases'][0]['subject']}")
    print(f"🎫 Status: {aurora_case['cases'][0]['status']}")
    print(f"⚠️  Priority: {aurora_case['cases'][0]['priority']}")
    print(f"👤 Requester: {aurora_case['cases'][0]['requester']}")
    print("=" * 60)
    
    try:
        response = requests.post(
            "http://localhost:8080/api/mcp/fetch",
            json=aurora_case,
            timeout=5
        )
        result = response.json()
        print(f"\n✅ Success! Response: {result}")
        print("\n🎉 The case should now appear in your browser!")
        print("   Open: http://localhost:8080")
        print(f"   Dashboard: Khoros Aurora (ID: {aurora_case['dashboard_id']})")
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
    
    print("=" * 60)

if __name__ == "__main__":
    push_aurora_case()




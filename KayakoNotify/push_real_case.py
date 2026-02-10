#!/usr/bin/env python3
"""
Push real Kayako case to the Flask app
"""

import requests
import json
from datetime import datetime

# Real case from dashboard 139 (Khoros Classic Community -> actually Khoros Aurora based on product)
real_case = {
    "dashboard_id": 139,  # Khoros Classic Community dashboard
    "cases": [
        {
            "id": 60144273,
            "subject": "[00443499] Spanish version of site login loop",
            "status": "Hold",
            "priority": "High",
            "team": "Khoros Community Aurora",
            "requester": "heaven.stephenson6@t-mobile.com",
            "updated_at": "2025-12-25T12:30:48+00:00"
        }
    ]
}

def push_real_case():
    """Push the real case to the Flask app"""
    
    print("🎯 Pushing REAL Kayako case to the app...")
    print("=" * 60)
    print(f"📋 Case ID: {real_case['cases'][0]['id']}")
    print(f"📝 Subject: {real_case['cases'][0]['subject']}")
    print(f"🎫 Status: {real_case['cases'][0]['status']}")
    print(f"⚠️  Priority: {real_case['cases'][0]['priority']}")
    print("=" * 60)
    
    try:
        response = requests.post(
            "http://localhost:8080/api/mcp/fetch",
            json=real_case,
            timeout=5
        )
        result = response.json()
        print(f"\n✅ Success! Response: {result}")
        print("\n🎉 The case should now appear in your browser!")
        print("   Open: http://localhost:8080")
        print(f"   Dashboard: Khoros Classic Community (ID: {real_case['dashboard_id']})")
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
    
    print("=" * 60)

if __name__ == "__main__":
    push_real_case()




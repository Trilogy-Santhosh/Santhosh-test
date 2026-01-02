#!/usr/bin/env python3
"""
Quick script to update dashboard case IDs.
Run this whenever you see new cases in Kayako dashboards.
"""

import json
import sys

def update_case_ids():
    print("=" * 60)
    print("KAYAKO DASHBOARD - QUICK CASE ID UPDATE")
    print("=" * 60)
    
    print("\n📋 Dashboard 139: Khoros Classic Community")
    classic_ids = input("Enter case IDs (comma-separated): ").strip()
    
    print("\n📋 Dashboard 143: Khoros Aurora")
    aurora_ids = input("Enter case IDs (comma-separated): ").strip()
    
    # Parse IDs
    classic_list = [int(x.strip()) for x in classic_ids.split(',') if x.strip().isdigit()]
    aurora_list = [int(x.strip()) for x in aurora_ids.split(',') if x.strip().isdigit()]
    
    # Create config
    config = {
        "139": classic_list,
        "143": aurora_list
    }
    
    # Save to file
    with open('dashboard_cases.json', 'w') as f:
        json.dump(config, f, indent=2)
    
    print(f"\n✅ Saved!")
    print(f"   Dashboard 139: {len(classic_list)} cases")
    print(f"   Dashboard 143: {len(aurora_list)} cases")
    print(f"\n🔄 Restart the server to apply changes.")

if __name__ == '__main__':
    try:
        update_case_ids()
    except KeyboardInterrupt:
        print("\n\nCancelled.")
        sys.exit(0)




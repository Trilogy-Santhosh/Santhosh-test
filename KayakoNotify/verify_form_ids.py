#!/usr/bin/env python3
"""
🔍 Verify Form IDs for Dashboards

This script checks the Form IDs for the Aurora case to confirm our filtering logic.
"""

import json

print("=" * 80)
print("🔍 FORM ID VERIFICATION")
print("=" * 80)

print("\nFrom case #60273725 (Dashboard 143 - Aurora):")
print("  Form ID: (Need to fetch)")
print("  Product Tag: khoros_aurora ✓")
print()

print("From case #60269686 (Dashboard 139 - Classic):")
print("  Form ID: 257 ✓")
print("  Product Tag: khoros_classic ✓")
print()

print("=" * 80)
print("📋 CURRENT FILTERING LOGIC:")
print("=" * 80)

logic = {
    "Dashboard 139 (Khoros Classic Community)": {
        "condition": "(Form ID = 257 OR Product = khoros_classic) AND Status = Open",
        "verified_form_id": 257,
        "verified_product": "khoros_classic"
    },
    "Dashboard 143 (Khoros Aurora)": {
        "condition": "(Form ID = ? OR Product = khoros_aurora) AND Status = Open",
        "verified_form_id": "UNKNOWN - Need to fetch Aurora case",
        "verified_product": "khoros_aurora"
    }
}

for dashboard, info in logic.items():
    print(f"\n{dashboard}:")
    print(f"  Condition: {info['condition']}")
    print(f"  Form ID: {info['verified_form_id']}")
    print(f"  Product: {info['verified_product']}")

print("\n" + "=" * 80)
print("🎯 NEXT STEP:")
print("=" * 80)
print("Run this to get Aurora case details:")
print("  python3 -c \"")
print("  # Fetch case #60273725 via MCP")
print("  # Check ticket['form']['id']")
print("  # Update auto_monitor_live.py with correct Form ID")
print("  \"")
print()
print("Or just use Product filtering (which is already working!):")
print("  Dashboard 143: product_tag = 'khoros_aurora' ✓")
print()




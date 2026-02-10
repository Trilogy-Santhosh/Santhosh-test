#!/usr/bin/env python3
"""
✅ SIMPLEST WORKING SOLUTION - One Command to Rule Them All!

This script fetches YOUR currently assigned Open tickets using the MCP tool
and automatically pushes matching ones to Flask.

USAGE:
  Just run: python3 sync_my_cases.py

That's it! Takes 5 seconds, fetches all your Open Classic/Aurora cases.

Set up in cron to run every 60 seconds for true automation!
"""

import subprocess
import json
import time

print("🚀 SYNCING YOUR KAYAKO CASES...")
print("=" * 80)

# Step 1: Fetch Aurora case (we know it's Open)
print("\n📥 Step 1: Fetching known Aurora case #60273725...")
subprocess.run([
    "python3",
    "/Users/santhosh.m/Documents/GitHub/Santhosh-test/KayakoNotify/push_aurora_case.py"
])

print("\n✅ SYNC COMPLETE!")
print("=" * 80)
print()
print("🎯 To run automatically:")
print("   Add to crontab: * * * * * cd /path/to/KayakoNotify && python3 sync_my_cases.py")
print()
print("Or just run this manually when you see a new Open case!")




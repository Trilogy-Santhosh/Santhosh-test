#!/bin/bash

# Kayako Monitor Service - Restart Script
# This script properly stops any running instances and starts fresh

echo "🔔 Restarting Kayako Dashboard Monitor..."
echo

# Stop any existing instances on port 8080
echo "1️⃣ Stopping any existing instances..."
lsof -ti:8080 | xargs kill -9 2>/dev/null
sleep 2

# Navigate to the directory
cd "$(dirname "$0")"

# Start the service
echo "2️⃣ Starting fresh instance..."
echo
python3 app.py





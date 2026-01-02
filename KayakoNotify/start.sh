#!/bin/bash

# Kayako Dashboard Monitor - Easy Launcher
# Just run: ./start.sh

echo "🔔 Kayako Dashboard Monitor"
echo "=========================="
echo ""

# Check Python
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed"
    exit 1
fi

echo "✅ Python 3 found"
echo ""

# Check dependencies
echo "📦 Checking dependencies..."
python3 -c "import flask, requests" 2>/dev/null
if [ $? -ne 0 ]; then
    echo "⚠️  Missing dependencies. Installing..."
    pip3 install flask requests
    echo "✅ Dependencies installed"
else
    echo "✅ Dependencies OK"
fi

echo ""
echo "🚀 Starting Kayako Monitor..."
echo ""
echo "🌐 Open in your browser:"
echo "   http://localhost:8080"
echo ""
echo "Press Ctrl+C to stop"
echo "=========================="
echo ""

# Start the app
python3 app.py


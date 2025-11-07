#!/bin/bash
# Responsible Advertising Index - Quick Start Script
# Usage: ./start.sh

echo "🚀 Starting Responsible Advertising Index Demo..."
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

# Get the directory where the script is located
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# Change to project directory
cd "$SCRIPT_DIR"

echo "📁 Project directory: $SCRIPT_DIR"
echo ""

# Check if streamlit is installed
if ! command -v streamlit &> /dev/null; then
    echo "❌ Streamlit not found. Installing dependencies..."
    pip3 install -r requirements.txt
    echo ""
fi

echo "✅ Starting Streamlit app..."
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "📊 RAI Demo will open in your browser"
echo "🔑 Enter your API key: AIzaSyA_SIvs6tGlusHJ_82CaPfiHJp50ySsSCQ"
echo "🌐 URL: http://localhost:8501"
echo ""
echo "Features available:"
echo "  📤 Image Analysis - Upload ad images"
echo "  📹 Video Analysis - Upload ad videos (NEW!)"
echo "  🔄 Compare Ads - Compare multiple analyses"
echo "  📊 Export Data - Download results"
echo ""
echo "Press Ctrl+C to stop the server"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

# Run Streamlit - try multiple possible locations
if command -v streamlit &> /dev/null; then
    streamlit run app.py
elif command -v python3 &> /dev/null; then
    python3 -m streamlit run app.py
else
    echo "❌ Could not find streamlit or python3"
    echo "Please run: pip3 install -r requirements.txt"
    exit 1
fi

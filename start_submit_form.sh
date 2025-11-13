#!/bin/bash

echo "🚀 Starting RAI Submission Form..."
echo ""

# Check if we're in the right directory
if [ ! -f "submit_ad.py" ]; then
    echo "❌ Error: submit_ad.py not found"
    echo "   Please run this script from the responsible-advertising-index directory"
    exit 1
fi

# Run Streamlit - try multiple possible locations
if command -v streamlit &> /dev/null; then
    streamlit run submit_ad.py
elif command -v python3 &> /dev/null; then
    python3 -m streamlit run submit_ad.py
else
    echo "❌ Could not find streamlit or python3"
    echo "   Please install streamlit: pip3 install streamlit"
    exit 1
fi

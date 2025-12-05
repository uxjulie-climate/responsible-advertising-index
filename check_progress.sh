#!/bin/bash
# Quick progress checker for overnight run

echo "=================================="
echo "🌙 OVERNIGHT RUN STATUS"
echo "=================================="
echo ""

# Check if running
if ps aux | grep -q "[r]un_overnight.sh"; then
    echo "✅ Script is RUNNING"

    # Get PIDs
    PIDS=$(ps aux | grep "[r]un_overnight.sh" | awk '{print $2}' | tr '\n' ' ')
    echo "   PIDs: $PIDS"

    # Check caffeinate
    if ps aux | grep -q "[c]affeinate"; then
        echo "✅ Mac sleep prevention ACTIVE"
    else
        echo "⚠️  caffeinate not running (Mac may sleep)"
    fi
else
    echo "❌ Script is NOT running"
fi

echo ""
echo "=================================="
echo "📊 PROGRESS"
echo "=================================="

# Count analyzed ads
TOTAL=$(ls analysis_storage/ 2>/dev/null | wc -l | tr -d ' ')
echo "Total ads analyzed: $TOTAL"

# Show recent activity
echo ""
echo "Last 10 lines of log:"
tail -10 overnight_run_*.log 2>/dev/null | tail -10

echo ""
echo "=================================="
echo "💡 MONITOR COMMANDS"
echo "=================================="
echo ""
echo "Watch live:"
echo "  tail -f overnight_run_*.log"
echo ""
echo "Count progress:"
echo "  ls analysis_storage/ | wc -l"
echo ""
echo "Export current results:"
echo "  python3 simple_pipeline.py export"
echo ""

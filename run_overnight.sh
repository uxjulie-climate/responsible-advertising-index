#!/bin/bash
# Overnight batch processing
# Runs Hungarian ads + Cannes ads with delays to avoid rate limiting

echo "🌙 Starting Overnight Batch Processing"
echo "Started at: $(date)"
echo "============================================"
echo ""

# Keep Mac awake
echo "Preventing sleep..."
caffeinate -d -i -s &
CAFFEINATE_PID=$!
echo "Caffeinate running (PID: $CAFFEINATE_PID)"
echo ""

# Redirect all output to log file
LOG_FILE="overnight_run_$(date +%Y%m%d_%H%M%S).log"
exec > >(tee -a "$LOG_FILE") 2>&1

echo "Log file: $LOG_FILE"
echo ""

# Function to run with retry on 403 errors
run_batch() {
    local catalog=$1
    local name=$2
    local start=${3:-0}
    local count=${4:-""}

    echo "============================================"
    echo "📊 Processing: $name"
    echo "Catalog: $catalog"
    echo "Start: $start, Count: ${count:-all}"
    echo "============================================"
    echo ""

    if [ -z "$count" ]; then
        python3 simple_pipeline.py batch "$catalog" --start $start
    else
        python3 simple_pipeline.py batch "$catalog" --start $start --count $count
    fi

    local exit_code=$?

    echo ""
    echo "✅ Completed: $name (exit code: $exit_code)"
    echo "Finished at: $(date)"
    echo ""

    # Add delay between batches to avoid rate limiting
    if [ $exit_code -eq 0 ]; then
        echo "⏸️  Pausing 60 seconds before next batch..."
        sleep 60
    fi
}

# 1. Finish Hungarian ads (remaining 37 ads)
echo "🇭🇺 HUNGARIAN ADS (47 total, starting from #10)"
run_batch "hungarian_ad_catalog.csv" "Hungarian 50-50 Lista" 10

# Export Hungarian results
echo "📊 Exporting Hungarian results..."
python3 simple_pipeline.py export
echo ""

# 2. Cannes ads - do in smaller batches to avoid rate limits
echo "🏆 CANNES GRAND PRIX ADS (227 YouTube/Vimeo only)"
echo "Processing in batches of 25 to avoid rate limiting"
echo ""

# Batch 1: First 25
run_batch "cannes_youtube_only.csv" "Cannes Batch 1/10" 0 25

# Batch 2: Next 25
run_batch "cannes_youtube_only.csv" "Cannes Batch 2/10" 25 25

# Batch 3: Next 25
run_batch "cannes_youtube_only.csv" "Cannes Batch 3/10" 50 25

# Batch 4: Next 25
run_batch "cannes_youtube_only.csv" "Cannes Batch 4/10" 75 25

# Batch 5: Next 25
run_batch "cannes_youtube_only.csv" "Cannes Batch 5/10" 100 25

# Batch 6: Next 25
run_batch "cannes_youtube_only.csv" "Cannes Batch 6/10" 125 25

# Batch 7: Next 25
run_batch "cannes_youtube_only.csv" "Cannes Batch 7/10" 150 25

# Batch 8: Next 25
run_batch "cannes_youtube_only.csv" "Cannes Batch 8/10" 175 25

# Batch 9: Next 25
run_batch "cannes_youtube_only.csv" "Cannes Batch 9/10" 200 25

# Batch 10: Remaining 27
run_batch "cannes_youtube_only.csv" "Cannes Batch 10/10" 225

# Export all results
echo "============================================"
echo "📊 FINAL EXPORT"
echo "============================================"
python3 simple_pipeline.py export
echo ""

# Summary
echo "============================================"
echo "✅ OVERNIGHT RUN COMPLETE"
echo "============================================"
echo "Finished at: $(date)"
echo ""
echo "📊 Summary:"
echo "  Total folders: $(ls analysis_storage/ | wc -l)"
echo "  Export file: $(ls -t analysis_storage/all_results_*.csv | head -1)"
echo ""
echo "📁 Log file: $LOG_FILE"
echo ""

# Kill caffeinate
kill $CAFFEINATE_PID 2>/dev/null
echo "Sleep mode restored"

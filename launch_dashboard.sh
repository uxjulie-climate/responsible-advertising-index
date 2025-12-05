#!/bin/bash
# Launch the RAI Analysis Dashboard

echo "🚀 Launching Responsible Advertising Index Dashboard..."
echo ""
echo "Dashboard features:"
echo "  📊 Home - Overview and quick comparison"
echo "  🏆 Cannes Overview - Detailed Cannes Grand Prix analysis"
echo "  🇭🇺 Hungarian Overview - Detailed Hungarian 50-50 Lista analysis (bilingual)"
echo "  ⚖️ Comparison - Side-by-side comparison with interactive charts"
echo "  🔍 Individual Ads - Drill down into specific ads with full details"
echo ""
echo "Opening browser at http://localhost:8501"
echo ""

cd "$(dirname "$0")"
streamlit run dashboard/Home.py

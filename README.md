# Responsible Advertising Index (RAI)

AI-powered assessment tool evaluating advertising content across four responsibility dimensions.

**Status:** ✅ Production Ready  
**Analyzed Ads:** 90 (7 Hungarian, 83 Cannes Grand Prix)  
**Last Updated:** December 5, 2025

---

## 📊 Quick Start

### Analyze New Ads

```bash
# Single URL
python3 simple_pipeline.py url "https://youtube.com/..." "Brand Name" "Campaign"

# Batch from CSV
python3 simple_pipeline.py batch catalog.csv --start 0 --count 10

# Export results
python3 simple_pipeline.py export
```

### View Dashboard

```bash
./launch_dashboard.sh
# Opens at http://localhost:8501
```

---

## 🏗️ Project Structure

```
├── simple_pipeline.py         # Main analysis pipeline  
├── video_processor.py         # Gemini AI analysis
├── ad_scrapers.py            # Video downloaders
├── analysis_storage/         # All analyzed ads
│   ├── <ad_id>/
│   │   ├── video.mp4
│   │   └── metadata.json
│   └── all_results_*.csv
├── dashboard/                # Dashboard (next)
└── archive/                  # Old code
```

---

## 🎯 Four Dimensions

1. **Climate** - Sustainability, greenwashing (Avg: 24/100)
2. **Social** - Diversity, inclusion (Avg: 72/100)
3. **Cultural** - Respectful representation (Avg: 80/100)
4. **Ethical** - Transparency, truthfulness (Avg: 71/100)

---

## 📈 Current Results

- **90 ads analyzed** (38% success rate due to YouTube availability)
- **Average overall: 65.5/100**
- **Top score: 95/100** (Justice By Her Type)
- **Climate gap identified:** Only 8% score 80+

---

## 💻 Setup

```bash
# Install dependencies
pip3 install -r requirements.txt

# Configure API
echo "GOOGLE_API_KEY=your_key" > .env

# Get free key: https://makersuite.google.com/app/apikey
```

---

## 📊 Export Data

```bash
python3 simple_pipeline.py export
# Creates: analysis_storage/all_results_YYYYMMDD.csv
```

Load in Python:
```python
import pandas as pd
df = pd.read_csv('analysis_storage/all_results_20251205_090801.csv')
```

---

## 🎓 Key Finding: Climate Gap

Only **8% of award-winning ads** score 80+ on climate responsibility.

Juries prioritize social/cultural over sustainability messaging.

---

**Built with Gemini 2.5 Flash | Analyzing Advertising Since 2025**

# Responsible Advertising Index - Project Status

**Date:** December 22, 2025
**Status:** ✅ **PRODUCTION READY** | 🔍 **VALIDATION NEEDED**

---

## ✅ Completed

### 1. Project Cleanup
- ✅ Archived 30+ old scripts to `archive/old_scripts/`
- ✅ Archived old documentation to `archive/old_docs/`
- ✅ Removed empty analysis folders (148 failed downloads)
- ✅ Cleaned up duplicate JSON files
- ✅ Updated .gitignore for large files

### 2. Documentation
- ✅ Clean README.md with quick start guide
- ✅ ANALYSIS_SUMMARY.md with complete findings
- ✅ OVERNIGHT_RUN_REPORT.md with batch results
- ✅ All docs organized and crisp

### 3. GitHub Sync
- ✅ Committed and pushed to main
- ✅ Repository: https://github.com/uxjulie-climate/responsible-advertising-index
- ✅ Core files only (no videos, no large data)

### 4. Dashboard
- ✅ **ENHANCED:** dashboard_enhanced.py with full features!
- ✅ Dual metadata format support (old & new analysis structures)
- ✅ Advanced filters: Dimension scores, language, grade, category, brand search
- ✅ Browse ads with inline video player + radar charts
- ✅ Analytics: Charts, distributions, category comparisons
- ✅ Deep Dive Analysis: Dimension distributions, temporal analysis
- ✅ Rankings: Top/Bottom performers, dimension leaders
- ✅ Export & Share: Download filtered results
- ✅ Running at: http://localhost:8501

---

## 📊 Current State

### Analyzed Ads
- **Total:** 93 ads (as of Dec 22, 2025)
- **Hungarian:** 7 (100% language detection ✅)
- **Cannes:** 83 international campaigns
- **Recent additions:** 3 new ads (Apple AirPods, Squarespace, Magnum)
- **Average:** 66.5/100 overall
- **Most common score:** 65/100 (11.7% of ads)

### File Structure

```
responsible-advertising-index/
├── simple_pipeline.py          # ⭐ Main analysis tool
├── video_processor.py          # Gemini AI engine
├── ad_scrapers.py             # Video downloaders
├── dashboard_enhanced.py       # ⭐ PRODUCTION Dashboard (full features)
├── dashboard_new.py           # Simplified dashboard (legacy)
├── analysis_storage/          # 93 analyzed ads
│   └── <ad_id>/
│       ├── video.mp4
│       └── metadata.json
├── new_ads_2025-12-22/        # Latest 3 ads for review
├── INVESTOR_PITCH.md          # Comprehensive investor document
├── archive/                   # Old code (archived)
└── dashboard/                 # Old dashboard (legacy)
```

### Key Files

**Core Scripts:**
- `simple_pipeline.py` - Analyze URLs or batches
- `dashboard_enhanced.py` - **PRODUCTION** dashboard with full features
- `dashboard_new.py` - Simplified dashboard (legacy)
- `check_progress.sh` - Monitor batch processing
- `run_overnight.sh` - Process 200+ ads

**Catalogs:**
- `hungarian_ad_catalog.csv` - 47 Hungarian ads
- `cannes_youtube_only.csv` - 227 downloadable Cannes ads

**Documentation:**
- `README.md` - Quick start guide
- `ANALYSIS_SUMMARY.md` - Complete findings
- `OVERNIGHT_RUN_REPORT.md` - Batch results
- `INVESTOR_PITCH.md` - **NEW** Comprehensive investor document
- `PROJECT_STATUS.md` - This file

---

## 🚀 How to Use

### View Dashboard

```bash
streamlit run dashboard_enhanced.py
# Opens at http://localhost:8501
```

**Features:**
- 📺 **Browse Ads** - Watch videos, see scores with radar charts, read transcripts
- 📊 **Analytics Dashboard** - Distribution charts, category comparisons, language breakdown
- 🔬 **Deep Dive Analysis** - Dimension distributions, temporal analysis
- 🏆 **Rankings** - Top/Bottom performers, climate/social/cultural/ethical leaders
- 📤 **Export & Share** - Download filtered results as CSV
- 🔍 **Advanced Filters** - Dimension score sliders, language, grade, category, brand search

### Analyze New Ads

```bash
# Single URL
python3 simple_pipeline.py url "https://youtube.com/..." "Brand" "Campaign"

# Batch processing
python3 simple_pipeline.py batch catalog.csv --start 0 --count 10

# Export results
python3 simple_pipeline.py export
```

### Load Data

```python
import pandas as pd
df = pd.read_csv('analysis_storage/all_results_20251205_090801.csv')
```

---

## 📈 Key Insights

### 1. Climate Responsibility Gap
- **Only 8%** of award-winning ads score 80+ on climate
- Average climate score: **23.7/100**
- Social responsibility (72/100) prioritized over sustainability
- **Climate scores show ceiling effect**: Max observed is 60/100, only 7 unique values

### 2. Hungarian vs Modern Campaigns
- Hungarian 1980s-90s ads: **51.3/100** average
- Modern Cannes campaigns: **~72/100** average
- **29% gap** reflects pre-sustainability era values

### 3. Social Excellence
- **73% of ads** score 80+ on social responsibility
- Diversity and inclusion highly valued by juries
- Authentic representation rewards creativity

### 4. Score Distribution Findings (Dec 2025)
- Most common score: **65/100** (11.7% of ads)
- Only **5.6%** score exactly 75 (less common than perceived)
- Recent non-Cannes ads: **20%** score exactly 75
- **Validation concern**: Some ads show identical dimension scores despite different content
  - Example: Burger King & Uber One both scored (60, 80, 90, 70)
  - Suggests potential template-based scoring and anchor bias

---

## 🎯 Next Steps

### 🔴 HIGH PRIORITY: Validation Study
**Issue:** Score clustering and potential template-based scoring identified
**Action needed:**
1. Manual review of 20-30 ads to establish baseline scores
2. Compare human expert scores vs AI scores
3. Identify systematic biases in AI scoring
4. Refine prompts to increase score variance and accuracy
5. Document validation methodology in separate report

**Timeline:** 2-4 weeks
**Resources needed:** Subject matter experts, €10K-15K budget
**See:** INVESTOR_PITCH.md Part 8.1 for detailed roadmap

### Medium Priority

**Retry Failed Downloads:**
148 ads failed to download (YouTube 403/removed). Some might work with retry:

```bash
# Check which failed
find analysis_storage -type d -empty

# Retry individually
python3 simple_pipeline.py url "<url>" "Brand" "Campaign"
```

**Expand Dataset:**
Add more campaigns for broader sample:

```bash
# Create CSV with: url, title
python3 simple_pipeline.py batch new_catalog.csv
```

**Dashboard Enhancements:**
- ✅ Export filtered results (DONE in dashboard_enhanced.py)
- Compare specific ads side-by-side
- Add dimension deep-dive views (partially done)
- Download individual analysis reports (PDF)

---

## 📁 What's in Archive

**Old Scripts** (30+ files):
- Multiple download attempts with different strategies
- Mapping/fixing scripts (no longer needed!)
- Test scripts

**Old Docs:**
- Historical troubleshooting guides
- Deprecated instructions
- Previous architecture attempts

**Why Archived:**
- Simple_pipeline.py solved all mapping problems
- Atomic storage eliminates need for complex scripts
- Keep for historical reference only

---

## 🔧 Maintenance

### Update Dashboard

If you modify `dashboard_enhanced.py`:

```bash
# Restart dashboard
pkill -f "streamlit run dashboard_enhanced.py"
streamlit run dashboard_enhanced.py
```

### Clean Up Storage

Remove analysis errors (0-score ads):

```python
# In Python
import pandas as pd
df = pd.read_csv('analysis_storage/all_results_*.csv')
errors = df[df['overall_score'] == 0]
# Review and delete folders if needed
```

### Sync with GitHub

```bash
git add dashboard_enhanced.py PROJECT_STATUS.md INVESTOR_PITCH.md
git commit -m "Update dashboard and documentation"
git push
```

---

## 📊 Export Current Data

```bash
# Export to CSV
python3 simple_pipeline.py export

# Output: analysis_storage/all_results_YYYYMMDD_HHMMSS.csv

# View in terminal
cat analysis_storage/all_results_20251205_090801.csv | head -20

# Load in Python/pandas
# Load in Excel/Numbers
# Load in Google Sheets
```

---

## ✅ Production Checklist

- [x] Core analysis pipeline working
- [x] Language detection accurate (100%)
- [x] Dashboard with video playback
- [x] Advanced filters and search functional
- [x] Data exported and accessible
- [x] Documentation complete
- [x] GitHub synced
- [x] Old code archived
- [x] Project organized and clean
- [x] Investor pitch document created
- [ ] **PENDING:** Validation study to address score clustering
- [ ] **PENDING:** Scoring methodology refinement

---

## 🎉 Success Metrics

| Metric | Status |
|--------|--------|
| Ads analyzed | 93 ✅ |
| Hungarian detection | 100% ✅ |
| Dashboard working | Enhanced ✅ |
| GitHub synced | Yes ✅ |
| Documentation | Complete ✅ |
| Project organized | Clean ✅ |
| Video playback | Working ✅ |
| Advanced filters | Functional ✅ |
| Investor pitch | Created ✅ |
| Score validation | **Needed ⚠️** |

---

## 📝 Notes

**Storage:** `analysis_storage/` contains ~500MB of video files (not in git)

**Dashboard:** Use `dashboard_enhanced.py` for full features. Old `dashboard/` and `dashboard_new.py` kept for reference.

**Archive:** `archive/` contains all old attempts (git-tracked for history)

**CSV Export:** Latest at `analysis_storage/all_results_20251205_090801.csv`

**New Ads (Dec 22):** `new_ads_2025-12-22/` contains latest 3 analyzed ads for easy viewing

**Investor Materials:** See `INVESTOR_PITCH.md` for comprehensive project overview and investment case

---

## 🚨 Current Status Summary

**Project is production-ready with validation needed! 🚀⚠️**

**Dashboard running at:** http://localhost:8501
**GitHub:** https://github.com/uxjulie-climate/responsible-advertising-index
**93 ads analyzed and ready for insights**

**Next critical step:** Validation study to address score clustering (see INVESTOR_PITCH.md Part 8.1)

**Latest update:** December 22, 2025
- Added 3 new ads (Apple, Squarespace, Magnum)
- Identified score clustering issue requiring validation
- Created comprehensive investor pitch document
- Enhanced dashboard with full feature set

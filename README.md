# Responsible Advertising Index (RAI)

AI-powered assessment tool that evaluates advertising content across four responsibility dimensions: Climate, Social, Cultural, and Ethical.

**Status:** 🟡 **Research Phase** - Directional insights, validation in progress

---

## 🚀 Quick Start

```bash
# Clone repository
git clone https://github.com/uxjulie-climate/responsible-advertising-index
cd responsible-advertising-index

# Install dependencies
pip3 install -r requirements.txt

# Set up API key (one-time)
echo "GOOGLE_API_KEY=your_key_here" > .env

# Run main analysis app
./start.sh

# Or run submission form
./start_submit_form.sh
```

Get your free Google AI API key at: https://aistudio.google.com/app/apikey

---

## 📊 What It Does

Analyzes advertisements (images and videos) using Google Gemini 2.5 Flash across four dimensions:

1. **🌍 Climate Responsibility** - Sustainability messaging and greenwashing detection
2. **👥 Social Responsibility** - Diversity, inclusion, stereotype avoidance
3. **🎨 Cultural Sensitivity** - Respectful representation and local awareness
4. **✨ Ethical Communication** - Transparency and truthfulness

Each ad receives:
- Scores (0-100) for each dimension
- Overall responsibility score
- Detailed findings with evidence
- Actionable recommendations
- Exportable PDF/Excel reports
- Bilingual output (English/Hungarian)

---

## ✨ Features

### Current Features (v1.0)

**Analysis:**
- ✅ Image ad analysis (PNG, JPG, JPEG, WEBP)
- ✅ Video ad analysis (MP4, MOV, AVI, WEBM) - up to 3 minutes
- ✅ Text + visual multimodal analysis
- ✅ Bilingual support (English/Hungarian)
- ✅ Scene-by-scene video breakdown
- ✅ Temporal analysis (how messaging evolves)

**Submission:**
- ✅ File upload (images and videos)
- ✅ URL submission (YouTube, LinkedIn, direct links) ⭐ NEW
- ✅ Public submission form for stakeholders
- ✅ Batch comparison mode

**Output:**
- ✅ Interactive radar charts and gauges
- ✅ PDF reports with visualizations
- ✅ Excel exports for data analysis
- ✅ JSON for API integration
- ✅ Side-by-side ad comparison

**Examples:**
- ✅ Built-in sample ads (excellent, problematic, mixed)
- ✅ Hungarian language examples
- ✅ One-click example loading

---

## 🎯 Current Status

**Phase:** Research & Validation
- ✅ Working prototype with Streamlit UI
- ✅ Google Gemini AI integration
- ✅ Video analysis capability
- ✅ Submission form for stakeholders
- ⏳ Expert validation studies (6 months)
- ⏳ Industry benchmarking
- ⏳ Public leaderboard (planned)

**Confidence Levels:**
- Direction (good vs. bad ads): 🟢 HIGH
- Relative ranking: 🟡 MEDIUM
- Exact scores: 🔴 LOW (validation in progress)

See: `docs/CONFIDENCE_EXECUTIVE_SUMMARY.md` for details

---

## 📁 Project Structure

```
responsible-advertising-index/
├── app.py                       # Main analysis application
├── submit_ad.py                 # Public submission form ⭐ NEW
├── config.py                    # Video configuration
├── video_processor.py           # Video analysis engine
├── video_utils.py               # Video validation
├── ad_scrapers.py               # Download utilities
├── download_ads.py              # Ad downloader CLI
├── start.sh                     # Quick start script
├── start_submit_form.sh         # Submission form launcher ⭐ NEW
├── requirements.txt             # Python dependencies
├── .env                         # API key (not in git)
├── docs/                        # Documentation
│   ├── STAKEHOLDER_RESPONSE_SUMMARY.md  # Quick answers
│   ├── METHODOLOGY_AND_VALIDATION.md    # Technical details
│   ├── CONFIDENCE_QUICK_REFERENCE.md    # Confidence levels
│   ├── URL_SUBMISSION_FEATURE.md        # URL submission guide ⭐ NEW
│   ├── SARCASM_TEST_GUIDE.md            # Testing irony detection
│   └── archive/                         # Archived planning docs
├── demo_samples/                # Demo materials
│   ├── DEMO_SCRIPT.md           # Presentation guide
│   ├── excellent_*.json         # Sample excellent ad report
│   ├── problematic_*.json       # Sample problematic ad report
│   └── mixed_*.json             # Sample mixed ad report
└── submissions/                 # Submission queue (not in git)
```

---

## 🔑 Setup

### 1. Get API Key
Get your free Google AI API key: https://aistudio.google.com/app/apikey

### 2. Install Dependencies
```bash
pip3 install -r requirements.txt
```

### 3. Configure API Key

**Option A: Secure (Recommended)**
```bash
echo "GOOGLE_API_KEY=your_key_here" > .env
```

**Option B: Manual Entry**
- Run app and paste key when prompted
- Key is requested each time

### 4. Run Application

**Main Analysis App:**
```bash
./start.sh
```

**Submission Form:**
```bash
./start_submit_form.sh
```

**Manual Start:**
```bash
python3 -m streamlit run app.py          # Main app
python3 -m streamlit run submit_ad.py    # Submission form
```

### 5. Try It Out
- Click "Example Ads" buttons to test
- Or upload your own ad (image or video)
- Or submit via URL (YouTube, etc.) ⭐ NEW

---

## 📖 Documentation

### Getting Started
- **START_HERE.md** - Project overview
- **QUICK_START.md** - Setup walkthrough
- **MAC_QUICKSTART.md** - Mac-specific instructions

### For Stakeholders
- **docs/STAKEHOLDER_RESPONSE_SUMMARY.md** - Answers to key questions
- **docs/STAKEHOLDER_REQUIREMENTS.md** - Features, costs, roadmap
- **docs/CONFIDENCE_EXECUTIVE_SUMMARY.md** - Validation status

### Features & How-To
- **docs/URL_SUBMISSION_FEATURE.md** - Submit ads via URL ⭐ NEW
- **docs/SARCASM_TEST_GUIDE.md** - Testing irony/satire detection
- **docs/HUNGARIAN_SUPPORT.md** - Bilingual functionality
- **docs/DOWNLOAD_ADS_GUIDE.md** - Download ads from platforms

### Methodology
- **docs/METHODOLOGY_AND_VALIDATION.md** - Full technical methodology
- **docs/CONFIDENCE_QUICK_REFERENCE.md** - One-page confidence guide
- **demo_samples/DEMO_SCRIPT.md** - Presentation guide

### Reference
- **docs/CHEATSHEET.md** - Quick command reference
- **docs/SAMPLE_AD_COPY.md** - Example ad text
- **docs/GCP_SETUP_STATUS.md** - Cloud setup (complete)

---

## 🛠️ Tech Stack

- **AI**: Google Gemini 2.5 Flash (multimodal vision + video)
- **Backend**: Python + Streamlit
- **Cloud**: Google Cloud Storage (for large videos)
- **Visualization**: Plotly (radar charts, gauges)
- **Export**: ReportLab (PDF), Pandas (Excel)
- **Video**: OpenCV, MoviePy, FFmpeg

---

## 💡 Use Cases

### 1. Internal Assessment
Analyze your own ads before publishing to identify potential issues.

### 2. Competitive Benchmarking
Compare your ads against competitors (submit their URLs).

### 3. Pre-Launch Review
Get feedback on draft campaigns before going live.

### 4. Industry Research
Analyze trends in responsible advertising across sectors.

### 5. Client Reporting
Generate professional PDF reports for clients.

---

## 🎬 How to Use

### Main Analysis App

1. **Run:** `./start.sh`
2. **Choose tab:**
   - **Image Analysis** - Upload image ads
   - **Video Analysis** - Upload video ads (up to 3 min)
   - **Compare Ads** - Side-by-side comparison
   - **Export Data** - Download results
3. **Try examples** - Click example ad buttons
4. **Upload your own** - Drag & drop or browse
5. **Add context** - Paste ad copy text (optional)
6. **Analyze** - Click "Analyze Ad"
7. **Review results** - Scores, findings, recommendations
8. **Export** - Download PDF/Excel reports

### Submission Form

1. **Run:** `./start_submit_form.sh`
2. **Fill form:**
   - Your contact info
   - Advertiser/brand name
   - **Choose:** Upload file OR share URL ⭐
   - Ad context (tone, intent)
   - Privacy settings
3. **Submit** - Ad queued for analysis
4. **Receive email** - Results sent to your email

---

## 📈 Roadmap

### ✅ Phase 1: Prototype (Complete)
- Working Streamlit interface
- Image and video analysis
- Bilingual support
- Export functionality

### 🔄 Phase 2: Validation (In Progress - 6 months)
- Expert panel studies (€20-30K)
- Industry benchmarking (€30-50K)
- Academic peer review
- Establish accuracy metrics

### 🔜 Phase 3: Platform (3-6 months)
- Automated submission processing
- User authentication
- Ad storage database
- Public/private leaderboards
- API access

### 🔮 Phase 4: Scale (6-12 months)
- Large-scale analysis
- Annual benchmark reports
- Certification program ("RAI Verified" badges)
- Browser extension
- Real-time monitoring

---

## 💰 Costs

### Current (Research Phase)
- **Analysis:** Free (research phase)
- **API costs:** ~€0.02 per image, ~€0.50 per video minute
- **Hosting:** Local (€0)

### Future (Production)
See `docs/STAKEHOLDER_REQUIREMENTS.md` for detailed breakdown:
- **Development:** €15K-136K (depending on scope)
- **Operations:** €125-800/month (depending on scale)
- **Revenue models:** Freemium, pay-per-use, certification

---

## 🔒 Security & Privacy

- ✅ API keys stored in `.env` (not committed to git)
- ✅ Submissions directory excluded from git
- ✅ User data privacy settings honored
- ✅ No data shared without permission
- ✅ GCP authentication configured
- ⚠️ **Important:** Don't commit `.env` or `submissions/` to public repos

---

## ⚠️ Important Notes

### This is a Research Tool

**What it IS:**
- ✅ Directional insights tool
- ✅ Red flag detector
- ✅ Best practice identifier
- ✅ Internal assessment aid

**What it's NOT:**
- ❌ Regulatory compliance tool
- ❌ Replacement for human judgment
- ❌ Definitive scoring system (yet)
- ❌ Ready for public brand rankings

**Use with expert review for important decisions.**

See: `docs/CONFIDENCE_EXECUTIVE_SUMMARY.md` for full transparency

---

## 🤝 Contributing

This project is in active development for research and validation.

**Questions?** Contact the project team.

**Found a bug?** Open an issue on GitHub.

**Want to collaborate?** See `docs/STAKEHOLDER_REQUIREMENTS.md` for partnership opportunities.

---

## 📄 License

[To be determined]

---

## 🙏 Credits

Built with:
- Google Gemini AI (vision + video analysis)
- Streamlit (UI framework)
- Claude Code (development assistance)
- Community feedback and testing

---

## 🔗 Links

- **GitHub:** https://github.com/uxjulie-climate/responsible-advertising-index
- **Google AI Studio:** https://aistudio.google.com/app/apikey
- **Documentation:** See `docs/` directory

---

**Ready to analyze ads responsibly?** 🌍

```bash
./start.sh
```

**Want to submit ads for analysis?** 📊

```bash
./start_submit_form.sh
```

---

**Version:** 1.0 (Research Phase)
**Last Updated:** January 13, 2025

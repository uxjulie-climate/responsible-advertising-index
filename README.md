# Responsible Advertising Index (RAI)

AI-powered assessment tool that evaluates advertising content across four responsibility dimensions: Climate, Social, Cultural, and Ethical.

## 🚀 Quick Start

```bash
# Install dependencies
pip3 install -r requirements.txt

# Run the demo
streamlit run app.py
```

Get your free Google AI API key at: https://makersuite.google.com/app/apikey

## 📊 What It Does

Analyzes advertisements using Google Gemini 2.5 Flash across four dimensions:

1. **Climate Responsibility** - Sustainability messaging and greenwashing detection
2. **Social Responsibility** - Diversity, inclusion, stereotype avoidance
3. **Cultural Sensitivity** - Respectful representation and local awareness
4. **Ethical Communication** - Transparency and truthfulness

Each ad receives:
- Scores (0-100) for each dimension
- Overall responsibility score
- Detailed findings with evidence
- Recommendations for improvement
- Exportable PDF/Excel reports

## 🎯 Current Status

**Phase 1: Telekom Demo** - Complete working prototype
- ✅ Streamlit web interface
- ✅ Google Gemini AI integration
- ✅ 4-dimension scoring framework
- ✅ Radar chart visualizations
- ✅ PDF/Excel export
- ✅ Multi-ad comparison
- ✅ Built-in example ads

## 📁 Project Structure

```
responsible-advertising-index/
├── app.py                    # Main Streamlit application
├── requirements.txt          # Python dependencies
├── CLAUDE.md                 # AI assistant guidance
├── .claude/commands/         # Custom Claude Code commands
├── docs/                     # Comprehensive documentation
│   ├── DEMO_GUIDE.md        # Presentation guide
│   ├── CHEATSHEET.md        # Quick reference
│   └── SAMPLE_AD_COPY.md    # Example ads
└── .gitignore               # Protects API keys
```

## 🔑 Setup

1. **Get API Key** (free): https://makersuite.google.com/app/apikey
2. **Install dependencies**: `pip3 install -r requirements.txt`
3. **Run app**: `streamlit run app.py`
4. **Paste API key** in sidebar when app opens
5. **Try example ads** or upload your own

## 📖 Documentation

- **CLAUDE.md** - Complete technical documentation and architecture
- **SETUP_SUMMARY.md** - Quick setup guide
- **docs/DEMO_GUIDE.md** - How to present the demo
- **docs/CHEATSHEET.md** - Demo day talking points
- **docs/SAMPLE_AD_COPY.md** - Example advertisements for testing

## 🛠️ Tech Stack

- **AI**: Google Gemini 2.5 Flash (multimodal vision API)
- **Backend**: Python + Streamlit
- **Visualization**: Plotly (radar charts, gauges)
- **Export**: ReportLab (PDF), Pandas (Excel)
- **Future**: Vertex AI for production (using Google Cloud credits)

## 🎬 Demo Features

- Upload ad images (PNG, JPG, JPEG)
- Multimodal analysis (image + text)
- Real-time scoring across 4 dimensions
- Interactive radar charts
- Detailed findings per dimension
- Export individual reports (PDF)
- Compare multiple ads (Excel/PDF)
- Analysis history tracking

## 📈 Roadmap

### Phase 1: Demo (Complete ✅)
- Working Streamlit prototype
- Gemini integration
- Basic scoring framework

### Phase 2: MVP (3 months)
- Automated ad library scraping
- Video analysis capability
- Validated scoring datasets
- Brand comparison features

### Phase 3: Index Launch (6-12 months)
- Large-scale analysis
- Annual benchmark reports
- Public API
- Advanced analytics dashboard

## 🔒 Security

- API keys protected via `.gitignore`
- No keys committed to repository
- Environment variables for production

## 🤝 Contributing

This is a working demo for the Telekom presentation. For questions or contributions, contact the project team.

## 📄 License

[To be determined]

## 🙏 Credits

Built with:
- Google Gemini AI
- Streamlit
- Claude Code for development assistance

---

**Ready to analyze ads responsibly?** 🌍

View the live project: https://github.com/uxjulie-climate/responsible-advertising-index

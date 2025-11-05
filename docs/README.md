# Responsible Advertising Index - Demo (Gemini Version)

A Streamlit-based demo powered by **Google Gemini** that uses AI to evaluate advertisements across four responsibility dimensions.

## 🚀 Quick Start

### Step 1: Install Dependencies

```bash
# On Mac/Linux:
pip3 install -r requirements.txt

# On Windows:
pip install -r requirements.txt
```

### Step 2: Get Your Free Google AI API Key

1. Go to [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Sign in with your Google account
3. Click "Create API Key"
4. Copy the API key

**Note:** This is FREE and gives you generous quota for testing!

### Step 3: Run the App

```bash
streamlit run app.py
```

### Step 4: Use the App

1. Browser opens automatically (usually http://localhost:8501)
2. Paste your Google AI API key in the sidebar
3. Upload an ad image
4. Paste the ad copy
5. Click "Analyze"

## 💰 Using Your Google Cloud Credits

This version uses the **free Google AI API** which is perfect for demos and testing.

**To use your Google Cloud startup credits instead:**

You'll want to use **Vertex AI** (Google Cloud's enterprise AI platform). See the separate guide: `VERTEX_AI_SETUP.md`

### Why Two Options?

- **Google AI API (this version)**: Free, easy setup, perfect for demos
- **Vertex AI (Cloud credits)**: Enterprise version, uses your GCP credits, requires more setup

Start with this free version for your demo, then switch to Vertex AI for production!

## 📊 What It Does

Analyzes advertisements across four dimensions:
1. **Climate Responsibility** - Sustainability messaging and greenwashing detection
2. **Social Responsibility** - Diversity, inclusion, stereotype avoidance
3. **Cultural Sensitivity** - Respectful representation and local awareness
4. **Ethical Communication** - Transparency and truthfulness

## 🎯 Demo Strategy

Use 5 sample ads that demonstrate range:
1. Excellent (85-95 score) - Authentic sustainability + diversity
2. Good (70-85) - Strong on some dimensions
3. Mixed (60-75) - Good visually, weak on substance
4. Problematic (40-60) - Greenwashing or stereotypes
5. Poor (30-50) - Multiple issues

See `SAMPLE_AD_COPY.md` for examples!

## 📁 Files

- `app.py` - Main Streamlit application (Gemini-powered)
- `requirements.txt` - Python dependencies
- `README.md` - This file
- `SAMPLE_AD_COPY.md` - Example ad copy for testing
- `DEMO_GUIDE.md` - Complete demo guide
- `VERTEX_AI_SETUP.md` - How to use Google Cloud credits

## 🔑 API Key & Costs

### Free Tier (Google AI API):
- **Cost:** FREE
- **Quota:** 60 requests per minute
- **Best for:** Demos, testing, development
- **Get key:** https://makersuite.google.com/app/apikey

### Paid Tier (Vertex AI with your Google Cloud credits):
- **Cost:** ~$0.01-0.02 per ad (from your startup credits)
- **Quota:** Much higher
- **Best for:** Production, high volume
- **Setup:** See VERTEX_AI_SETUP.md

## ⚡ Performance

- Analysis takes 10-30 seconds per ad
- Requires internet connection (API calls)
- Works best with high-quality images
- Supports PNG, JPEG formats

## 🔧 Troubleshooting

**"Module not found" error:**
```bash
pip3 install --upgrade -r requirements.txt
```

**API key error:**
- Make sure you copied the entire key
- Get a new key at https://makersuite.google.com/app/apikey
- Check you're signed in with the correct Google account

**Slow analysis:**
- Normal for first request
- Check internet speed
- Try smaller image files

**Rate limit error:**
- Free tier: 60 requests/minute
- Wait a minute and try again
- Or upgrade to Vertex AI for higher limits

## 🆚 Gemini vs Claude

Both work great! Here's the comparison:

| Feature | Gemini (this version) | Claude (original) |
|---------|----------------------|-------------------|
| **API Cost** | FREE (then ~$0.01/ad) | ~$0.05-0.10/ad |
| **Your Credits** | ✅ Can use GCP credits | ❌ Separate billing |
| **Setup** | ✅ Easiest | Medium |
| **Quality** | Excellent | Excellent |
| **Speed** | Fast | Fast |

**Recommendation:** Use this Gemini version! It's free for testing and can use your Google Cloud credits in production.

## 📈 Future Enhancements

- Video analysis
- Batch processing
- Historical tracking
- Competitor comparison
- PDF report export
- Industry benchmarks
- Integration with Vertex AI for production

## 🎓 Learn More

- **Framework details:** See DEMO_GUIDE.md
- **Sample ads:** See SAMPLE_AD_COPY.md
- **Architecture:** See ARCHITECTURE.md (from original package)
- **Google Cloud setup:** See VERTEX_AI_SETUP.md

## 📞 Support

- **Google AI Studio:** https://ai.google.dev/
- **API Documentation:** https://ai.google.dev/docs
- **Gemini API:** https://ai.google.dev/tutorials/python_quickstart

---

**Ready to start?** Just run:
```bash
pip3 install -r requirements.txt
streamlit run app.py
```

Then get your free API key at: https://makersuite.google.com/app/apikey

🎉 You're all set!

# Setup Telekom Demo

**IMPORTANT**: A working Streamlit demo already exists at `/Users/julieschiller/Downloads/rai_demo_gemini/`

This command helps you set up and prepare the existing demo for your Telekom presentation.

## Step 1: Copy Demo Files to Project

Copy the working demo from Downloads into this project:

```bash
# Copy main app
cp /Users/julieschiller/Downloads/rai_demo_gemini/app.py /Users/julieschiller/responsible-advertising-index/

# Copy requirements
cp /Users/julieschiller/Downloads/rai_demo_gemini/requirements.txt /Users/julieschiller/responsible-advertising-index/

# Copy documentation for reference
mkdir -p /Users/julieschiller/responsible-advertising-index/docs
cp /Users/julieschiller/Downloads/rai_demo_gemini/*.md /Users/julieschiller/responsible-advertising-index/docs/
```

## Step 2: Install Dependencies

```bash
cd /Users/julieschiller/responsible-advertising-index
pip3 install -r requirements.txt
```

Dependencies:
- streamlit >= 1.28.0
- google-generativeai >= 0.7.0
- pillow == 10.2.0
- plotly == 5.18.0
- reportlab == 4.0.7
- matplotlib == 3.8.2
- pandas >= 2.0.0
- openpyxl >= 3.1.0

## Step 3: Get Google AI API Key

1. Go to https://makersuite.google.com/app/apikey
2. Sign in with Google account
3. Click "Create API Key"
4. Copy the key (keep it secure)

**Note**: This is FREE for testing (no credit card required)

## Step 4: Test the Demo

```bash
# Run the app
streamlit run app.py

# Browser opens automatically at http://localhost:8501
```

In the app:
1. Paste your Google AI API key in the sidebar
2. Click one of the example ads (Excellent, Problematic, or Mixed)
3. Click "Analyze Advertisement"
4. Wait 10-30 seconds for results
5. Review the scores and findings

## Step 5: Prepare Telekom Ads

For your actual demo, prepare 3 Telekom advertisements:

1. **Collect materials**:
   - Get ad images (PNG/JPG format)
   - Copy the ad copy text (headlines, body text, taglines)

2. **Pre-test before demo**:
   - Upload each Telekom ad
   - Run analysis
   - Note the scores
   - Screenshot the results (backup in case of internet issues)

3. **Expected analysis time**: 10-30 seconds per ad

## Step 6: Demo Preparation Checklist

- [ ] App installed and tested with example ads
- [ ] Google AI API key obtained and working
- [ ] 3 Telekom ads prepared (images + copy text)
- [ ] Telekom ads pre-analyzed and screenshots taken
- [ ] Read `docs/CHEATSHEET.md` for talking points
- [ ] Read `docs/DEMO_GUIDE.md` for presentation tips
- [ ] Internet connection verified
- [ ] Backup plan: screenshots ready in case of API issues

## What the Demo Provides

✅ **Already working features**:
- Upload ad images (PNG, JPG, JPEG)
- Paste ad copy text
- AI analysis via Google Gemini 2.5 Flash
- 4-dimension scoring (Climate, Social, Cultural, Ethical)
- Radar chart visualization
- Overall score with gauge
- Detailed findings per dimension
- PDF report export
- Multi-ad comparison
- Excel export for comparisons
- Analysis history tracking
- Built-in example ads

## Troubleshooting

**"Module not found" error:**
```bash
pip3 install --upgrade -r requirements.txt
```

**API key not working:**
- Verify you copied the entire key
- Generate a new key at https://makersuite.google.com/app/apikey
- Check you're signed into the correct Google account

**Slow analysis:**
- Normal for first request (model initialization)
- Check internet connection
- Try with smaller images if issues persist

**During demo - internet fails:**
- Use your pre-captured screenshots
- Explain: "This is a live API demo - here's what the results look like"

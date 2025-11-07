# Quick Start Guide

## ✅ Your Setup is Complete!

---

## 1. Start the App

```bash
cd /Users/julieschiller/responsible-advertising-index
./start.sh
```

The app will:
- ✅ Auto-open in your browser
- ✅ **Auto-load your API key** (no need to paste it!)
- ✅ Show all 4 tabs (Image, Video, Compare, Export)

---

## 2. API Key (Automatic!)

Your API key is now stored in `.env` and will **automatically load** when you start the app!

**File:** `.env` (already created, not committed to git)
```
GOOGLE_API_KEY=AIzaSyA_SIvs6tGlusHJ_82CaPfiHJp50ySsSCQ
```

**You don't need to paste it anymore!** 🎉

---

## 3. Download Video Ads

### For Your LinkedIn Ad Example

**URL:** https://www.linkedin.com/ad-library/detail/946953156

#### Quick Method (Browser):
1. Visit the URL in browser
2. Log in to LinkedIn
3. Open DevTools (F12 or Cmd+Option+I)
4. Go to **Network** tab
5. Filter by "mp4"
6. Play the video
7. Find the video URL in network requests
8. Right-click → Open in new tab
9. Right-click video → Save As → `linkedin_ad.mp4`
10. Upload to RAI

#### For Testing (Use YouTube Instead):
```bash
# Install yt-dlp (one time)
pip3 install yt-dlp

# Download any YouTube ad
yt-dlp "https://www.youtube.com/watch?v=VIDEO_ID" -o "test_ad.mp4"

# Example: Search "telekom commercial 2024" on YouTube
```

---

## 4. Analyze Video

1. Start app: `./start.sh`
2. Go to **"📹 Video Analysis"** tab
3. Upload video (MP4, MOV, AVI, WebM)
4. Enter brand name (optional)
5. Click **"🎬 Analyze Video"**
6. Wait 10-60 seconds
7. View results!

---

## 5. What You'll Get

### Analysis Includes:
- ✅ Overall score (0-100)
- ✅ 4-dimension scores (Climate, Social, Cultural, Ethical)
- ✅ **Full video transcript** with timestamps
- ✅ **Scene-by-scene breakdown** (3-5 scenes)
- ✅ **Temporal analysis** (how messaging evolves)
- ✅ **Key moments** timeline
- ✅ **Audio-visual alignment** check
- ✅ Detailed findings per dimension
- ✅ Strengths, concerns, recommendations
- ✅ **Bilingual** (English/Hungarian if detected)

---

## 6. Cost

- **Per video:** ~$0.01-0.02
- **100 test videos:** ~$2
- **Your $10k credits:** 500,000 videos

**Cost is NOT a concern!** 🎉

---

## Files Created

### Configuration
- ✅ `.env` - API key storage (secure, not in git)
- ✅ `start.sh` - One-command startup script

### Video Analysis
- ✅ `config.py` - Video settings
- ✅ `video_utils.py` - Validation utilities
- ✅ `video_processor.py` - VideoAnalyzer class
- ✅ `ad_scrapers.py` - Video download utilities

### Documentation
- ✅ `docs/VIDEO_READY.md` - Complete testing guide
- ✅ `docs/VIDEO_AD_SCRAPING.md` - How to get videos
- ✅ `docs/QUICK_START.md` - This file!

---

## Troubleshooting

### App won't start
```bash
# Make sure you're in the right directory
cd /Users/julieschiller/responsible-advertising-index

# Try manual start
python3 -m streamlit run app.py
```

### API key not loading
Check that `.env` file exists:
```bash
cat .env
# Should show: GOOGLE_API_KEY=AIza...
```

### Can't download LinkedIn video
LinkedIn requires manual download (see section 3 above).
**Easier option:** Test with YouTube videos first!

### Video upload fails
- Check file size (<200MB)
- Check duration (<3 minutes)
- Try converting to MP4 if other format

---

## Next Steps

### Immediate Testing
1. ✅ Start app with `./start.sh`
2. ✅ Verify API key auto-loads
3. ⬜ Download a test video (YouTube recommended)
4. ⬜ Upload to Video Analysis tab
5. ⬜ Analyze and review results

### This Week
1. ⬜ Download 5-10 sample ads
2. ⬜ Test with different types (fashion, tech, food)
3. ⬜ Test Hungarian language support
4. ⬜ Validate accuracy of analysis

### Future Enhancements
- ⬜ Automate LinkedIn ad downloads (Playwright)
- ⬜ Batch video processing
- ⬜ URL input field in UI
- ⬜ Video comparison mode
- ⬜ Timeline visualization chart

---

## Support

Need help? Check these docs:
- **VIDEO_READY.md** - Complete video analysis guide
- **VIDEO_AD_SCRAPING.md** - Detailed scraping instructions
- **GCP_SETUP_STATUS.md** - Cloud infrastructure status

---

**You're all set! 🚀**

Run `./start.sh` and start analyzing video ads!

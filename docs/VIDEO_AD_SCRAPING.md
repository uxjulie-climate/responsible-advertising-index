# Video Ad Scraping Guide

**How to get video ads from various platforms for analysis**

---

## Quick Summary

### ✅ Automated (Easy)
- **YouTube** - Use `yt-dlp`
- **Direct URLs** - Just download

### ⚠️ Manual Required (Protected Content)
- **LinkedIn Ad Library** - Right-click → Save
- **Meta Ad Library** - Browser DevTools method
- **Google Ads Transparency** - Right-click → Save

---

## Option 1: LinkedIn Ad Library (Your Example)

**URL:** https://www.linkedin.com/ad-library/detail/946953156

### Method A: Manual Download (Easiest)
1. Visit the ad URL in your browser
2. **Log in to LinkedIn** (required to view ads)
3. Play the video
4. Right-click on the video
5. Select "Save Video As..."
6. Save as MP4
7. Upload to RAI

### Method B: Browser DevTools (If right-click disabled)
1. Visit the ad URL
2. Open Developer Tools (F12 or Cmd+Option+I on Mac)
3. Go to **Network** tab
4. Filter by "mp4" or "video"
5. Play the video
6. Look for the video URL in the network requests
7. Right-click the video URL → "Open in new tab"
8. Right-click the video → "Save Video As..."

### Method C: Browser Extension
Install: **Video DownloadHelper** (Firefox/Chrome)
- Visit ad page
- Click extension icon
- Select video quality
- Download

**Limitation:** LinkedIn requires authentication, so automated scraping is difficult.

---

## Option 2: Meta Ad Library (Facebook/Instagram)

**URL:** https://www.facebook.com/ads/library/?id=XXXXXXXXX

### Manual Download Method
1. Visit the ad library URL
2. Click on the ad to view it
3. Open Developer Tools (F12)
4. Go to **Network** tab
5. Filter by "mp4"
6. Play the video
7. Find the .mp4 URL in network requests
8. Right-click → Copy URL
9. Paste URL in new tab
10. Right-click video → Save

### Alternative: Use Meta API (Advanced)
- Requires Facebook Developer account
- Need to apply for Ad Library API access
- Can programmatically download ads
- Documentation: https://developers.facebook.com/docs/ad-library-api

---

## Option 3: YouTube (Automated!) ✅

**Best option for testing**

### Install yt-dlp
```bash
pip install yt-dlp
```

### Download Video Ads
```bash
# Download any YouTube video
yt-dlp "https://www.youtube.com/watch?v=VIDEO_ID" -o "ad.mp4"

# Download with quality limit (720p max)
yt-dlp "https://www.youtube.com/watch?v=VIDEO_ID" -f "best[height<=720]" -o "ad.mp4"
```

### Find YouTube Ads
Search YouTube for:
- "telekom commercial 2024"
- "sustainable fashion ad"
- "electric vehicle commercial"
- "brand name + advertisement"

**Advantage:** Fully automated, no manual steps!

---

## Option 4: Google Ads Transparency Center

**URL:** https://adstransparency.google.com/

### Manual Download
1. Visit the transparency center
2. Search for advertiser (e.g., "Telekom")
3. Click on a video ad
4. Right-click → "Save Video As..."

---

## Option 5: Direct Video URLs

If you have a direct link to a video file:

```bash
# Using curl
curl -o ad.mp4 "https://example.com/video.mp4"

# Using wget
wget -O ad.mp4 "https://example.com/video.mp4"
```

---

## Using the Ad Scraper Tool

We've created `ad_scrapers.py` to help automate this:

### Test Platform Detection
```bash
python3 ad_scrapers.py "https://www.linkedin.com/ad-library/detail/946953156"
```

### Download from YouTube
```bash
python3 ad_scrapers.py "https://www.youtube.com/watch?v=XXXXXXXXX"
```

### Download from Direct URL
```bash
python3 ad_scrapers.py "https://example.com/video.mp4"
```

---

## Recommended Workflow for Your LinkedIn Ad

Since LinkedIn requires manual download, here's the best approach:

### Step-by-Step:
1. **Open the LinkedIn ad:**
   ```
   https://www.linkedin.com/ad-library/detail/946953156
   ```

2. **Log in to LinkedIn** (if not already)

3. **Use Browser DevTools Method:**
   - Open DevTools (F12)
   - Go to Network tab
   - Filter: "mp4"
   - Play the video
   - Find the video URL (looks like: `https://...linkedin.com/...video.mp4`)
   - Copy that URL

4. **Download the video:**
   ```bash
   curl -o linkedin_ad.mp4 "PASTE_VIDEO_URL_HERE"
   ```

5. **Upload to RAI:**
   - Open RAI demo: `./start.sh`
   - Go to "Video Analysis" tab
   - Upload `linkedin_ad.mp4`

---

## Automated Pipeline (Future Enhancement)

To fully automate LinkedIn/Meta ads, we'd need:

### Option A: Playwright/Selenium (Browser Automation)
```python
from playwright.sync_api import sync_playwright

def download_linkedin_ad(ad_url):
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()

        # Login to LinkedIn
        page.goto("https://www.linkedin.com/login")
        page.fill("#username", "your_email")
        page.fill("#password", "your_password")
        page.click("button[type='submit']")

        # Navigate to ad
        page.goto(ad_url)

        # Intercept video request
        video_url = None
        def handle_response(response):
            if ".mp4" in response.url:
                video_url = response.url

        page.on("response", handle_response)
        page.click("video")  # Play video

        # Download video_url
        ...
```

**Pros:** Can handle authenticated platforms
**Cons:** Requires LinkedIn credentials, fragile (breaks if UI changes)

### Option B: API Access (Best for Production)
- **LinkedIn Marketing API** - Requires partnership
- **Meta Marketing API** - Requires app approval
- **Google Ads API** - Requires developer account

**Pros:** Official, reliable, legal
**Cons:** Requires approval, may have usage limits

### Option C: Manual Upload Workflow (Current Best)
1. Use browser to download ads manually
2. Save to a folder
3. Batch upload to RAI
4. Analyze all at once

**Pros:** Simple, works now, no legal concerns
**Cons:** Manual effort

---

## Recommended Immediate Solution

For your LinkedIn ad example:

### Quick Test (Right Now)
1. Find a YouTube ad instead:
   - Search: "telekom commercial 2024"
   - Download with: `yt-dlp URL -o test_ad.mp4`
   - Upload to RAI

### For LinkedIn Ads (This Week)
1. Use browser DevTools method
2. Download 5-10 sample ads manually
3. Upload to RAI for testing
4. Validate the analysis quality

### For Production (Next Month)
1. Build Playwright automation
2. Or partner with ad platforms for API access
3. Create batch processing pipeline

---

## Ad Sources for Testing

### Free Ad Libraries (Manual Download)
- **Meta Ad Library:** https://www.facebook.com/ads/library/
- **Google Ads Transparency:** https://adstransparency.google.com/
- **LinkedIn Ad Library:** https://www.linkedin.com/ad-library/
- **TikTok Ad Library:** https://library.tiktok.com/

### YouTube Commercial Collections (Automated)
- Search: "[brand] commercial 2024"
- Channels that post ads
- AdWeek, AdAge compilations

### Stock Ad Footage (For Testing)
- Pexels.com (free)
- Pixabay.com (free)
- Add text overlays to simulate ads

---

## Cost Comparison

### Manual Approach
- **Time:** 2-3 minutes per ad
- **Cost:** $0
- **Effort:** High for large batches

### Automated Approach
- **Setup Time:** 1-2 weeks
- **Time per ad:** ~10 seconds
- **Cost:** Development time + API fees (if using official APIs)

---

## Next Steps

### Immediate (For Testing)
1. ✅ API key now auto-loads from `.env` file (done!)
2. ⬜ Download 3-5 YouTube ads with yt-dlp
3. ⬜ Test video analysis feature
4. ⬜ Validate results quality

### Short-Term (This Week)
1. ⬜ Manually download 10 LinkedIn ads via DevTools
2. ⬜ Batch analyze them
3. ⬜ Document any issues

### Long-Term (Production)
1. ⬜ Build Playwright automation for LinkedIn
2. ⬜ Apply for Meta Ad Library API access
3. ⬜ Create scheduled pipeline for new ads
4. ⬜ Database for storing analyzed ads

---

## Want Me to Build the Automation?

I can create:

**Option 1: Browser Automation Script**
- Uses Playwright
- Handles LinkedIn login
- Downloads ads automatically
- Requires your LinkedIn credentials (stored securely)

**Option 2: URL Input Feature in UI**
- Add URL field to video tab
- Detect platform
- Show download instructions
- Auto-download if possible (YouTube, direct URLs)

**Option 3: Batch Processing Tool**
- Give it a list of URLs
- Downloads all automatically (where possible)
- Provides manual instructions for others
- Analyzes all videos in batch

Which would be most useful?

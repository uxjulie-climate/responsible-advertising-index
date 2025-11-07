# How to Download Video Ads

## Quick Start

```bash
# Interactive mode - guides you through the process
python3 download_ads.py

# Direct download (YouTube)
python3 download_ads.py "https://youtube.com/watch?v=VIDEO_ID"

# Manual instructions (LinkedIn)
python3 download_ads.py "https://www.linkedin.com/ad-library/detail/946953156"

# See where to find ads
python3 download_ads.py search
```

---

## Method 1: YouTube (Automated) ✅

### Step 1: Find an ad on YouTube
Search for:
- "telekom commercial 2024"
- "sustainable fashion ad"
- "[brand] advertisement"

### Step 2: Copy the URL
Example: `https://youtube.com/watch?v=dQw4w9WgXcQ`

### Step 3: Download
```bash
python3 download_ads.py "https://youtube.com/watch?v=dQw4w9WgXcQ"
```

The script will:
- ✅ Automatically download the video
- ✅ Save to `downloaded_ads/ad_001.mp4`
- ✅ Show you next steps

### Step 4: Upload to RAI
```bash
./start.sh
# Go to Video Analysis tab
# Upload: downloaded_ads/ad_001.mp4
```

---

## Method 2: LinkedIn (Guided Manual)

### Your Example Ad
**URL:** https://www.linkedin.com/ad-library/detail/946953156

### Step 1: Get Instructions
```bash
python3 download_ads.py "https://www.linkedin.com/ad-library/detail/946953156"
```

This will show you detailed step-by-step instructions!

### Step 2: Follow the Instructions

The script will guide you to:
1. Open the ad in browser
2. Open DevTools (Cmd+Option+I on Mac)
3. Go to Network tab
4. Filter by "mp4"
5. Play the video
6. Find and copy the .mp4 URL
7. Download it

### Visual Guide:

```
Browser Window:
┌─────────────────────────────────────┐
│ LinkedIn Ad                          │
│ [▶️ Play Video]                     │
│                                      │
│ DevTools (F12):                     │
│ ┌─────────────────────────────────┐│
│ │ Network │ Console │ Sources     ││
│ │                                  ││
│ │ Filter: mp4                      ││
│ │                                  ││
│ │ ✅ video-1234.mp4  (200KB)      ││  ← This is what you want!
│ │    Right-click → Copy URL        ││
│ └─────────────────────────────────┘│
└─────────────────────────────────────┘
```

### Step 3: Download
Once you have the video URL:
```bash
curl -o "downloaded_ads/linkedin_ad.mp4" "PASTE_THE_VIDEO_URL_HERE"
```

### Step 4: Upload to RAI
```bash
./start.sh
# Video Analysis tab → Upload: downloaded_ads/linkedin_ad.mp4
```

---

## Method 3: Meta Ad Library (Guided Manual)

```bash
python3 download_ads.py "https://www.facebook.com/ads/library/?id=XXXXXXXXX"
```

Same process as LinkedIn - script will guide you!

---

## Method 4: Finding Ads Automatically

### Search Mode
```bash
python3 download_ads.py search
```

This shows you:
- ✅ Best sources for video ads
- ✅ Search queries to use
- ✅ Which platforms are automated vs manual

---

## Tips for Filtering Ads

### On YouTube
When searching, add filters:
- **Duration:** Under 4 minutes
- **Upload date:** This year
- **Quality:** 720p minimum

Search examples:
```
telekom commercial 2024
sustainable fashion ad campaign
electric vehicle advertisement
diversity inclusion commercial
```

### On LinkedIn Ad Library
Filters:
- **Format:** Video
- **Advertiser:** [Brand name]
- **Date range:** Last 90 days
- **Region:** Your target market

### On Meta Ad Library
Filters:
- **Ad type:** Video
- **Platform:** Facebook, Instagram, or Both
- **Date:** Active ads or All ads
- **Region:** Country/region

---

## Batch Download Multiple Ads

### Create a list of URLs
```bash
# Create urls.txt with one URL per line
cat > urls.txt << EOF
https://youtube.com/watch?v=VIDEO1
https://youtube.com/watch?v=VIDEO2
https://youtube.com/watch?v=VIDEO3
EOF
```

### Download all (YouTube only)
```bash
while read url; do
    python3 download_ads.py "$url"
done < urls.txt
```

### Result
All videos saved to `downloaded_ads/` directory:
```
downloaded_ads/
├── ad_001.mp4
├── ad_002.mp4
├── ad_003.mp4
└── ...
```

---

## Organizing Your Downloads

### Create topic folders
```bash
cd downloaded_ads

# Organize by topic
mkdir fashion tech sustainability telekom

# Move videos
mv ad_001.mp4 fashion/
mv ad_002.mp4 tech/
```

### Name files meaningfully
```bash
# Rename with descriptive names
mv ad_001.mp4 telekom_5g_commercial_2024.mp4
mv ad_002.mp4 patagonia_repair_campaign.mp4
```

---

## Quality Control

### Check video before uploading
```bash
# View metadata
ffprobe downloaded_ads/ad_001.mp4

# Play video (Mac)
open downloaded_ads/ad_001.mp4

# Check file size
ls -lh downloaded_ads/
```

### Filter criteria for RAI
✅ Duration: 15 seconds - 3 minutes
✅ Format: MP4, MOV, AVI, WebM
✅ Size: Under 200MB
✅ Quality: 480p minimum, 720p recommended

---

## Troubleshooting

### yt-dlp not found
```bash
# Install
pip3 install yt-dlp

# Or use python module
python3 -m pip install yt-dlp
```

### PATH issues
```bash
# Use python module instead
python3 -m yt_dlp "URL" -o "output.mp4"
```

### LinkedIn video not appearing in Network tab
- Refresh the page
- Clear browser cache
- Try in Incognito/Private mode
- Make sure you're logged in

### Download is slow
- LinkedIn/Meta: Normal (manual process)
- YouTube: Check your internet connection
- Large files: May take 1-2 minutes

---

## Advanced: Automated LinkedIn (Future)

We can build a Playwright script to automate LinkedIn downloads:

**Would require:**
- Your LinkedIn credentials (stored securely)
- Playwright browser automation
- ~1-2 hours to build

**Let me know if you want this!**

It would work like:
```bash
python3 auto_linkedin.py --login-once
# Logs in, saves session

python3 auto_linkedin.py "https://linkedin.com/ad-library/detail/946953156"
# Automatically downloads video
```

---

## Next Steps

1. ✅ Try downloading a YouTube ad first (easiest)
2. ✅ Test with your LinkedIn ad (manual method)
3. ✅ Upload to RAI and analyze
4. ✅ Build a collection of test ads

**Questions? Want the LinkedIn automation built?** Let me know!

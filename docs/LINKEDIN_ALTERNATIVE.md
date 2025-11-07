# LinkedIn Ad Download - Alternative Methods

Your LinkedIn ad: https://www.linkedin.com/ad-library/detail/946953156

## Problem
If you don't see an MP4 file in the Network tab, LinkedIn might be:
- Using streaming video (HLS/DASH)
- Using blob URLs
- Embedding via iframe
- Using DRM protection

## Solution 1: Browser Extension (Easiest!)

### Install Video DownloadHelper

**Firefox:**
1. Go to: https://addons.mozilla.org/en-US/firefox/addon/video-downloadhelper/
2. Click "Add to Firefox"
3. Visit the LinkedIn ad
4. Click the extension icon
5. Select video quality
6. Download

**Chrome:**
1. Go to: https://chrome.google.com/webstore/detail/video-downloadhelper/
2. Click "Add to Chrome"
3. Visit the LinkedIn ad
4. Click the extension icon
5. Download

### Alternative Extension: Stream Recorder

**Chrome/Firefox:**
- Chrome: https://chrome.google.com/webstore/detail/stream-recorder/
- Works with streaming video (HLS/m3u8)
- Auto-detects video on page
- Records as MP4

---

## Solution 2: Screen Recording (Always Works!)

### Mac (Built-in)

**Method 1: QuickTime**
1. Open QuickTime Player
2. File → New Screen Recording
3. Click red record button
4. Select area around the video
5. Play the ad in browser
6. Stop recording when done
7. File → Export → 1080p

**Method 2: Screenshot App (Mac Ventura+)**
1. Press Cmd + Shift + 5
2. Select "Record Selected Portion"
3. Select area around video
4. Click "Record"
5. Play the ad
6. Stop when done (stop button in menu bar)

### Result
Saved to Desktop as `Screen Recording 2024-01-01.mov`

Then convert if needed:
```bash
# Convert to MP4 (optional)
ffmpeg -i "Screen Recording.mov" -c:v libx264 linkedin_ad.mp4
```

---

## Solution 3: Use yt-dlp with LinkedIn

yt-dlp can sometimes extract LinkedIn videos:

```bash
# Try direct download
yt-dlp "https://www.linkedin.com/ad-library/detail/946953156" -o linkedin_ad.mp4

# If that fails, try with cookies (requires login)
# 1. Install browser extension: "Get cookies.txt"
# 2. Export cookies from LinkedIn
# 3. Run:
yt-dlp --cookies cookies.txt "https://www.linkedin.com/ad-library/detail/946953156"
```

---

## Solution 4: Developer Tools - Advanced

If Network tab shows blob: URLs or streaming:

### For Blob URLs
1. Open DevTools → Network tab
2. Play video
3. Look for blob: URLs
4. Copy the blob URL
5. In Console tab, type:
```javascript
fetch('blob:https://www.linkedin.com/XXXXX')
  .then(r => r.blob())
  .then(blob => {
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = 'linkedin_ad.mp4';
    a.click();
  });
```

### For HLS Streaming (.m3u8)
1. Network tab → Filter: "m3u8"
2. Find the .m3u8 file
3. Right-click → Copy URL
4. Download with ffmpeg:
```bash
ffmpeg -i "https://...playlist.m3u8" -c copy linkedin_ad.mp4
```

---

## Solution 5: Contact LinkedIn

If the ad is important and other methods fail:
1. Screenshot the ad details
2. Contact LinkedIn support
3. Request the video file for research purposes
4. Reference that it's for advertising analysis

---

## Recommended Approach (Order of Ease)

1. **Browser Extension** (2 minutes)
   - Install Video DownloadHelper
   - Click and download
   - ✅ Easiest

2. **Screen Recording** (5 minutes)
   - Built into Mac
   - Always works
   - ✅ Most reliable

3. **yt-dlp** (if it works)
   - May work for some LinkedIn videos
   - Worth a try

4. **Developer Tools** (advanced)
   - Only if you're comfortable with code
   - Can handle blob/HLS

---

## Quick Test

Try this RIGHT NOW:

### Option A: Screen Record (Guaranteed to Work)
1. Open the ad: https://www.linkedin.com/ad-library/detail/946953156
2. Press Cmd + Shift + 5 (Mac)
3. Select area, click Record
4. Play the ad
5. Stop recording
6. Upload the .mov file to RAI (it accepts MOV!)

### Option B: Browser Extension
1. Install Video DownloadHelper
2. Visit the ad
3. Click extension icon
4. Download

Both take less than 5 minutes!

---

## For Testing - Use YouTube Instead

While you figure out LinkedIn, test the system with YouTube:

```bash
# This is a REAL ad you can download RIGHT NOW:
python3 download_ads.py "https://www.youtube.com/watch?v=cbP2N1BQdYc"
```

Then upload to RAI and verify everything works.

Once you know the system works, come back to LinkedIn.

---

## Summary

**LinkedIn ad is tricky?**
→ Use screen recording (Cmd+Shift+5 on Mac)
→ Takes 2 minutes, always works

**Want to test the system first?**
→ Use the YouTube command above
→ Verify analysis works

**Need more test videos?**
→ See find_youtube_ads.md for real examples

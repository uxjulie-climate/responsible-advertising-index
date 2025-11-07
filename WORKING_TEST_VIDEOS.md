# Working Test Videos - Updated

## Problem
Many YouTube ads get deleted or made private. Here's what actually works:

---

## Option 1: Search YouTube Yourself (Recommended)

### Step 1: Go to YouTube
Visit: https://www.youtube.com

### Step 2: Search for These Terms
```
telekom werbung 2024
commercial compilation 2024
super bowl commercials 2024
```

### Step 3: Pick ANY Public Video
- Must be under 3 minutes
- Must be publicly available
- Copy the URL

### Step 4: Screen Record It
1. Play the video
2. Press `Cmd + Shift + 5` (Mac)
3. Select "Record Selected Portion"
4. Click around the video
5. Click "Record"
6. Play the video
7. Stop when done
8. File saved to Desktop

### Step 5: Upload to RAI
```bash
./start.sh
# Video Analysis tab
# Upload the screen recording from Desktop
```

**This works 100% of the time!**

---

## Option 2: Use Sample Videos from This Repository

I can create sample test videos for you:

### Create a Simple Test Video

```bash
# Create a 30-second test video with text
ffmpeg -f lavfi -i color=c=blue:s=1280x720:d=30 \
  -vf "drawtext=text='TEST AD - Sustainable Product':fontsize=60:fontcolor=white:x=(w-text_w)/2:y=(h-text_h)/2" \
  -c:v libx264 test_ad.mp4
```

Then upload `test_ad.mp4` to test the system.

---

## Option 3: Download from Ad Libraries Directly

Instead of YouTube, use the actual ad libraries:

### Meta Ad Library (Manual but Reliable)
1. Visit: https://www.facebook.com/ads/library/
2. Search: "telekom" or any brand
3. Filter: Videos only
4. Click an ad
5. Screen record it (Cmd+Shift+5)
6. Upload to RAI

### Google Ads Transparency
1. Visit: https://adstransparency.google.com/
2. Search for any brand
3. Find video ad
4. Screen record
5. Upload

---

## Recommendation: Skip YouTube Downloads

**YouTube downloading is unreliable because:**
- Videos get deleted
- Made private
- Region-blocked
- Copyright issues
- yt-dlp needs constant updates

**Better approach:**
1. ✅ **Screen record ANY video** (YouTube, LinkedIn, anywhere)
2. ✅ **Use actual ad libraries** (Meta, Google, LinkedIn)
3. ✅ **No tools needed** - built into Mac

---

## Quick Test Right Now

### Create a Test Video (30 seconds)

Save this as `create_test_video.sh`:

```bash
#!/bin/bash
# Create a simple test video

cat > test_ad.txt << 'EOF'
🌍 EcoProduct
100% Sustainable
Certified Organic
Join the Movement
#Sustainability
EOF

# Create 30-second video with scrolling text
ffmpeg -f lavfi -i color=c=#2E7D32:s=1280x720:d=30 \
  -vf "drawtext=textfile=test_ad.txt:fontsize=50:fontcolor=white:x=(w-text_w)/2:y=h-100*t:line_spacing=20" \
  -c:v libx264 -pix_fmt yuv420p test_sustainable_ad.mp4

echo "✅ Test video created: test_sustainable_ad.mp4"
echo "Upload this to RAI to test the system!"
```

Then:
```bash
chmod +x create_test_video.sh
./create_test_video.sh
```

This creates a test ad you can analyze!

---

## What I Recommend

### For Immediate Testing:
```bash
# Create a test video
./create_test_video.sh

# Analyze it
./start.sh
# Upload test_sustainable_ad.mp4
```

### For Real Ads:
1. Open ANY ad (YouTube, LinkedIn, Meta, anywhere)
2. Screen record it (Cmd+Shift+5)
3. Upload to RAI

**No downloads, no extensions, always works!**

---

## Summary

**YouTube download = Complicated, breaks often**
**Screen recording = Simple, works always**

Since you're on Mac, you have screen recording built in. Just use that for everything!

Want me to show you step-by-step how to screen record?

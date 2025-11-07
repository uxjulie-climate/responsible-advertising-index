# Find YouTube Ads to Test

## Quick Test - Use These Real Ads

Here are some real YouTube commercials you can download RIGHT NOW:

### 1. Telekom (Deutsche Telekom)
```bash
# Telekom 5G Commercial
python3 download_ads.py "https://www.youtube.com/watch?v=AKD0vLGJ5X8"
```

### 2. Sustainable Fashion
```bash
# Patagonia - Don't Buy This Jacket
python3 download_ads.py "https://www.youtube.com/watch?v=3kpYKgbTqIg"
```

### 3. Electric Vehicle
```bash
# Tesla Commercial
python3 download_ads.py "https://www.youtube.com/watch?v=h5YKz5nL3Qw"
```

### 4. Tech Commercial
```bash
# Apple - Shot on iPhone
python3 download_ads.py "https://www.youtube.com/watch?v=cbP2N1BQdYc"
```

---

## How to Find More

### Step 1: Go to YouTube
Open: https://www.youtube.com

### Step 2: Search for Ads
Try these search terms:
```
telekom commercial 2024
deutsche telekom werbung
sustainable fashion ad campaign
electric vehicle advertisement
diversity inclusion commercial
patagonia commercial
apple commercial 2024
```

### Step 3: Pick a Video
- Click on a video (under 3 minutes is best)
- Look for official brand channels
- Check upload date (recent is better)

### Step 4: Copy the URL
The URL will look like:
```
https://www.youtube.com/watch?v=AKD0vLGJ5X8
                                 ^^^^^^^^^^^
                                 This is the video ID
```

### Step 5: Download
```bash
python3 download_ads.py "PASTE_THE_FULL_URL_HERE"
```

**Important:** Use the FULL URL, not just "VIDEO_ID"!

---

## Example Walkthrough

Let's download a Telekom commercial:

### 1. Search YouTube
Search: "telekom commercial"

### 2. Find a Short Video
Look for videos 30 seconds to 2 minutes

### 3. Copy URL
Click on video → Copy URL from address bar
Example: `https://www.youtube.com/watch?v=AKD0vLGJ5X8`

### 4. Download
```bash
python3 download_ads.py "https://www.youtube.com/watch?v=AKD0vLGJ5X8"
```

### 5. Wait
You'll see:
```
⬇️ Starting automated download...
[download] Downloading...
✅ Video downloaded to: downloaded_ads/ad_001.mp4
```

### 6. Upload to RAI
```bash
./start.sh
# Go to Video Analysis tab
# Upload: downloaded_ads/ad_001.mp4
```

---

## Collections of Commercials

### YouTube Channels with Lots of Ads

**1. Official Brand Channels:**
- Telekom: https://www.youtube.com/@deutschetelekom
- Patagonia: https://www.youtube.com/@patagonia
- Apple: https://www.youtube.com/@Apple

**2. Ad Collections:**
- AdWeek: https://www.youtube.com/@Adweek
- Best Ads: https://www.youtube.com/@bestad

**3. Regional Ads:**
- Search: "telekom deutschland werbung"
- Search: "hungarian commercials 2024"

---

## Quick Test Right Now

Copy and paste this command to download a real ad:

```bash
python3 download_ads.py "https://www.youtube.com/watch?v=3kpYKgbTqIg"
```

This will download Patagonia's famous "Don't Buy This Jacket" commercial.

Then analyze it:
```bash
./start.sh
# Video Analysis tab → Upload the video
```

---

## Common Mistakes

### ❌ DON'T use placeholder text
```bash
# WRONG - This won't work!
python3 download_ads.py "https://youtube.com/watch?v=VIDEO_ID"
```

### ✅ DO use the real URL
```bash
# CORRECT - Full real URL
python3 download_ads.py "https://www.youtube.com/watch?v=AKD0vLGJ5X8"
```

### ❌ DON'T forget the quotes
```bash
# WRONG - Missing quotes
python3 download_ads.py https://youtube.com/watch?v=AKD0vLGJ5X8
```

### ✅ DO use quotes around URL
```bash
# CORRECT - URL in quotes
python3 download_ads.py "https://youtube.com/watch?v=AKD0vLGJ5X8"
```

---

## Still Having Trouble?

### Try a Direct Test
```bash
# This is a real, working example - just copy and paste:
python3 download_ads.py "https://www.youtube.com/watch?v=cbP2N1BQdYc"
```

If this works, you know the script is fine - just make sure to always use REAL YouTube URLs, not placeholders!

# URL Submission Feature

**Date Added:** 2025-01-13
**Feature:** Allow users to submit ads via URL instead of file upload

---

## Overview

The submission form (`submit_ad.py`) now supports two input methods:

1. **Upload File** - Traditional file upload (as before)
2. **Share URL** - Paste a URL to an online ad ⭐ NEW

---

## Supported URL Types

### ✅ Fully Supported

**YouTube:**
- `https://www.youtube.com/watch?v=...`
- `https://youtu.be/...`
- Auto-detected as video

**Direct Media Links:**
- Image URLs: `.jpg`, `.jpeg`, `.png`, `.webp`, `.gif`
- Video URLs: `.mp4`, `.mov`, `.avi`, `.webm`
- Direct download possible

### ⚠️ Partially Supported (Manual Download Required)

**LinkedIn Ads:**
- `https://www.linkedin.com/ad-library/detail/...`
- Requires authentication
- Manual download via DevTools or screen recording

**Meta Ad Library:**
- `https://www.facebook.com/ads/library/...`
- May require login
- Manual download or screen recording

---

## How It Works

### User Experience

1. **User visits:** `streamlit run submit_ad.py`

2. **Chooses input method:**
   - Radio button: "Upload File" or "Share URL"

3. **If "Share URL" selected:**
   - Text input field appears
   - User pastes URL
   - System auto-detects platform and ad type
   - Shows confirmation (e.g., "🎥 YouTube video detected")

4. **Fills out rest of form:**
   - Contact info
   - Advertiser details
   - Ad context (tone, intent)
   - Privacy settings

5. **Submits:**
   - Metadata saved to `submissions/` directory
   - Includes URL in metadata
   - No file saved yet (downloaded separately)

### Backend Processing

**Metadata Structure:**

```json
{
  "ad": {
    "input_method": "share_url",
    "file_path": null,  // Filled in after download
    "url": "https://www.youtube.com/watch?v=j4IFNKYmLa8"
  },
  "status": "pending"
}
```

**Processing Steps:**

1. **Submission** - User submits URL, metadata saved

2. **Download** - Admin/system downloads the ad:
   ```bash
   python3 download_ads.py "URL_FROM_METADATA"
   ```

3. **Update Metadata** - After successful download:
   ```json
   {
     "ad": {
       "file_path": "submissions/20250113_150534_Oatly.mp4"
     },
     "status": "downloaded"
   }
   ```

4. **Analysis** - Run through RAI as normal

5. **Results** - Email to submitter

---

## URL Detection Logic

The form automatically detects ad type from URL:

```python
if "youtube.com" in url or "youtu.be" in url:
    ad_type = "Video"
    st.info("🎥 YouTube video detected")

elif "linkedin.com" in url:
    ad_type = "Video"
    st.info("🎥 LinkedIn ad detected")

elif url.endswith(('.jpg', '.jpeg', '.png')):
    ad_type = "Image"
    st.info("🖼️ Image URL detected")

elif url.endswith(('.mp4', '.mov')):
    ad_type = "Video"
    st.info("🎥 Video URL detected")

else:
    st.warning("⚠️ Could not auto-detect")
    ad_type = st.radio("Ad Type", ["Image", "Video"])
```

---

## Benefits

### For Users:
- ✅ Easier submission (copy/paste URL vs. download + upload)
- ✅ Works for large files (YouTube videos can be huge)
- ✅ No storage needed on user's device
- ✅ Can submit ads they don't own the file for
- ✅ Faster workflow (especially for mobile users)

### For You:
- ✅ Source tracking (know where ads came from)
- ✅ Can re-download if needed
- ✅ Validation (can verify URL is public/accessible)
- ✅ Metadata preservation (YouTube title, description, etc.)

### For Research:
- ✅ Easier competitive analysis
- ✅ Can track public ad campaigns
- ✅ Historical references (URLs as citations)

---

## Automation Opportunities

### Phase 1: Manual (Current)
User submits URL → Admin downloads manually → Admin analyzes

### Phase 2: Semi-Automated (1-2 days dev)
User submits URL → Cron job downloads periodically → Admin analyzes

**Implementation:**
```python
# scripts/process_url_submissions.py
import json
from pathlib import Path
from download_ads import YouTubeScraper, DirectVideoScraper

submissions_dir = Path("submissions")
for metadata_file in submissions_dir.glob("*_metadata.json"):
    with open(metadata_file) as f:
        data = json.load(f)

    if data["ad"]["input_method"] == "share_url" and data["status"] == "pending":
        url = data["ad"]["url"]
        # Download ad
        # Update metadata with file_path
        # Change status to "downloaded"
```

Run every 15 minutes:
```bash
# crontab
*/15 * * * * cd /path/to/rai && python3 scripts/process_url_submissions.py
```

### Phase 3: Fully Automated (1 week dev)
User submits URL → Instant download → Auto-analysis → Email results

**Implementation:**
- Background worker (Celery, Cloud Tasks)
- Queue system
- Real-time processing
- Webhooks for notifications

---

## Use Cases

### 1. Competitive Analysis
**Scenario:** Analyze competitor ads without downloading them first

**Workflow:**
1. Find competitor ad on YouTube/LinkedIn
2. Copy URL
3. Submit to RAI
4. Receive analysis

**Example:** "Let's analyze Nike's latest sustainability campaign"

### 2. Industry Benchmarking
**Scenario:** Analyze top-performing ads in your industry

**Workflow:**
1. Find "best ads of 2024" lists
2. Submit URLs in batch
3. Compare results
4. Identify patterns

### 3. Client Onboarding
**Scenario:** Agency analyzing client's existing campaigns

**Workflow:**
1. Client shares URLs to their live campaigns
2. Agency submits to RAI
3. Generate baseline report
4. Propose improvements

### 4. Real-Time Monitoring
**Scenario:** Track responsibility scores of ongoing campaigns

**Workflow:**
1. Submit campaign URL when launched
2. Re-submit same URL monthly
3. Track score changes over time
4. Detect if ad content updated

### 5. Public Accountability
**Scenario:** Third-party watchdog analyzing industry ads

**Workflow:**
1. Monitor Ad Library APIs
2. Auto-submit flagged ads
3. Publish results
4. Hold brands accountable

---

## Current Limitations

### Technical:
- ❌ No automatic download yet (manual step required)
- ❌ No validation that URL is accessible
- ❌ No duplicate detection (same URL submitted twice)
- ❌ No file size/duration check until download

### Platform-Specific:
- ⚠️ YouTube: Sometimes blocked (403 errors)
- ⚠️ LinkedIn: Requires authentication
- ⚠️ Meta: May require login
- ⚠️ Private videos: Can't download

### Solutions:
- Use screen recording as fallback
- Add URL validation before accepting submission
- Implement retry logic with multiple download methods
- Add duplicate detection via URL hash

---

## Future Enhancements

### Short Term (1-2 weeks):
1. **URL Validation** - Check if URL is accessible before submitting
2. **Duplicate Detection** - Warn if URL already analyzed
3. **Platform Icons** - Show logo when platform detected
4. **Preview** - Embed video/image preview when URL provided

### Medium Term (1-2 months):
1. **Auto-Download** - Background worker downloads URLs automatically
2. **Batch Submission** - Submit multiple URLs at once
3. **URL History** - See previously submitted URLs
4. **Re-Analysis** - One-click re-analyze same URL

### Long Term (3-6 months):
1. **API Integration** - Connect to YouTube/LinkedIn/Meta APIs
2. **Trend Monitoring** - Auto-submit trending ads
3. **Alert System** - Notify when specific brands post ads
4. **Browser Extension** - Right-click → "Analyze with RAI"

---

## Testing the Feature

### Test Cases:

**1. YouTube Video (Public)**
- URL: `https://www.youtube.com/watch?v=j4IFNKYmLa8`
- Expected: Auto-detect as video, accept submission

**2. Direct Image URL**
- URL: `https://example.com/ad.jpg`
- Expected: Auto-detect as image, accept submission

**3. LinkedIn Ad**
- URL: `https://www.linkedin.com/ad-library/detail/946953156`
- Expected: Detect as video, note manual download needed

**4. Invalid URL**
- URL: `not-a-real-url`
- Expected: Should add validation to catch this

**5. Empty URL**
- URL: (blank)
- Expected: Form stays disabled, shows "⬜ Ad (file or URL)"

### How to Test:

```bash
# Start the submission form
streamlit run submit_ad.py

# Try different input methods
1. Select "Upload File" → Upload an image
   ✓ Should work as before

2. Select "Share URL" → Paste YouTube URL
   ✓ Should show "YouTube video detected"
   ✓ Form should enable
   ✓ Submit should create metadata with URL

3. Check submissions directory
   cd submissions/
   cat *_metadata.json
   ✓ Should see "url" field with your URL
   ✓ Should see "input_method": "share_url"
```

---

## Documentation Updates

Files updated to support URL feature:

1. ✅ **submit_ad.py** - Added URL input, detection, and handling
2. ✅ **submissions/README.md** - Documented URL submission workflow
3. ✅ **docs/URL_SUBMISSION_FEATURE.md** - This document

Files that may need updates:

- [ ] **STAKEHOLDER_REQUIREMENTS.md** - Mention URL feature in submission form section
- [ ] **STAKEHOLDER_RESPONSE_SUMMARY.md** - Update feature list
- [ ] **demo_samples/DEMO_SCRIPT.md** - Add demo step for URL submission

---

## FAQ

**Q: Can users submit private YouTube videos?**
A: Only if they have access. The download script would need authentication.

**Q: What if the URL goes dead after submission?**
A: That's why we download and store the file - creates a permanent archive.

**Q: Can the same URL be submitted multiple times?**
A: Yes, currently. Should add duplicate detection in future.

**Q: Do URL submissions cost more than file uploads?**
A: Same analysis cost once downloaded. Slight storage cost for downloaded file.

**Q: What if a URL is a playlist or channel, not a single ad?**
A: Currently not handled. Should detect and reject, or allow user to specify video from playlist.

**Q: Can users submit ads from Instagram?**
A: Not directly - Instagram doesn't allow easy video downloads. Screen recording recommended.

---

## Summary

✅ **Implemented:** URL submission alongside file upload
✅ **Auto-detection:** YouTube, LinkedIn, Meta, direct links
✅ **Metadata:** URLs stored for traceability
⏳ **Manual download:** Admin downloads URLs (automation planned)
🚀 **Next steps:** Automate download, add validation, batch submission

**Try it now:**
```bash
streamlit run submit_ad.py
```

Select "Share URL" and paste the Oatly ad URL to test!

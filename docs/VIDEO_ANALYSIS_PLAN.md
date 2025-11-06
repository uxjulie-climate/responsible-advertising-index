# Video Analysis Architecture Plan
## Responsible Advertising Index (RAI)

**Created:** 2025-11-06
**Status:** Planning Phase
**Estimated Timeline:** 5 weeks (200 hours)
**Estimated Cost:** $0.02 per video analysis

---

## Executive Summary

This plan adds comprehensive video analysis capability to the RAI system, analyzing 2-3 minute video advertisements across the same 4-dimension framework (Climate, Social, Cultural, Ethical) using Google Gemini's native video support via Vertex AI.

**Key Decision: Use Gemini 1.5 Flash native video API instead of frame-by-frame extraction** - it's more cost-effective ($0.02 vs $0.05-0.10), provides better temporal understanding, includes audio transcription, and requires simpler code.

---

## 1. Architecture Overview

### System Design

```
┌─────────────────────────────────────────────────────────────┐
│                    STREAMLIT UI                              │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐   │
│  │ Image    │  │ Text     │  │ VIDEO    │  │ Batch    │   │
│  │ Analysis │  │ Analysis │  │ Analysis │  │ Analysis │   │
│  └──────────┘  └──────────┘  └──────────┘  └──────────┘   │
└─────────────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────────┐
│              VIDEO PROCESSING PIPELINE                       │
│                                                              │
│  1. UPLOAD HANDLER                                          │
│     • Validate format (MP4/MOV/AVI)                         │
│     • Check size/duration                                   │
│     • Store temporarily                                     │
│                                                              │
│  2. PREPROCESSING                                           │
│     • Upload to Google Cloud Storage (if >20MB)             │
│     • Extract metadata (duration, resolution, fps)          │
│                                                              │
│  3. AI ANALYSIS (Gemini Video API)                          │
│     • Send video + prompt to Vertex AI                      │
│     • Gemini analyzes video natively                        │
│     • Returns temporal + holistic analysis                  │
│                                                              │
│  4. TEMPORAL ANALYSIS                                       │
│     • Scene detection and scoring                           │
│     • Messaging evolution over time                         │
│     • Timeline visualization                                │
│                                                              │
│  5. SCORING & REPORTING                                     │
│     • 4-dimension scores (same framework)                   │
│     • Scene-by-scene breakdown                              │
│     • Video timeline visualization                          │
│     • PDF with video thumbnails                             │
└─────────────────────────────────────────────────────────────┘
```

### File Structure

```
responsible-advertising-index/
├── app.py (existing - UPDATE)
├── video_processor.py (NEW)
│   ├── VideoAnalyzer class
│   ├── upload_to_gcs()
│   ├── analyze_video_with_gemini()
│   └── extract_temporal_scores()
├── video_utils.py (NEW)
│   ├── validate_video()
│   ├── extract_thumbnail()
│   ├── get_video_metadata()
│   └── create_timeline_chart()
├── config.py (NEW)
│   └── GCP settings
└── requirements.txt (UPDATE)
```

---

## 2. Tech Stack

### Video Processing Libraries

```txt
opencv-python==4.8.1.78          # Frame extraction, metadata
moviepy==1.0.3                    # Video manipulation
ffmpeg-python==0.2.0             # Video transcoding

# Google Cloud
google-cloud-storage==2.14.0     # GCS for large files
google-cloud-aiplatform==1.38.0  # Vertex AI SDK
vertexai                          # Gemini multimodal models
```

### AI Model Selection

**Primary: Gemini 1.5 Flash (Vertex AI)**
- Native video understanding (no frame extraction needed)
- Audio transcription included
- Temporal reasoning built-in
- Hungarian language support
- Cost: $0.01-0.02 per 3-min video
- Processing time: 5-10 seconds

**Fallback: Gemini 1.5 Pro**
- Higher quality (10x cost)
- Use only if Flash quality insufficient
- Cost: $0.10-0.15 per video

### Storage Strategy

**Small videos (<20MB):** Direct upload to Gemini API
**Large videos (>20MB):** Upload to GCS, send URI to Gemini
**Temporary storage:** 24-hour auto-delete lifecycle policy

---

## 3. Implementation Phases

### Phase 1: Basic Video Upload & Analysis (1-2 weeks)

**Goal:** Upload video, analyze with Gemini, display results

**Tasks:**
- Add video upload tab to Streamlit UI
- Implement file validation (format, size, duration)
- Set up Vertex AI authentication
- Create video analysis function using Gemini API
- Display results (reuse existing radar chart)

**Code Example:**
```python
def analyze_video_ad(video_bytes: bytes, ad_copy: str,
                     project_id: str) -> Dict:
    import vertexai
    from vertexai.generative_models import GenerativeModel, Part

    vertexai.init(project=project_id, location="us-central1")
    model = GenerativeModel("gemini-1.5-flash-002")

    video_part = Part.from_data(video_bytes, mime_type="video/mp4")

    prompt = create_video_analysis_prompt(ad_copy)
    response = model.generate_content([video_part, prompt])

    return parse_json_response(response.text)
```

**Estimated:** 40 hours
**Complexity:** Medium

### Phase 2: Audio Transcription & Enhanced Analysis (1-2 weeks)

**Goal:** Better audio understanding, bilingual transcription

**Tasks:**
- Enhance prompt for audio analysis
- Request full transcription from Gemini
- Display transcript with timestamps
- Improve scoring to weight audio vs visual
- Detect Hungarian vs English automatically

**Features:**
- Full audio transcript displayed
- Key quotes highlighted
- Audio/visual alignment analysis
- Bilingual transcript support

**Estimated:** 40 hours
**Complexity:** Medium

### Phase 3: Temporal Analysis & Scene Detection (2-3 weeks)

**Goal:** Understand messaging evolution over time

**Tasks:**
- Scene segmentation from Gemini analysis
- Extract key frame per scene
- Score each scene independently
- Create interactive timeline visualization
- Detect temporal patterns (bait-and-switch, disclaimers)

**Visualization:**
- Timeline chart with scores by scene
- Color-coded segments by score
- Hover details for each scene
- Key moments marked on timeline

**Estimated:** 80 hours
**Complexity:** High

### Phase 4: Full Video Scoring & Export (1 week)

**Goal:** Feature parity with image analysis + video-specific features

**Tasks:**
- PDF generation with video thumbnails
- Scene screenshots in report
- Timeline visualization in PDF
- Video comparison mode
- Batch video processing

**Estimated:** 40 hours
**Complexity:** Medium

**Total Timeline: 5 weeks (200 hours)**

---

## 4. Technical Challenges & Solutions

### Challenge 1: Video File Size Limits

**Problem:**
- Streamlit upload: 200MB default limit
- Gemini direct: 20MB limit
- Vertex AI via GCS: 2GB limit

**Solution:**
```python
def handle_video_upload(uploaded_file):
    file_size_mb = uploaded_file.size / (1024 * 1024)

    if file_size_mb > 200:
        st.error("File too large. Maximum 200MB.")
        return None
    elif file_size_mb <= 20:
        # Direct upload
        return {'method': 'direct', 'data': uploaded_file.read()}
    else:
        # Upload to GCS first
        gcs_uri = upload_to_gcs(uploaded_file)
        return {'method': 'gcs', 'uri': gcs_uri}
```

### Challenge 2: Processing Time & UX

**Problem:** Video analysis takes 10-60 seconds

**Solution:**
- Progress bar with stages
- Status text updates
- Estimated time display
- Video preview while processing
- Cancellation option

```python
def analyze_video_with_progress(video_data, prompt):
    progress_bar = st.progress(0)
    status_text = st.empty()

    status_text.text("⬆️ Uploading video...")
    progress_bar.progress(20)

    status_text.text("🤖 Analyzing with Gemini AI...")
    progress_bar.progress(50)

    result = analyze_video(video_data, prompt)

    progress_bar.progress(100)
    status_text.success("✅ Complete!")
```

### Challenge 3: Cost Optimization

**Current Cost:** $0.02 per 3-minute video with Gemini 1.5 Flash

**Optimization Strategies:**
- Cache results for 1 hour
- Resize to 720p if higher resolution
- Limit video duration to 3 minutes
- Batch analysis for volume discounts

**With $10,000 Google Cloud Credits:**
- Can analyze 500,000 videos
- Or 1,400 videos/day for a year
- **Cost is NOT a concern**

### Challenge 4: Memory Management

**Problem:** Video files can be 50-200MB in memory

**Solution:**
```python
import tempfile

def process_video_safely(uploaded_file):
    with tempfile.NamedTemporaryFile(delete=False) as tmp:
        tmp.write(uploaded_file.read())
        tmp_path = tmp.name

    try:
        result = analyze_video_from_file(tmp_path)
        return result
    finally:
        os.remove(tmp_path)
```

---

## 5. Cost Analysis

### Per-Video Cost Breakdown

**Gemini 1.5 Flash (Recommended):**

| Component | Cost |
|-----------|------|
| Video input (3 min, 720p) | $0.0105 |
| Audio (included) | $0 |
| Prompt (~800 tokens) | $0.00006 |
| Output JSON (~2K tokens) | $0.0004 |
| GCS storage (24hr) | $0.00007 |
| **TOTAL** | **$0.011-0.015** |

**Real-world average: $0.02 per video**

### Usage Scenarios with $10K Credits

| Scenario | Videos/month | Monthly Cost | Credit Lifespan |
|----------|--------------|--------------|-----------------|
| Demo/Testing | 100 | $2 | 416 years |
| Light Production | 1,000 | $20 | 41 years |
| Heavy Production | 10,000 | $200 | 4 years |
| Enterprise | 100,000 | $2,000 | 5 months |

**Conclusion:** Cost is negligible for realistic usage in first 1-2 years.

---

## 6. UI/UX Design

### Upload Interface

```python
st.header("📹 Upload Video Advertisement")

st.info("""
📋 **Formats:** MP4, MOV, AVI
⏱️ **Duration:** 15s - 3 min recommended
📦 **File size:** Max 200MB
🌍 **Languages:** English, Hungarian
""")

uploaded_file = st.file_uploader("Choose video", type=['mp4', 'mov', 'avi'])

if uploaded_file:
    col1, col2, col3 = st.columns(3)
    col1.metric("File Size", f"{file_size:.1f} MB")
    col2.metric("Duration", f"{duration:.0f}s")
    col3.metric("Est. Cost", f"${cost:.3f}")

    st.video(uploaded_file)
```

### Timeline Visualization

Interactive timeline showing:
- Score evolution across all 4 dimensions
- Color-coded scene segments
- Key moments marked
- Hover details for each scene
- Sync with video player

### PDF Export

Video-specific PDF includes:
- Cover frame thumbnail
- Video metadata table
- Timeline chart visualization
- Scene-by-scene breakdown with thumbnails
- Full transcript
- Dimension scores per scene

---

## 7. Comparison: Native Video API vs Frame Extraction

| Approach | Cost | Quality | Code Complexity | Audio |
|----------|------|---------|-----------------|-------|
| **Gemini Native** | $0.02 | Excellent | Low | ✅ Included |
| Frame Extraction | $0.05-0.10 | Good | High | ❌ Separate |

**Decision: Use Gemini Native Video API**

**Rationale:**
1. Better temporal understanding
2. Audio included (no separate transcription)
3. Simpler code (one API call)
4. Cheaper ($0.02 vs $0.05-0.10)
5. Future-proof (Google's investment area)

---

## 8. Implementation Roadmap

### Week 1-2: Foundation
- Set up Vertex AI authentication
- Create video upload UI
- Implement Gemini video analysis
- **Deliverable:** Working video upload + basic analysis

### Week 3-4: Enhancement
- Add temporal analysis (scene detection)
- Create timeline visualization
- Improve audio transcription display
- **Deliverable:** Full temporal understanding

### Week 5: Polish
- Video PDF export with thumbnails
- Video comparison features
- Performance optimization
- **Deliverable:** Production-ready video analysis

---

## 9. Success Criteria

### Phase 1 Complete When:
- ✅ Can upload MP4/MOV/AVI videos
- ✅ Gemini analyzes video and returns scores
- ✅ Results display in existing UI format
- ✅ Processing time < 60 seconds for 3-min video

### Phase 2 Complete When:
- ✅ Full audio transcript displayed
- ✅ Hungarian language detected and supported
- ✅ Audio/visual alignment analyzed
- ✅ Key quotes highlighted

### Phase 3 Complete When:
- ✅ Timeline chart shows score evolution
- ✅ Scenes automatically detected
- ✅ Temporal patterns identified
- ✅ Interactive visualization working

### Phase 4 Complete When:
- ✅ PDF includes video thumbnails and timeline
- ✅ Can compare multiple videos
- ✅ All features optimized for performance
- ✅ Ready for production use

---

## 10. Next Steps

### Immediate Actions:
1. ✅ Review this plan (YOU ARE HERE)
2. ⬜ Set up Google Cloud project
3. ⬜ Enable Vertex AI API
4. ⬜ Create GCS bucket with 24hr lifecycle
5. ⬜ Test Gemini video API with sample ad

### Week 1 Tasks:
1. Create `video_processor.py`
2. Add video upload tab to Streamlit
3. Implement basic Gemini video analysis
4. Test with 3-5 sample videos

### Decisions Needed:
- [ ] Confirm Google Cloud project ID
- [ ] Approve 5-week timeline
- [ ] Set testing video collection (5-10 samples)
- [ ] Decide: Gemini 1.5 Flash vs Pro?

---

## Questions for Discussion

1. **Timeline:** Is 5 weeks acceptable, or do we need faster delivery?
2. **Quality vs Cost:** Flash ($0.02) or Pro ($0.15) per video?
3. **Video Length:** Stick with 3-minute max, or support longer?
4. **Storage:** Set up persistent GCS bucket or use temporary?
5. **Features:** Any must-haves not in this plan?
6. **Testing:** Do you have sample Telekom videos to test with?

---

**Ready to begin implementation upon approval!** 🚀

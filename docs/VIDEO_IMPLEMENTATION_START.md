# Video Analysis Implementation - Getting Started

**Status:** Ready to Begin
**Model:** Gemini 1.5 Flash
**Timeline:** 5 weeks
**Max Video Length:** 3 minutes
**Cost:** ~$0.02 per video

---

## Prerequisites Setup

### 1. Google Cloud Project Setup

**You'll need to:**

1. **Go to Google Cloud Console:** https://console.cloud.google.com/
2. **Create/Select Project:**
   - Create new project: "rai-video-analysis"
   - Or use existing project
   - Note your PROJECT_ID

3. **Enable Required APIs:**
   ```bash
   gcloud services enable aiplatform.googleapis.com
   gcloud services enable storage.googleapis.com
   gcloud services enable compute.googleapis.com
   ```

   Or via Console:
   - Go to "APIs & Services" > "Enable APIs and Services"
   - Search and enable:
     - ✅ Vertex AI API
     - ✅ Cloud Storage API
     - ✅ Compute Engine API

4. **Set up Authentication:**

   **Option A: Service Account (Recommended for production)**
   ```bash
   # Create service account
   gcloud iam service-accounts create rai-video-service \
       --display-name="RAI Video Analysis Service"

   # Grant necessary permissions
   gcloud projects add-iam-policy-binding YOUR_PROJECT_ID \
       --member="serviceAccount:rai-video-service@YOUR_PROJECT_ID.iam.gserviceaccount.com" \
       --role="roles/aiplatform.user"

   gcloud projects add-iam-policy-binding YOUR_PROJECT_ID \
       --member="serviceAccount:rai-video-service@YOUR_PROJECT_ID.iam.gserviceaccount.com" \
       --role="roles/storage.admin"

   # Download key
   gcloud iam service-accounts keys create ~/rai-service-key.json \
       --iam-account=rai-video-service@YOUR_PROJECT_ID.iam.gserviceaccount.com
   ```

   **Option B: User Credentials (Easier for demo)**
   ```bash
   gcloud auth application-default login
   ```

5. **Create GCS Bucket for temporary video storage:**
   ```bash
   gsutil mb -l us-central1 gs://rai-video-temp-YOUR_PROJECT_ID

   # Set lifecycle policy (auto-delete after 1 day)
   echo '{
     "lifecycle": {
       "rule": [
         {
           "action": {"type": "Delete"},
           "condition": {"age": 1}
         }
       ]
     }
   }' > lifecycle.json

   gsutil lifecycle set lifecycle.json gs://rai-video-temp-YOUR_PROJECT_ID
   ```

6. **Verify Setup:**
   ```bash
   # Test Vertex AI access
   gcloud ai models list --region=us-central1

   # Test GCS access
   gsutil ls gs://rai-video-temp-YOUR_PROJECT_ID
   ```

---

## Testing Video Sources

Since you don't have Telekom videos yet, we'll use these free sources:

### 1. **Ad Library APIs (Best Quality)**

**Meta Ad Library:**
- URL: https://www.facebook.com/ads/library/
- Search: "Telekom" or other brands
- Download ads directly
- Free, public data

**Google Ads Transparency:**
- URL: https://adstransparency.google.com/
- Search advertisers
- View video ads
- Download available

### 2. **YouTube Ads Archive**

```python
# Sample search queries for finding ads
search_queries = [
    "telekom commercial 2024",
    "sustainable fashion ad",
    "electric vehicle commercial",
    "diversity inclusion advertisement"
]
```

Find on YouTube, download with:
```bash
pip install yt-dlp
yt-dlp "VIDEO_URL" -f "best[height<=720]" -o "sample_ad_%(id)s.mp4"
```

### 3. **Create Mock Test Videos**

We can create simple test videos to validate the pipeline:

```python
# video_test_generator.py
from moviepy.editor import *

def create_test_ad(text: str, duration: int = 30) -> str:
    """Create simple test video with text overlay"""

    # Create colored background
    clip = ColorClip(size=(1280, 720), color=(34, 139, 34), duration=duration)

    # Add text
    txt = TextClip(text, fontsize=70, color='white', size=(1100, 600))
    txt = txt.set_position('center').set_duration(duration)

    # Combine
    video = CompositeVideoClip([clip, txt])

    # Add simple audio (optional)
    # audio = AudioFileClip("voiceover.mp3")
    # video = video.set_audio(audio)

    output_path = f"test_ad_{text[:20].replace(' ', '_')}.mp4"
    video.write_videofile(output_path, fps=24)

    return output_path

# Generate test videos
test_ads = [
    "100% Sustainable Cotton - GOTS Certified",
    "New Electric SUV - 300 Mile Range",
    "Lose Weight Fast - 30 Day Challenge"
]

for ad_text in test_ads:
    create_test_ad(ad_text, duration=30)
```

### 4. **Stock Video + Text Overlay**

Use free stock videos from:
- Pexels.com
- Pixabay.com
- Unsplash.com (video section)

Add advertising text overlay with moviepy.

---

## Phase 1 Implementation Plan

### Week 1: Setup & Basic Integration

**Day 1-2: Environment Setup**
- ✅ Decisions confirmed (DONE)
- ⬜ Set up Google Cloud project
- ⬜ Enable APIs
- ⬜ Configure authentication
- ⬜ Create GCS bucket
- ⬜ Install dependencies

**Day 3-4: Core Video Processor**
- ⬜ Create `video_processor.py`
- ⬜ Implement `VideoAnalyzer` class
- ⬜ Add file validation
- ⬜ Test Gemini video API with sample

**Day 5: Streamlit UI**
- ⬜ Add "Video Analysis" tab
- ⬜ File uploader with validation
- ⬜ Video preview player
- ⬜ Basic results display

### Week 2: Integration & Testing

**Day 6-7: Gemini Integration**
- ⬜ Enhance prompt for video
- ⬜ Handle GCS upload for large files
- ⬜ Parse video analysis response
- ⬜ Extract temporal data

**Day 8-9: Results Display**
- ⬜ Reuse existing radar chart
- ⬜ Display overall scores
- ⬜ Show findings
- ⬜ Progress indicators

**Day 10: Testing & Iteration**
- ⬜ Test with 5 sample videos
- ⬜ Validate scores
- ⬜ Fix bugs
- ⬜ Performance optimization

---

## Code Skeleton to Create

### 1. config.py

```python
# config.py
import os
from dataclasses import dataclass

@dataclass
class GCPConfig:
    """Google Cloud Platform configuration"""
    project_id: str = os.getenv("GCP_PROJECT_ID", "your-project-id")
    location: str = "us-central1"
    bucket_name: str = f"rai-video-temp-{project_id}"
    service_account_key: str = os.getenv("GOOGLE_APPLICATION_CREDENTIALS", "")

@dataclass
class VideoConfig:
    """Video processing configuration"""
    max_file_size_mb: int = 200
    max_duration_seconds: int = 180  # 3 minutes
    supported_formats: list = ("mp4", "mov", "avi")
    target_resolution: int = 720  # 720p optimal

    # Gemini model
    model_name: str = "gemini-1.5-flash-002"
    temperature: float = 0.4
    max_output_tokens: int = 4000

# Global config instances
gcp_config = GCPConfig()
video_config = VideoConfig()
```

### 2. video_utils.py

```python
# video_utils.py
import cv2
from typing import Dict, Tuple
import subprocess
import json

def get_video_metadata(video_path: str) -> Dict:
    """Extract video metadata using ffprobe"""
    cmd = [
        'ffprobe', '-v', 'quiet',
        '-print_format', 'json',
        '-show_format', '-show_streams',
        video_path
    ]

    result = subprocess.run(cmd, capture_output=True, text=True)
    metadata = json.loads(result.stdout)

    video_stream = next(s for s in metadata['streams'] if s['codec_type'] == 'video')

    return {
        'duration': float(metadata['format']['duration']),
        'size_mb': float(metadata['format']['size']) / (1024 * 1024),
        'width': video_stream['width'],
        'height': video_stream['height'],
        'fps': eval(video_stream['r_frame_rate']),
        'codec': video_stream['codec_name']
    }

def validate_video(video_path: str, max_size_mb: int = 200,
                   max_duration: int = 180) -> Tuple[bool, str]:
    """Validate video meets requirements"""
    try:
        metadata = get_video_metadata(video_path)

        if metadata['duration'] > max_duration:
            return False, f"Video too long: {metadata['duration']:.0f}s (max {max_duration}s)"

        if metadata['size_mb'] > max_size_mb:
            return False, f"File too large: {metadata['size_mb']:.1f}MB (max {max_size_mb}MB)"

        return True, "Valid"

    except Exception as e:
        return False, f"Error reading video: {str(e)}"

def extract_thumbnail(video_path: str, timestamp: float = 0) -> bytes:
    """Extract frame from video at timestamp"""
    cap = cv2.VideoCapture(video_path)

    # Seek to timestamp
    cap.set(cv2.CAP_PROP_POS_MSEC, timestamp * 1000)

    ret, frame = cap.read()
    cap.release()

    if not ret:
        raise ValueError(f"Could not extract frame at {timestamp}s")

    # Convert to bytes
    _, buffer = cv2.imencode('.jpg', frame)
    return buffer.tobytes()
```

### 3. video_processor.py

```python
# video_processor.py
import vertexai
from vertexai.generative_models import GenerativeModel, Part
from google.cloud import storage
import tempfile
import os
from typing import Dict
from config import gcp_config, video_config

class VideoAnalyzer:
    """Analyze video ads using Gemini 1.5 Flash"""

    def __init__(self):
        # Initialize Vertex AI
        vertexai.init(
            project=gcp_config.project_id,
            location=gcp_config.location
        )

        self.model = GenerativeModel(video_config.model_name)
        self.storage_client = storage.Client()

    def analyze_video(self, video_data: bytes, ad_copy: str = "") -> Dict:
        """Main analysis function"""

        # Determine upload method based on size
        size_mb = len(video_data) / (1024 * 1024)

        if size_mb <= 20:
            # Direct upload
            return self._analyze_direct(video_data, ad_copy)
        else:
            # Upload to GCS first
            return self._analyze_from_gcs(video_data, ad_copy)

    def _analyze_direct(self, video_data: bytes, ad_copy: str) -> Dict:
        """Analyze small video directly"""

        video_part = Part.from_data(video_data, mime_type="video/mp4")
        prompt = self._create_prompt(ad_copy)

        response = self.model.generate_content(
            [video_part, prompt],
            generation_config={
                "temperature": video_config.temperature,
                "max_output_tokens": video_config.max_output_tokens
            }
        )

        return self._parse_response(response.text)

    def _analyze_from_gcs(self, video_data: bytes, ad_copy: str) -> Dict:
        """Analyze large video via GCS"""

        # Upload to GCS
        gcs_uri = self._upload_to_gcs(video_data)

        # Create Part from URI
        video_part = Part.from_uri(gcs_uri, mime_type="video/mp4")
        prompt = self._create_prompt(ad_copy)

        response = self.model.generate_content(
            [video_part, prompt],
            generation_config={
                "temperature": video_config.temperature,
                "max_output_tokens": video_config.max_output_tokens
            }
        )

        return self._parse_response(response.text)

    def _upload_to_gcs(self, video_data: bytes) -> str:
        """Upload video to GCS and return URI"""
        import uuid

        bucket = self.storage_client.bucket(gcp_config.bucket_name)
        blob_name = f"uploads/{uuid.uuid4()}/video.mp4"
        blob = bucket.blob(blob_name)

        blob.upload_from_string(video_data, content_type="video/mp4")

        return f"gs://{gcp_config.bucket_name}/{blob_name}"

    def _create_prompt(self, ad_copy: str) -> str:
        """Create analysis prompt for video"""
        # Import existing framework
        from app import FRAMEWORK, detect_language

        detected_lang = detect_language(ad_copy) if ad_copy else 'en'

        prompt = f"""You are an expert in responsible advertising assessment.
Analyze this VIDEO advertisement across four key dimensions.

CRITICAL INSTRUCTIONS:
1. VISUAL ANALYSIS: Analyze all visual elements throughout the video
2. AUDIO ANALYSIS:
   - Transcribe all dialogue/voiceover
   - Analyze tone, music, sound effects
   - Detect language (appears to be {detected_lang})
3. TEMPORAL ANALYSIS:
   - Identify 3-5 key scenes/transitions
   - Note how messaging evolves over time
   - Flag contradictions between beginning and end
4. INTEGRATION:
   - Compare visual vs audio messaging
   - Flag mismatches or misleading combinations

Additional provided context: {ad_copy}

FRAMEWORK:
{json.dumps(FRAMEWORK, indent=2)}

Return JSON in this EXACT format:
{{
    "overall_score": <0-100>,
    "detected_language": "{detected_lang}",
    "duration_analyzed": "<video length in seconds>",
    "transcript": "full video transcription with timestamps",
    "dimensions": {{
        "Climate Responsibility": {{
            "score": <0-100>,
            "findings": ["finding 1", "finding 2", "finding 3"],
            "findings_hu": ["magyar megállapítás 1", "..."] // only if Hungarian
        }},
        "Social Responsibility": {{ ... same structure ... }},
        "Cultural Sensitivity": {{ ... same structure ... }},
        "Ethical Communication": {{ ... same structure ... }}
    }},
    "scenes": [
        {{
            "timestamp": "0:00-0:30",
            "description": "Opening scene description",
            "visual_elements": ["element 1", "element 2"],
            "audio_content": "What is said/heard",
            "climate_score": <0-100>,
            "social_score": <0-100>,
            "cultural_score": <0-100>,
            "ethical_score": <0-100>,
            "overall_scene_score": <0-100>
        }}
    ],
    "summary": {{
        "strengths": ["strength 1", "strength 2", "strength 3"],
        "strengths_hu": ["erősség 1", "..."],  // only if Hungarian
        "concerns": ["concern 1", "concern 2", "concern 3"],
        "concerns_hu": ["aggály 1", "..."],  // only if Hungarian
        "recommendations": ["rec 1", "rec 2", "rec 3"],
        "recommendations_hu": ["ajánlás 1", "..."]  // only if Hungarian
    }},
    "temporal_analysis": {{
        "messaging_evolution": "How the message changes over time",
        "key_moments": [
            {{"timestamp": "0:45", "event": "Disclaimer appears briefly"}},
            {{"timestamp": "1:30", "event": "Tone shift from empowering to manipulative"}}
        ],
        "audio_visual_alignment": "consistent" or "contradictory",
        "pacing_notes": "Analysis of timing and emphasis"
    }}
}}

Be specific and reference actual elements from the video."""

        return prompt

    def _parse_response(self, response_text: str) -> Dict:
        """Parse JSON from Gemini response"""
        import json

        # Handle markdown code blocks
        if "```json" in response_text:
            start = response_text.find("```json") + 7
            end = response_text.find("```", start)
            json_str = response_text[start:end].strip()
        elif "```" in response_text:
            start = response_text.find("```") + 3
            end = response_text.find("```", start)
            json_str = response_text[start:end].strip()
        else:
            start = response_text.find('{')
            end = response_text.rfind('}') + 1
            json_str = response_text[start:end]

        return json.loads(json_str)
```

---

## Next Immediate Steps

### 1. **You need to:**
   - [ ] Set up Google Cloud project (if not already)
   - [ ] Share PROJECT_ID with me
   - [ ] Enable Vertex AI API
   - [ ] Set up authentication (gcloud auth or service account)

### 2. **I will:**
   - [ ] Create the three core files (config.py, video_utils.py, video_processor.py)
   - [ ] Update app.py with video analysis tab
   - [ ] Update requirements.txt
   - [ ] Create test video generator
   - [ ] Test with sample videos

### 3. **We will:**
   - [ ] Test end-to-end with sample ads
   - [ ] Validate scores make sense
   - [ ] Iterate on prompt
   - [ ] Prepare for Phase 2

---

## Questions?

- **Need help with GCP setup?** I can guide you through each step
- **Want to see code first?** I can create the files now and test later
- **Prefer different approach?** Open to adjustments

**Ready to start coding when you are!** 🚀

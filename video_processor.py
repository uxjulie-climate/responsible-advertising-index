"""
Video analysis using Google Gemini 2.5 Flash.
"""

import google.generativeai as genai
import json
import time
from typing import Dict, Optional
from config import video_config
import tempfile
import os


class VideoAnalyzer:
    """Analyze video ads using Gemini 2.5 Flash"""

    def __init__(self, api_key: str):
        """
        Initialize the video analyzer.

        Args:
            api_key: Google AI API key
        """
        self.api_key = api_key
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel(video_config.model_name)

    def analyze_video(self, video_bytes: bytes, ad_copy: str = "",
                     detected_language: str = "en") -> Dict:
        """
        Analyze a video advertisement.

        Args:
            video_bytes: Video file as bytes
            ad_copy: Optional text description/copy from the ad
            detected_language: Language code ('en' or 'hu')

        Returns:
            Dictionary with analysis results
        """
        size_mb = len(video_bytes) / (1024 * 1024)

        # For large videos, use File API
        if size_mb > video_config.file_api_threshold_mb:
            return self._analyze_via_file_api(video_bytes, ad_copy, detected_language)
        else:
            return self._analyze_direct(video_bytes, ad_copy, detected_language)

    def _analyze_direct(self, video_bytes: bytes, ad_copy: str,
                       detected_language: str) -> Dict:
        """Analyze small video directly (< 20MB)"""

        # Write to temp file (Gemini needs a file path for video)
        with tempfile.NamedTemporaryFile(delete=False, suffix='.mp4') as tmp:
            tmp.write(video_bytes)
            tmp_path = tmp.name

        try:
            # Upload the video file
            video_file = genai.upload_file(path=tmp_path)

            # Wait for processing
            while video_file.state.name == "PROCESSING":
                time.sleep(1)
                video_file = genai.get_file(video_file.name)

            if video_file.state.name == "FAILED":
                raise ValueError("Video processing failed")

            # Create prompt
            prompt = self._create_prompt(ad_copy, detected_language)

            # Generate analysis
            response = self.model.generate_content(
                [video_file, prompt],
                generation_config={
                    "temperature": video_config.temperature,
                    "max_output_tokens": video_config.max_output_tokens
                }
            )

            # Delete the file from Google's servers
            genai.delete_file(video_file.name)

            return self._parse_response(response.text)

        finally:
            # Clean up temp file
            try:
                os.remove(tmp_path)
            except:
                pass

    def _analyze_via_file_api(self, video_bytes: bytes, ad_copy: str,
                              detected_language: str) -> Dict:
        """Analyze large video via File API (> 20MB)"""

        # Write to temp file
        with tempfile.NamedTemporaryFile(delete=False, suffix='.mp4') as tmp:
            tmp.write(video_bytes)
            tmp_path = tmp.name

        try:
            # Upload the video file
            print("Uploading video to Google's servers...")
            video_file = genai.upload_file(path=tmp_path)

            # Wait for processing
            print("Processing video...")
            while video_file.state.name == "PROCESSING":
                time.sleep(2)
                video_file = genai.get_file(video_file.name)

            if video_file.state.name == "FAILED":
                raise ValueError("Video processing failed")

            print("Analyzing video...")
            # Create prompt
            prompt = self._create_prompt(ad_copy, detected_language)

            # Generate analysis
            response = self.model.generate_content(
                [video_file, prompt],
                generation_config={
                    "temperature": video_config.temperature,
                    "max_output_tokens": video_config.max_output_tokens
                }
            )

            # Delete the file from Google's servers
            genai.delete_file(video_file.name)

            return self._parse_response(response.text)

        finally:
            # Clean up temp file
            try:
                os.remove(tmp_path)
            except:
                pass

    def _create_prompt(self, ad_copy: str, detected_language: str) -> str:
        """Create analysis prompt for video"""

        # Import framework from app.py
        try:
            from app import FRAMEWORK
        except:
            # Fallback if app.py not available
            FRAMEWORK = {
                "Climate Responsibility": {"hu_name": "Klímafelelősség"},
                "Social Responsibility": {"hu_name": "Társadalmi Felelősség"},
                "Cultural Sensitivity": {"hu_name": "Kulturális Érzékenység"},
                "Ethical Communication": {"hu_name": "Etikus Kommunikáció"}
            }

        bilingual = detected_language == 'hu'

        prompt = f"""You are an expert in responsible advertising assessment.
Analyze this VIDEO advertisement across four key dimensions.

CRITICAL INSTRUCTIONS FOR VIDEO ANALYSIS:

1. VISUAL ANALYSIS:
   - Watch the ENTIRE video carefully
   - Note all visual elements: people, products, environments, text overlays
   - Identify brand messages shown on screen
   - Look for greenwashing visual cues (nature imagery, green colors without substance)
   - Assess diversity and representation

2. AUDIO ANALYSIS:
   - Transcribe ALL dialogue and voiceover
   - Detect the language (appears to be {detected_language})
   - Note music, tone, and sound effects
   - Identify any audio claims or promises

3. TEMPORAL ANALYSIS:
   - Identify 3-5 key scenes/moments in the video
   - Note how messaging evolves from beginning to end
   - Flag any contradictions (e.g., empowering start, manipulative end)
   - Look for fast disclaimers or buried warnings

4. INTEGRATION:
   - Compare what's SHOWN vs. what's SAID
   - Flag mismatches between visual and audio messaging
   - Identify misleading combinations

Additional context provided: {ad_copy if ad_copy else "None"}

FRAMEWORK - Assess across these dimensions:
{json.dumps(FRAMEWORK, indent=2)}

Return JSON in this EXACT format:
{{
    "overall_score": <0-100>,
    "detected_language": "{detected_language}",
    "duration_analyzed": "<video length in seconds>",
    "transcript": "Full transcription with key timestamps like [0:15] Speaker: ...",
    "dimensions": {{
        "Climate Responsibility": {{
            "score": <0-100>,
            "findings": ["finding 1 with specific video evidence", "finding 2", "finding 3"],
            {"findings_hu": [\"magyar megállapítás 1\", \"...\"]," if bilingual else ""}
        }},
        "Social Responsibility": {{
            "score": <0-100>,
            "findings": ["finding 1", "finding 2", "finding 3"],
            {"findings_hu": [\"magyar megállapítás 1\", \"...\"]," if bilingual else ""}
        }},
        "Cultural Sensitivity": {{
            "score": <0-100>,
            "findings": ["finding 1", "finding 2", "finding 3"],
            {"findings_hu": [\"magyar megállapítás 1\", \"...\"]," if bilingual else ""}
        }},
        "Ethical Communication": {{
            "score": <0-100>,
            "findings": ["finding 1", "finding 2", "finding 3"],
            {"findings_hu": [\"magyar megállapítás 1\", \"...\"]," if bilingual else ""}
        }}
    }},
    "scenes": [
        {{
            "timestamp": "0:00-0:30",
            "description": "Opening scene description with visual and audio details",
            "visual_elements": ["element 1", "element 2"],
            "audio_content": "What is said or heard",
            "climate_score": <0-100>,
            "social_score": <0-100>,
            "cultural_score": <0-100>,
            "ethical_score": <0-100>,
            "overall_scene_score": <0-100>
        }}
    ],
    "summary": {{
        "strengths": ["strength 1 with video timestamp reference", "strength 2", "strength 3"],
        {"strengths_hu": [\"erősség 1\", \"...\"]," if bilingual else ""}
        "concerns": ["concern 1 with timestamp", "concern 2", "concern 3"],
        {"concerns_hu": [\"aggály 1\", \"...\"]," if bilingual else ""}
        "recommendations": ["recommendation 1", "recommendation 2", "recommendation 3"],
        {"recommendations_hu": [\"ajánlás 1\", \"...\"]" if bilingual else ""}
    }},
    "temporal_analysis": {{
        "messaging_evolution": "Describe how the message changes from beginning to end",
        "key_moments": [
            {{"timestamp": "0:45", "event": "Brief disclaimer appears"}},
            {{"timestamp": "1:30", "event": "Tone shifts from empowering to manipulative"}}
        ],
        "audio_visual_alignment": "consistent" or "contradictory",
        "pacing_notes": "Analysis of timing, emphasis, and what's rushed vs. highlighted"
    }}
}}

Be specific and reference ACTUAL elements from the video with timestamps."""

        return prompt

    def _parse_response(self, response_text: str) -> Dict:
        """Parse JSON from Gemini response"""

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
            # Find JSON object
            start = response_text.find('{')
            end = response_text.rfind('}') + 1
            if start == -1 or end == 0:
                raise ValueError("No JSON found in response")
            json_str = response_text[start:end]

        try:
            return json.loads(json_str)
        except json.JSONDecodeError as e:
            raise ValueError(f"Failed to parse JSON response: {e}\n\nResponse:\n{json_str[:500]}")

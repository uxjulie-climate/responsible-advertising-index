"""
Configuration settings for Responsible Advertising Index.
"""

from dataclasses import dataclass
from typing import List

@dataclass
class VideoConfig:
    """Video processing configuration"""
    # File size limits
    max_file_size_mb: int = 200
    max_duration_seconds: int = 180  # 3 minutes

    # Supported formats
    supported_formats: List[str] = None

    # Gemini model settings
    model_name: str = "gemini-2.5-flash"
    temperature: float = 0.4
    max_output_tokens: int = 8000  # Increased for video analysis

    # File API threshold (videos larger than this use File API)
    file_api_threshold_mb: int = 20

    def __post_init__(self):
        if self.supported_formats is None:
            self.supported_formats = ["mp4", "mov", "avi", "webm"]

# Global config instance
video_config = VideoConfig()

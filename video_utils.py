"""
Utility functions for video processing.
"""

import subprocess
import json
from typing import Dict, Tuple, Optional
import tempfile
import os

def get_video_metadata(video_bytes: bytes) -> Dict:
    """
    Extract video metadata using ffprobe.

    Args:
        video_bytes: Video file as bytes

    Returns:
        Dictionary with duration, size_mb, width, height, fps, codec
    """
    # Write to temp file for ffprobe
    with tempfile.NamedTemporaryFile(delete=False, suffix='.mp4') as tmp:
        tmp.write(video_bytes)
        tmp_path = tmp.name

    try:
        cmd = [
            'ffprobe', '-v', 'quiet',
            '-print_format', 'json',
            '-show_format', '-show_streams',
            tmp_path
        ]

        result = subprocess.run(cmd, capture_output=True, text=True)

        if result.returncode != 0:
            # If ffprobe fails, return basic info
            return {
                'duration': 0,
                'size_mb': len(video_bytes) / (1024 * 1024),
                'width': 0,
                'height': 0,
                'fps': 0,
                'codec': 'unknown'
            }

        metadata = json.loads(result.stdout)

        # Find video stream
        video_stream = None
        for stream in metadata.get('streams', []):
            if stream.get('codec_type') == 'video':
                video_stream = stream
                break

        if not video_stream:
            return {
                'duration': float(metadata.get('format', {}).get('duration', 0)),
                'size_mb': len(video_bytes) / (1024 * 1024),
                'width': 0,
                'height': 0,
                'fps': 0,
                'codec': 'unknown'
            }

        # Parse frame rate (can be "30/1" format)
        fps_str = video_stream.get('r_frame_rate', '0/1')
        try:
            num, den = fps_str.split('/')
            fps = float(num) / float(den) if float(den) != 0 else 0
        except:
            fps = 0

        return {
            'duration': float(metadata.get('format', {}).get('duration', 0)),
            'size_mb': len(video_bytes) / (1024 * 1024),
            'width': video_stream.get('width', 0),
            'height': video_stream.get('height', 0),
            'fps': fps,
            'codec': video_stream.get('codec_name', 'unknown')
        }

    finally:
        # Clean up temp file
        try:
            os.remove(tmp_path)
        except:
            pass


def validate_video(video_bytes: bytes, max_size_mb: int = 200,
                   max_duration: int = 180) -> Tuple[bool, str, Optional[Dict]]:
    """
    Validate video meets requirements.

    Args:
        video_bytes: Video file as bytes
        max_size_mb: Maximum file size in MB
        max_duration: Maximum duration in seconds

    Returns:
        Tuple of (is_valid, message, metadata)
    """
    try:
        metadata = get_video_metadata(video_bytes)

        if metadata['size_mb'] > max_size_mb:
            return False, f"File too large: {metadata['size_mb']:.1f}MB (max {max_size_mb}MB)", metadata

        if metadata['duration'] > max_duration:
            return False, f"Video too long: {metadata['duration']:.0f}s (max {max_duration}s)", metadata

        if metadata['duration'] == 0:
            return False, "Could not determine video duration (file may be corrupted)", metadata

        return True, "Valid", metadata

    except Exception as e:
        return False, f"Error reading video: {str(e)}", None


def format_duration(seconds: float) -> str:
    """
    Format duration in seconds to MM:SS format.

    Args:
        seconds: Duration in seconds

    Returns:
        Formatted string like "2:30"
    """
    mins = int(seconds // 60)
    secs = int(seconds % 60)
    return f"{mins}:{secs:02d}"


def estimate_cost(duration_seconds: float) -> float:
    """
    Estimate the cost of analyzing a video.

    Based on Gemini 2.5 Flash pricing:
    - ~$0.01 per minute of video

    Args:
        duration_seconds: Video duration in seconds

    Returns:
        Estimated cost in USD
    """
    minutes = duration_seconds / 60
    cost_per_minute = 0.01
    return minutes * cost_per_minute

"""
Ad scraping utilities for downloading videos from various platforms.
"""

import requests
import re
from typing import Optional, Dict
import subprocess
import tempfile
import os


class AdScraper:
    """Base class for ad scrapers"""

    @staticmethod
    def download_video(url: str, output_path: str) -> bool:
        """
        Download video from URL to output_path.
        Returns True if successful.
        """
        raise NotImplementedError


class LinkedInAdScraper(AdScraper):
    """
    Scrape videos from LinkedIn Ad Library.

    Note: LinkedIn ads are protected and require authentication.
    This scraper uses playwright/selenium to extract the video URL.
    """

    @staticmethod
    def extract_video_url(page_url: str) -> Optional[str]:
        """
        Extract video URL from LinkedIn Ad Library page.

        Args:
            page_url: LinkedIn ad library URL (e.g., https://www.linkedin.com/ad-library/detail/946953156)

        Returns:
            Direct video URL or None
        """
        # LinkedIn requires authentication - would need playwright/selenium
        # For now, return instructions
        print("❌ LinkedIn Ad Library requires manual download:")
        print(f"1. Visit: {page_url}")
        print("2. Right-click on video → 'Save Video As...'")
        print("3. Upload the downloaded file to RAI")
        return None

    @staticmethod
    def download_video(url: str, output_path: str) -> bool:
        """LinkedIn requires manual download"""
        LinkedInAdScraper.extract_video_url(url)
        return False


class MetaAdLibraryScraper(AdScraper):
    """
    Scrape videos from Meta (Facebook/Instagram) Ad Library.

    URL format: https://www.facebook.com/ads/library/?id=XXXXXXXXX
    """

    @staticmethod
    def extract_video_url(page_url: str) -> Optional[str]:
        """
        Extract video URL from Meta Ad Library page.

        Note: Meta Ad Library requires API access for automated downloads.
        For manual use, videos can be inspected via browser developer tools.
        """
        print("❌ Meta Ad Library requires manual download:")
        print(f"1. Visit: {page_url}")
        print("2. Open browser Developer Tools (F12)")
        print("3. Go to Network tab, filter by 'mp4'")
        print("4. Play the video and look for video URL")
        print("5. Right-click the mp4 request → Copy → Copy URL")
        print("6. Download using that URL")
        return None

    @staticmethod
    def download_video(url: str, output_path: str) -> bool:
        """Meta requires manual download or API access"""
        MetaAdLibraryScraper.extract_video_url(url)
        return False


class YouTubeScraper(AdScraper):
    """
    Download videos from YouTube using yt-dlp.

    Requires: pip install yt-dlp
    """

    @staticmethod
    def download_video(url: str, output_path: str) -> bool:
        """
        Download YouTube video using yt-dlp.

        Args:
            url: YouTube video URL
            output_path: Where to save the video

        Returns:
            True if successful
        """
        try:
            # Try multiple paths for yt-dlp
            yt_dlp_paths = [
                'yt-dlp',
                '/Users/julieschiller/Library/Python/3.9/bin/yt-dlp',
                'python3 -m yt_dlp'
            ]

            yt_dlp_cmd = None
            for cmd_path in yt_dlp_paths:
                try:
                    if cmd_path.startswith('python3'):
                        test_cmd = ['python3', '-m', 'yt_dlp', '--version']
                    else:
                        test_cmd = [cmd_path, '--version']

                    result = subprocess.run(test_cmd, capture_output=True)
                    if result.returncode == 0:
                        yt_dlp_cmd = cmd_path
                        break
                except:
                    continue

            if not yt_dlp_cmd:
                print("❌ yt-dlp not found. Install with: pip3 install yt-dlp")
                return False

            # Download video (max 720p, mp4 format)
            # Add custom user agent to avoid 403 errors
            user_agent = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36"

            if yt_dlp_cmd.startswith('python3'):
                cmd = [
                    'python3', '-m', 'yt_dlp',
                    url,
                    '-f', 'best[height<=720]',
                    '-o', output_path,
                    '--no-playlist',
                    '--user-agent', user_agent
                ]
            else:
                cmd = [
                    yt_dlp_cmd,
                    url,
                    '-f', 'best[height<=720]',
                    '-o', output_path,
                    '--no-playlist',
                    '--user-agent', user_agent
                ]

            result = subprocess.run(cmd, capture_output=True, text=True)
            if result.returncode == 0:
                print(f"✅ Video downloaded to: {output_path}")
                return True
            else:
                print(f"❌ Download failed: {result.stderr}")
                return False

        except Exception as e:
            print(f"❌ Error: {e}")
            return False


class VimeoScraper(AdScraper):
    """
    Download videos from Vimeo using yt-dlp.

    Vimeo videos can be downloaded using yt-dlp just like YouTube.
    """

    @staticmethod
    def download_video(url: str, output_path: str) -> bool:
        """
        Download Vimeo video using yt-dlp.

        Args:
            url: Vimeo video URL
            output_path: Where to save the video

        Returns:
            True if successful
        """
        # Use the same method as YouTube since yt-dlp supports both
        return YouTubeScraper.download_video(url, output_path)


class GoogleAdsScraper(AdScraper):
    """
    Scrape from Google Ads Transparency Center.

    URL format: https://adstransparency.google.com/advertiser/XXXXXXXXX
    """

    @staticmethod
    def extract_video_url(page_url: str) -> Optional[str]:
        """Google Ads requires manual inspection"""
        print("❌ Google Ads Transparency Center requires manual download:")
        print(f"1. Visit: {page_url}")
        print("2. Click on the ad creative")
        print("3. Right-click video → 'Save Video As...'")
        return None

    @staticmethod
    def download_video(url: str, output_path: str) -> bool:
        """Google Ads requires manual download"""
        GoogleAdsScraper.extract_video_url(url)
        return False


class DirectVideoScraper(AdScraper):
    """
    Download videos from direct URLs (MP4, MOV, etc.)
    """

    @staticmethod
    def download_video(url: str, output_path: str) -> bool:
        """
        Download video from direct URL.

        Args:
            url: Direct video URL (ending in .mp4, .mov, etc.)
            output_path: Where to save

        Returns:
            True if successful
        """
        try:
            print(f"⬇️ Downloading from: {url}")
            response = requests.get(url, stream=True, timeout=60)
            response.raise_for_status()

            with open(output_path, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)

            print(f"✅ Video downloaded to: {output_path}")
            return True

        except Exception as e:
            print(f"❌ Download failed: {e}")
            return False


def detect_platform(url: str) -> str:
    """
    Detect which platform the URL is from.

    Returns:
        'linkedin', 'meta', 'youtube', 'vimeo', 'google_ads', 'direct', or 'unknown'
    """
    url = url.lower()

    if 'linkedin.com/ad-library' in url:
        return 'linkedin'
    elif 'facebook.com/ads/library' in url or 'instagram.com' in url:
        return 'meta'
    elif 'youtube.com' in url or 'youtu.be' in url:
        return 'youtube'
    elif 'vimeo.com' in url:
        return 'vimeo'
    elif 'adstransparency.google.com' in url:
        return 'google_ads'
    elif url.endswith(('.mp4', '.mov', '.avi', '.webm')):
        return 'direct'
    else:
        return 'unknown'


def download_ad_video(url: str, output_path: Optional[str] = None) -> Optional[str]:
    """
    Automatically detect platform and download video.

    Args:
        url: Ad URL or direct video URL
        output_path: Optional output path. If None, creates temp file.

    Returns:
        Path to downloaded video, or None if failed
    """
    if output_path is None:
        # Create temp file
        temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.mp4')
        output_path = temp_file.name
        temp_file.close()

    platform = detect_platform(url)

    scrapers = {
        'linkedin': LinkedInAdScraper,
        'meta': MetaAdLibraryScraper,
        'youtube': YouTubeScraper,
        'vimeo': VimeoScraper,
        'google_ads': GoogleAdsScraper,
        'direct': DirectVideoScraper
    }

    if platform == 'unknown':
        print(f"❌ Unknown platform: {url}")
        print("Supported platforms:")
        print("  - YouTube (automated)")
        print("  - Vimeo (automated)")
        print("  - Direct video URLs (automated)")
        print("  - LinkedIn Ad Library (manual)")
        print("  - Meta Ad Library (manual)")
        print("  - Google Ads Transparency (manual)")
        return None

    scraper = scrapers[platform]
    success = scraper.download_video(url, output_path)

    if success:
        return output_path
    else:
        # Clean up temp file if download failed
        try:
            os.remove(output_path)
        except:
            pass
        return None


if __name__ == "__main__":
    # Test the scrapers
    import sys

    if len(sys.argv) < 2:
        print("Usage: python ad_scrapers.py <url>")
        print("\nExamples:")
        print("  python ad_scrapers.py https://www.youtube.com/watch?v=XXXXXXXXX")
        print("  python ad_scrapers.py https://www.linkedin.com/ad-library/detail/946953156")
        print("  python ad_scrapers.py https://example.com/video.mp4")
        sys.exit(1)

    url = sys.argv[1]
    result = download_ad_video(url, output_path="downloaded_ad.mp4")

    if result:
        print(f"\n✅ Success! Video saved to: {result}")
    else:
        print(f"\n❌ Failed to download video")

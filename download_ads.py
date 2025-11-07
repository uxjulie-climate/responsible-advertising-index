#!/usr/bin/env python3
"""
Interactive Ad Downloader
Downloads video ads from various platforms with guided instructions.
"""

import sys
import os
from ad_scrapers import download_ad_video, detect_platform
from pathlib import Path


def main():
    print("=" * 70)
    print("📹 Video Ad Downloader")
    print("=" * 70)
    print()

    # Get URL from user
    if len(sys.argv) > 1:
        url = sys.argv[1]
    else:
        url = input("Enter ad URL (or 'search' to find ads): ").strip()

    # Search mode
    if url.lower() == 'search':
        show_search_guide()
        return

    # Check for placeholder URL
    if 'VIDEO_ID' in url or 'XXXXXXXXX' in url or url.endswith('...'):
        print()
        print("❌ ERROR: You used a placeholder URL!")
        print()
        print("You entered:", url)
        print()
        print("That's just an EXAMPLE - you need to use a REAL YouTube URL.")
        print()
        print("📺 Try this real example:")
        print('   python3 download_ads.py "https://www.youtube.com/watch?v=cbP2N1BQdYc"')
        print()
        print("Or search YouTube for an ad and copy the REAL URL from your browser.")
        print()
        print("Need help finding ads? Run:")
        print("   python3 download_ads.py search")
        print()
        return

    # Detect platform
    platform = detect_platform(url)

    print(f"\n🔍 Detected platform: {platform.upper()}")
    print()

    # Create output directory
    output_dir = Path.cwd() / "downloaded_ads"
    output_dir.mkdir(exist_ok=True)

    # Generate output filename
    video_num = len(list(output_dir.glob("*.mp4"))) + 1
    output_path = output_dir / f"ad_{video_num:03d}.mp4"

    print(f"📁 Output directory: {output_dir}")
    print(f"📝 Output file: {output_path.name}")
    print()

    # Download
    if platform in ['youtube', 'direct']:
        print("⬇️ Starting automated download...")
        result = download_ad_video(url, str(output_path))

        if result:
            print()
            print("=" * 70)
            print(f"✅ SUCCESS! Video saved to: {result}")
            print("=" * 70)
            print()
            print("Next steps:")
            print("1. Run: ./start.sh")
            print("2. Go to 'Video Analysis' tab")
            print(f"3. Upload: {result}")
            print()
        else:
            print()
            print("❌ Download failed. See error messages above.")
            print()

    elif platform == 'linkedin':
        show_linkedin_instructions(url, output_path)

    elif platform == 'meta':
        show_meta_instructions(url, output_path)

    elif platform == 'google_ads':
        show_google_ads_instructions(url, output_path)

    else:
        print(f"❌ Unknown platform. Cannot download from: {url}")
        print()
        print("Supported platforms:")
        print("  ✅ YouTube (automated)")
        print("  ✅ Direct video URLs (automated)")
        print("  ⚠️  LinkedIn Ad Library (manual)")
        print("  ⚠️  Meta Ad Library (manual)")
        print("  ⚠️  Google Ads Transparency (manual)")
        print()


def show_search_guide():
    """Show guide for finding video ads"""
    print()
    print("=" * 70)
    print("🔍 Where to Find Video Ads")
    print("=" * 70)
    print()

    print("📺 YOUTUBE (Easiest - Automated Download)")
    print("-" * 70)
    print("Search YouTube for:")
    print('  • "telekom commercial 2024"')
    print('  • "sustainable fashion ad"')
    print('  • "[brand name] advertisement"')
    print()
    print("Then copy the video URL and run:")
    print('  python3 download_ads.py "https://youtube.com/watch?v=..."')
    print()

    print("💼 LINKEDIN AD LIBRARY (Manual Download)")
    print("-" * 70)
    print("1. Visit: https://www.linkedin.com/ad-library/")
    print("2. Search for brand or topic")
    print("3. Click on a video ad")
    print("4. Copy the URL")
    print("5. Run: python3 download_ads.py <URL>")
    print("   (Will show download instructions)")
    print()

    print("👥 META AD LIBRARY (Manual Download)")
    print("-" * 70)
    print("1. Visit: https://www.facebook.com/ads/library/")
    print("2. Search for brand or topic")
    print("3. Filter by 'Video' ads")
    print("4. Click on an ad")
    print("5. Copy the URL")
    print("6. Run: python3 download_ads.py <URL>")
    print()

    print("🔍 GOOGLE ADS TRANSPARENCY (Manual Download)")
    print("-" * 70)
    print("1. Visit: https://adstransparency.google.com/")
    print("2. Search for advertiser")
    print("3. Click on video ad")
    print("4. Copy the URL")
    print("5. Run: python3 download_ads.py <URL>")
    print()


def show_linkedin_instructions(url: str, output_path: Path):
    """Show LinkedIn download instructions"""
    print("=" * 70)
    print("💼 LINKEDIN AD LIBRARY - Manual Download Required")
    print("=" * 70)
    print()
    print(f"Ad URL: {url}")
    print()

    print("STEP-BY-STEP INSTRUCTIONS:")
    print("-" * 70)
    print()

    print("1️⃣  OPEN THE AD IN BROWSER:")
    print(f"   {url}")
    print()

    print("2️⃣  LOG IN TO LINKEDIN (if needed)")
    print()

    print("3️⃣  OPEN DEVELOPER TOOLS:")
    print("   • Mac: Cmd + Option + I")
    print("   • Windows/Linux: F12 or Ctrl + Shift + I")
    print()

    print("4️⃣  GO TO 'NETWORK' TAB:")
    print("   • Click on 'Network' in the DevTools")
    print("   • Clear existing requests (🚫 icon)")
    print()

    print("5️⃣  PLAY THE VIDEO:")
    print("   • Click play on the ad video")
    print("   • Watch the Network tab for new requests")
    print()

    print("6️⃣  FIND THE VIDEO FILE:")
    print("   • Look for large files (>1MB)")
    print("   • Filter by: 'mp4' OR 'video' OR 'm3u8' OR 'ts'")
    print("   • Common patterns:")
    print("     - *.mp4 (most common)")
    print("     - *.mov")
    print("     - *.m3u8 (streaming format)")
    print("     - blob: URLs")
    print("   • Sort by 'Size' column (largest files)")
    print("   • Right-click on it → 'Copy' → 'Copy URL'")
    print()

    print("7️⃣  DOWNLOAD THE VIDEO:")
    print("   • Option A: Paste URL in new tab → Right-click video → Save As")
    print("   • Option B: Use curl:")
    print(f'     curl -o "{output_path}" "PASTE_VIDEO_URL_HERE"')
    print()

    print("8️⃣  UPLOAD TO RAI:")
    print("   • Run: ./start.sh")
    print("   • Go to 'Video Analysis' tab")
    print(f"   • Upload: {output_path}")
    print()

    print("=" * 70)
    print("💡 TIP: If you can't find the .mp4, try refreshing the page")
    print("         and playing the video again while Network tab is open.")
    print("=" * 70)
    print()


def show_meta_instructions(url: str, output_path: Path):
    """Show Meta Ad Library download instructions"""
    print("=" * 70)
    print("👥 META AD LIBRARY - Manual Download Required")
    print("=" * 70)
    print()
    print(f"Ad URL: {url}")
    print()

    print("STEP-BY-STEP INSTRUCTIONS:")
    print("-" * 70)
    print()

    print("1️⃣  OPEN THE AD:")
    print(f"   {url}")
    print()

    print("2️⃣  OPEN DEVELOPER TOOLS:")
    print("   • Mac: Cmd + Option + I")
    print("   • Windows/Linux: F12")
    print()

    print("3️⃣  NETWORK TAB:")
    print("   • Click 'Network' tab")
    print("   • Filter by 'mp4' or 'video'")
    print()

    print("4️⃣  PLAY VIDEO:")
    print("   • Click play on the ad")
    print("   • Watch for .mp4 requests in Network tab")
    print()

    print("5️⃣  COPY VIDEO URL:")
    print("   • Right-click the .mp4 request")
    print("   • Copy → Copy URL")
    print()

    print("6️⃣  DOWNLOAD:")
    print(f'   curl -o "{output_path}" "PASTE_URL_HERE"')
    print()

    print("7️⃣  ANALYZE:")
    print("   • ./start.sh")
    print(f"   • Upload: {output_path}")
    print()


def show_google_ads_instructions(url: str, output_path: Path):
    """Show Google Ads download instructions"""
    print("=" * 70)
    print("🔍 GOOGLE ADS TRANSPARENCY - Manual Download")
    print("=" * 70)
    print()
    print(f"Ad URL: {url}")
    print()

    print("STEPS:")
    print("-" * 70)
    print("1. Open the URL in browser")
    print("2. Click on the video ad creative")
    print("3. Right-click on video → 'Save Video As...'")
    print(f"4. Save to: {output_path}")
    print("5. Upload to RAI Video Analysis tab")
    print()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 Cancelled by user")
        sys.exit(0)

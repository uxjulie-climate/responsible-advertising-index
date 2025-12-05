#!/usr/bin/env python3
"""
SIMPLE AD ANALYSIS PIPELINE
No more mapping nightmares. Just: URL → Download → Analyze → Store

Usage:
  python3 simple_pipeline.py analyze_url "https://youtube.com/..." "Brand Name" "Campaign Name"
  python3 simple_pipeline.py analyze_batch catalog.csv
"""

import os
import sys
import json
import hashlib
from pathlib import Path
from datetime import datetime
import pandas as pd

# Load environment
env_path = Path(__file__).parent / '.env'
if env_path.exists():
    with open(env_path) as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith('#') and '=' in line:
                key, value = line.split('=', 1)
                os.environ[key.strip()] = value.strip()

from video_processor import VideoAnalyzer
from ad_scrapers import download_ad_video

# Simple storage structure
STORAGE_DIR = Path('analysis_storage')
STORAGE_DIR.mkdir(exist_ok=True)

def generate_id(url: str) -> str:
    """Generate unique ID from URL"""
    return hashlib.md5(url.encode()).hexdigest()[:12]

def download_with_metadata(url: str, brand: str = "Unknown", campaign: str = "") -> dict:
    """
    Download video and immediately create metadata file
    Returns: {'id', 'video_path', 'metadata_path', 'url', 'brand', 'campaign'}
    """
    print(f"\n📥 Downloading: {url}")

    # Generate unique ID
    ad_id = generate_id(url)

    # Create storage directory for this ad
    ad_dir = STORAGE_DIR / ad_id
    ad_dir.mkdir(exist_ok=True)

    # Download video
    video_path = ad_dir / "video.mp4"

    print(f"  ID: {ad_id}")
    print(f"  Downloading to: {video_path}")

    success = download_ad_video(url, str(video_path))

    if not success or not video_path.exists():
        print("  ❌ Download failed")
        return None

    # Create metadata immediately
    metadata = {
        'id': ad_id,
        'url': url,
        'brand': brand,
        'campaign': campaign,
        'downloaded_at': datetime.now().isoformat(),
        'video_file': str(video_path),
        'status': 'downloaded'
    }

    metadata_path = ad_dir / "metadata.json"
    with open(metadata_path, 'w') as f:
        json.dump(metadata, f, indent=2)

    print(f"  ✅ Downloaded and saved metadata")

    return {
        'id': ad_id,
        'video_path': video_path,
        'metadata_path': metadata_path,
        'url': url,
        'brand': brand,
        'campaign': campaign
    }

def analyze_ad(ad_id: str = None, video_path: Path = None) -> dict:
    """
    Analyze a downloaded ad (by ID or direct path)
    Updates metadata file with results
    """
    api_key = os.getenv('GOOGLE_API_KEY')
    if not api_key:
        print("❌ GOOGLE_API_KEY not found in .env")
        return None

    # Load from ID if provided
    if ad_id:
        ad_dir = STORAGE_DIR / ad_id
        if not ad_dir.exists():
            print(f"❌ Ad {ad_id} not found")
            return None

        metadata_path = ad_dir / "metadata.json"
        with open(metadata_path, 'r') as f:
            metadata = json.load(f)

        video_path = Path(metadata['video_file'])

    if not video_path or not video_path.exists():
        print(f"❌ Video file not found: {video_path}")
        return None

    print(f"\n🤖 Analyzing: {video_path.name}")

    # Read video
    with open(video_path, 'rb') as f:
        video_bytes = f.read()

    # Analyze
    analyzer = VideoAnalyzer(api_key=api_key)

    # Simple ad copy (no assumptions about language)
    ad_copy = f"Brand: {metadata.get('brand', 'Unknown')}\nCampaign: {metadata.get('campaign', '')}"

    # Let AI detect language automatically
    result = analyzer.analyze_video(
        video_bytes=video_bytes,
        ad_copy=ad_copy,
        detected_language='auto'  # Will be overridden by actual detection
    )

    if not result or 'dimensions' not in result:
        print("  ❌ Analysis failed")
        return None

    # Extract scores
    dimensions = result.get('dimensions', {})
    climate_score = dimensions.get('Climate Responsibility', {}).get('score', 0)
    social_score = dimensions.get('Social Responsibility', {}).get('score', 0)
    cultural_score = dimensions.get('Cultural Sensitivity', {}).get('score', 0)
    ethical_score = dimensions.get('Ethical Communication', {}).get('score', 0)

    analysis_result = {
        'analyzed_at': datetime.now().isoformat(),
        'detected_language': result.get('detected_language', 'unknown'),
        'overall_score': result.get('overall_score', 0),
        'climate_score': climate_score,
        'social_score': social_score,
        'cultural_score': cultural_score,
        'ethical_score': ethical_score,
        'summary': result.get('summary', {}),
        'dimensions': dimensions,
        'transcript': result.get('transcript', ''),
        'duration': result.get('duration_analyzed', '')
    }

    # Update metadata with analysis
    if ad_id:
        metadata.update({
            'status': 'analyzed',
            'analysis': analysis_result
        })

        with open(metadata_path, 'w') as f:
            json.dump(metadata, f, indent=2, ensure_ascii=False)

    print(f"  ✅ Overall: {analysis_result['overall_score']}/100")
    print(f"     Language: {analysis_result['detected_language']}")
    print(f"     Climate: {climate_score}, Social: {social_score}, Cultural: {cultural_score}, Ethical: {ethical_score}")

    return analysis_result

def analyze_single_url(url: str, brand: str, campaign: str):
    """Download and analyze a single URL"""
    print("="*80)
    print("SIMPLE AD PIPELINE - Single URL")
    print("="*80)

    # Download
    download_result = download_with_metadata(url, brand, campaign)
    if not download_result:
        return

    # Analyze
    analyze_ad(ad_id=download_result['id'])

    print("\n" + "="*80)
    print(f"✅ Complete! Results stored in: {STORAGE_DIR / download_result['id']}")
    print("="*80)

def analyze_from_catalog(catalog_path: str, start_index: int = 0, max_count: int = None):
    """Download and analyze from a CSV catalog"""
    print("="*80)
    print("SIMPLE AD PIPELINE - Batch from Catalog")
    print("="*80)

    # Load catalog
    df = pd.read_csv(catalog_path)

    # Normalize column names to lowercase for consistency
    df.columns = df.columns.str.lower()

    if max_count:
        df = df.iloc[start_index:start_index+max_count]
    else:
        df = df.iloc[start_index:]

    print(f"\n📊 Processing {len(df)} ads (starting from index {start_index})")

    results = []

    for idx, row in df.iterrows():
        print(f"\n[{idx+1}/{len(df)}] Processing...")

        url = row['url']

        # Try to extract brand/campaign from title
        title = row.get('title', '')
        if '//' in title:
            parts = title.split('//')
            brand = parts[0].strip()
            campaign = parts[1].strip() if len(parts) > 1 else ''
        else:
            brand = title.split()[0] if title else "Unknown"
            campaign = title

        # Download
        download_result = download_with_metadata(url, brand, campaign)
        if not download_result:
            results.append({'id': None, 'status': 'download_failed', 'url': url})
            continue

        # Analyze
        analysis = analyze_ad(ad_id=download_result['id'])
        if not analysis:
            results.append({'id': download_result['id'], 'status': 'analysis_failed', 'url': url})
            continue

        results.append({
            'id': download_result['id'],
            'status': 'success',
            'url': url,
            'brand': brand,
            **analysis
        })

        # Small delay
        import time
        time.sleep(2)

    # Save summary
    summary_path = STORAGE_DIR / f"batch_summary_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    with open(summary_path, 'w') as f:
        json.dump(results, f, indent=2, ensure_ascii=False)

    print("\n" + "="*80)
    print(f"✅ Batch complete! Summary: {summary_path}")
    print(f"   Successful: {sum(1 for r in results if r['status'] == 'success')}/{len(results)}")
    print("="*80)

def export_all_results():
    """Export all analyzed ads to CSV"""
    print("\n📊 Exporting all results...")

    all_results = []

    for ad_dir in STORAGE_DIR.iterdir():
        if not ad_dir.is_dir():
            continue

        metadata_path = ad_dir / "metadata.json"
        if not metadata_path.exists():
            continue

        with open(metadata_path, 'r') as f:
            metadata = json.load(f)

        if 'analysis' not in metadata:
            continue

        analysis = metadata['analysis']

        all_results.append({
            'id': metadata['id'],
            'url': metadata['url'],
            'brand': metadata['brand'],
            'campaign': metadata['campaign'],
            'detected_language': analysis.get('detected_language'),
            'overall_score': analysis.get('overall_score'),
            'climate_score': analysis.get('climate_score'),
            'social_score': analysis.get('social_score'),
            'cultural_score': analysis.get('cultural_score'),
            'ethical_score': analysis.get('ethical_score'),
            'analyzed_at': analysis.get('analyzed_at')
        })

    if not all_results:
        print("  No analyzed ads found")
        return

    df = pd.DataFrame(all_results)
    export_path = STORAGE_DIR / f"all_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
    df.to_csv(export_path, index=False)

    print(f"  ✅ Exported {len(all_results)} ads to: {export_path}")

def main():
    if len(sys.argv) < 2:
        print("""
SIMPLE AD ANALYSIS PIPELINE
============================

Usage:
  # Analyze single URL
  python3 simple_pipeline.py url "https://youtube.com/..." "Brand" "Campaign"

  # Analyze from catalog (all)
  python3 simple_pipeline.py batch catalog.csv

  # Analyze from catalog (range)
  python3 simple_pipeline.py batch catalog.csv --start 0 --count 10

  # Export all results to CSV
  python3 simple_pipeline.py export

Storage:
  All data stored in: analysis_storage/
    ├── <ad_id>/
    │   ├── video.mp4
    │   └── metadata.json (includes analysis)
        """)
        return

    command = sys.argv[1]

    if command == "url":
        if len(sys.argv) < 3:
            print("❌ Usage: python3 simple_pipeline.py url <URL> [brand] [campaign]")
            return

        url = sys.argv[2]
        brand = sys.argv[3] if len(sys.argv) > 3 else "Unknown"
        campaign = sys.argv[4] if len(sys.argv) > 4 else ""

        analyze_single_url(url, brand, campaign)

    elif command == "batch":
        if len(sys.argv) < 3:
            print("❌ Usage: python3 simple_pipeline.py batch <catalog.csv> [--start N] [--count N]")
            return

        catalog_path = sys.argv[2]
        start = 0
        count = None

        if '--start' in sys.argv:
            start = int(sys.argv[sys.argv.index('--start') + 1])
        if '--count' in sys.argv:
            count = int(sys.argv[sys.argv.index('--count') + 1])

        analyze_from_catalog(catalog_path, start, count)

    elif command == "export":
        export_all_results()

    else:
        print(f"❌ Unknown command: {command}")

if __name__ == '__main__':
    main()

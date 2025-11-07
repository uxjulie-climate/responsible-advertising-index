#!/bin/bash
# Create a simple test advertisement video

echo "🎬 Creating test advertisement video..."

# Check if ffmpeg is installed
if ! command -v ffmpeg &> /dev/null; then
    echo "❌ ffmpeg not found. Install with: brew install ffmpeg"
    exit 1
fi

# Create output directory
mkdir -p test_videos

# Create a sustainable fashion ad
ffmpeg -f lavfi -i color=c=#2E7D32:s=1280x720:d=30 \
  -vf "drawtext=text='EcoThreads':fontsize=80:fontcolor=white:x=(w-text_w)/2:y=100,\
       drawtext=text='Sustainable Fashion':fontsize=50:fontcolor=white:x=(w-text_w)/2:y=250,\
       drawtext=text='100%% Organic Cotton':fontsize=40:fontcolor=#EEEEEE:x=(w-text_w)/2:y=350,\
       drawtext=text='Fair Trade Certified':fontsize=40:fontcolor=#EEEEEE:x=(w-text_w)/2:y=420,\
       drawtext=text='Lifetime Repair Guarantee':fontsize=40:fontcolor=#EEEEEE:x=(w-text_w)/2:y=490,\
       drawtext=text='#WearItOut':fontsize=35:fontcolor=#81C784:x=(w-text_w)/2:y=600" \
  -c:v libx264 -pix_fmt yuv420p -y test_videos/sustainable_fashion_ad.mp4 2>&1 | grep -v "deprecated"

echo ""
echo "✅ Test video created!"
echo ""
echo "📁 Location: test_videos/sustainable_fashion_ad.mp4"
echo "⏱️  Duration: 30 seconds"
echo "📐 Resolution: 1280x720"
echo ""
echo "Next steps:"
echo "1. Run: ./start.sh"
echo "2. Go to 'Video Analysis' tab"
echo "3. Upload: test_videos/sustainable_fashion_ad.mp4"
echo "4. Expected score: ~85-90 (sustainable messaging)"
echo ""

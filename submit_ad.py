"""
Responsible Advertising Index - Ad Submission Form
Public-facing form for stakeholders to submit ads for analysis.
"""

import streamlit as st
import google.generativeai as genai
from datetime import datetime
from pathlib import Path
import json
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Page configuration
st.set_page_config(
    page_title="Submit Ad for Analysis - RAI",
    page_icon="📊",
    layout="wide",
)

# Custom CSS
st.markdown("""
    <style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f1f1f;
        margin-bottom: 0.5rem;
    }
    .sub-header {
        font-size: 1.2rem;
        color: #666;
        margin-bottom: 2rem;
    }
    .info-box {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 1rem 0;
    }
    </style>
""", unsafe_allow_html=True)

# Header
st.markdown('<div class="main-header">📊 Submit Your Ad for Responsible Analysis</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-header">Get AI-powered insights on Climate, Social, Cultural, and Ethical responsibility</div>', unsafe_allow_html=True)

# Info box
st.markdown("""
<div class="info-box">
    <strong>What is RAI?</strong><br>
    The Responsible Advertising Index analyzes advertisements across four dimensions:
    <ul>
        <li>🌍 <strong>Climate Responsibility</strong> - Environmental claims and sustainability</li>
        <li>👥 <strong>Social Responsibility</strong> - Representation, inclusivity, and impact</li>
        <li>🎨 <strong>Cultural Sensitivity</strong> - Respect for diverse cultures and contexts</li>
        <li>✨ <strong>Ethical Communication</strong> - Transparency, honesty, and evidence</li>
    </ul>
    <strong>How to submit:</strong> Upload a file OR share a URL (YouTube, LinkedIn, Meta Ad Library, or direct links)
    <br>
    <em>Note: RAI is a research tool providing directional insights. Scores should be reviewed by experts before making major decisions.</em>
</div>
""", unsafe_allow_html=True)

# Create two columns for the form
col1, col2 = st.columns([2, 1])

with col1:
    st.subheader("1️⃣ About Your Ad")

    # Contact information
    contact_name = st.text_input(
        "Your Name *",
        help="Who is submitting this ad?"
    )

    contact_email = st.text_input(
        "Email Address *",
        help="We'll send the analysis results to this email"
    )

    # Advertiser information
    advertiser_name = st.text_input(
        "Advertiser / Brand Name *",
        help="Which company or brand is this ad for?"
    )

    industry = st.selectbox(
        "Industry",
        [
            "Select...",
            "Fashion & Apparel",
            "Food & Beverage",
            "Technology",
            "Automotive",
            "Healthcare",
            "Finance",
            "Retail",
            "Energy",
            "Travel & Tourism",
            "Other"
        ]
    )

    if industry == "Other":
        industry_other = st.text_input("Please specify industry")

    product_name = st.text_input(
        "Product / Campaign Name",
        help="Optional: What product or campaign is being advertised?"
    )

    st.subheader("2️⃣ Provide Your Ad")

    # Choose input method
    input_method = st.radio(
        "How would you like to provide the ad? *",
        ["Upload File", "Share URL"],
        horizontal=True,
        help="Upload a file directly or provide a URL to an online ad"
    )

    uploaded_file = None
    ad_url = None

    if input_method == "Upload File":
        ad_type = st.radio(
            "Ad Type *",
            ["Image", "Video"],
            horizontal=True
        )

        if ad_type == "Image":
            uploaded_file = st.file_uploader(
                "Upload Image Ad",
                type=["jpg", "jpeg", "png", "webp"],
                help="Maximum file size: 10MB"
            )
        else:
            uploaded_file = st.file_uploader(
                "Upload Video Ad",
                type=["mp4", "mov", "avi", "webm"],
                help="Maximum file size: 200MB, maximum duration: 3 minutes"
            )

    else:  # Share URL
        ad_url = st.text_input(
            "Ad URL *",
            placeholder="https://www.youtube.com/watch?v=...",
            help="Paste the URL to the ad (YouTube, LinkedIn, Meta Ad Library, or direct video/image link)"
        )

        if ad_url:
            # Detect platform and ad type from URL
            if "youtube.com" in ad_url or "youtu.be" in ad_url:
                st.info("🎥 YouTube video detected")
                ad_type = "Video"
            elif "linkedin.com" in ad_url:
                st.info("🎥 LinkedIn ad detected")
                ad_type = "Video"
            elif "facebook.com/ads" in ad_url or "facebook.com/ad_library" in ad_url:
                st.info("📱 Meta Ad Library detected")
                ad_type = "Video"  # Could be image or video
            elif ad_url.lower().endswith(('.jpg', '.jpeg', '.png', '.webp', '.gif')):
                st.info("🖼️ Image URL detected")
                ad_type = "Image"
            elif ad_url.lower().endswith(('.mp4', '.mov', '.avi', '.webm')):
                st.info("🎥 Video URL detected")
                ad_type = "Video"
            else:
                st.warning("⚠️ Could not auto-detect ad type. Please specify:")
                ad_type = st.radio("Ad Type", ["Image", "Video"], horizontal=True)
        else:
            ad_type = "Video"  # Default

    ad_copy = st.text_area(
        "Ad Copy / Text",
        help="Optional: Include any text that appears in or with the ad",
        height=100
    )

    st.subheader("3️⃣ Additional Context")

    ad_language = st.selectbox(
        "Primary Language",
        ["English", "Hungarian", "Other"]
    )

    ad_tone = st.selectbox(
        "Tone of Ad",
        [
            "Select...",
            "Serious / Informative",
            "Humorous / Light",
            "Satirical / Ironic",
            "Emotional / Inspirational",
            "Urgent / Promotional"
        ],
        help="This helps our AI understand the intended tone"
    )

    ad_intent = st.text_area(
        "What is this ad trying to achieve?",
        help="Optional: Brief description of the ad's purpose or message",
        height=80
    )

    submission_purpose = st.radio(
        "Purpose of Submission",
        [
            "Internal assessment",
            "Pre-launch review",
            "Competitive benchmarking",
            "Research / Education",
            "Other"
        ]
    )

    # Privacy settings
    st.subheader("4️⃣ Privacy & Usage")

    make_public = st.checkbox(
        "Include in public leaderboard (anonymous)",
        help="If checked, your ad will be included in aggregate statistics and rankings (brand name shown, but submitter details kept private)"
    )

    share_learnings = st.checkbox(
        "Allow use for research & best practices",
        help="If checked, anonymized insights from your ad may be used to improve RAI and teach others",
        value=True
    )

    # Terms acceptance
    agree_terms = st.checkbox(
        "I agree to the Terms of Use and Privacy Policy *",
        help="By submitting, you confirm you have rights to this ad content and agree to our analysis terms"
    )

with col2:
    st.subheader("📋 Submission Checklist")

    # Validate required fields
    has_ad = (uploaded_file is not None) or (ad_url and ad_url.strip())
    required_fields_complete = all([
        contact_name,
        contact_email,
        advertiser_name,
        has_ad,
        agree_terms
    ])

    st.markdown("""
    **Required Fields:**
    """)

    st.write("✅ Your name" if contact_name else "⬜ Your name")
    st.write("✅ Email address" if contact_email else "⬜ Email address")
    st.write("✅ Advertiser/brand" if advertiser_name else "⬜ Advertiser/brand")
    st.write("✅ Ad provided" if has_ad else "⬜ Ad (file or URL)")
    st.write("✅ Terms accepted" if agree_terms else "⬜ Terms accepted")

    st.markdown("---")

    st.markdown("""
    **What happens next?**

    1. ⚡ Your ad is analyzed (10-60 seconds)
    2. 📧 Results sent to your email
    3. 📊 Access detailed report
    4. 🔄 Optional: Revise and resubmit

    **Analysis includes:**
    - Overall responsibility score
    - Dimension-by-dimension breakdown
    - Specific findings with evidence
    - Actionable recommendations
    """)

    st.markdown("---")

    st.markdown("""
    **Cost:**
    - Image analysis: **Free** (research phase)
    - Video analysis: **Free** (research phase)

    <em>Future pricing will apply after research phase ends.</em>
    """, unsafe_allow_html=True)

# Submit button
st.markdown("---")

if st.button("🚀 Submit for Analysis", type="primary", disabled=not required_fields_complete):
    if not required_fields_complete:
        st.error("Please complete all required fields marked with *")
    else:
        with st.spinner("Processing your submission..."):
            # Create submissions directory
            submissions_dir = Path("submissions")
            submissions_dir.mkdir(exist_ok=True)

            # Generate unique ID
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            submission_id = f"{timestamp}_{advertiser_name.replace(' ', '_')}"

            # Handle file upload or URL
            file_path = None
            if uploaded_file:
                # Save uploaded file
                file_extension = uploaded_file.name.split(".")[-1]
                file_path = submissions_dir / f"{submission_id}.{file_extension}"
                with open(file_path, "wb") as f:
                    f.write(uploaded_file.getbuffer())

            # Create submission metadata
            submission_data = {
                "submission_id": submission_id,
                "timestamp": datetime.now().isoformat(),
                "contact": {
                    "name": contact_name,
                    "email": contact_email
                },
                "advertiser": {
                    "name": advertiser_name,
                    "industry": industry if industry != "Select..." else None,
                    "product": product_name if product_name else None
                },
                "ad": {
                    "type": ad_type.lower(),
                    "language": ad_language,
                    "tone": ad_tone if ad_tone != "Select..." else None,
                    "intent": ad_intent if ad_intent else None,
                    "copy": ad_copy if ad_copy else None,
                    "input_method": input_method.lower().replace(" ", "_"),  # "upload_file" or "share_url"
                    "file_path": str(file_path) if file_path else None,
                    "url": ad_url if ad_url else None
                },
                "submission": {
                    "purpose": submission_purpose,
                    "make_public": make_public,
                    "share_learnings": share_learnings
                },
                "status": "pending",
                "analysis_results": None
            }

            # Save submission metadata
            metadata_path = submissions_dir / f"{submission_id}_metadata.json"
            with open(metadata_path, "w") as f:
                json.dump(submission_data, f, indent=2)

            st.success("✅ Ad submitted successfully!")

            # Show different message based on input method
            if ad_url:
                source_info = f"**URL:** {ad_url}"
                processing_note = """
                **Note:** For URL submissions, we'll download the ad first and then analyze it.
                YouTube and other platform videos may take a few extra minutes to process.
                """
            else:
                source_info = f"**File:** {uploaded_file.name}"
                processing_note = """
                **Note:** This is currently a manual review queue. During business hours,
                we typically process submissions within 1-2 hours.
                """

            st.markdown(f"""
            **Submission ID:** `{submission_id}`

            {source_info}

            Your ad has been queued for analysis. You'll receive results at **{contact_email}** within the next hour.

            **What's happening now:**
            1. {'Downloading ad from URL' if ad_url else 'Your ad is in the analysis queue'}
            2. Our AI is reviewing it across all 4 dimensions
            3. A detailed report is being generated
            4. Results will be emailed to you with PDF and Excel exports

            Thank you for using the Responsible Advertising Index!
            """)

            # Show info about what to expect
            st.info(processing_note + "\n\nFor immediate analysis, contact us about API access.")

            # Optional: Display submission summary
            with st.expander("📋 View Submission Summary"):
                st.json(submission_data)

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #666; padding: 2rem 0;">
    <p><strong>Responsible Advertising Index</strong> | Research Tool v1.0</p>
    <p>Questions? Contact: <a href="mailto:rai@example.com">rai@example.com</a></p>
    <p><em>Built with transparency. Validated with science.</em></p>
</div>
""", unsafe_allow_html=True)

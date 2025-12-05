import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from pathlib import Path
import json

st.set_page_config(page_title="Individual Ads", page_icon="🔍", layout="wide")

# Load data
@st.cache_data
def load_all_data():
    data_dir = Path(__file__).parent.parent.parent
    datasets = {'cannes': None, 'hungarian': None}

    cannes_files = sorted(data_dir.glob('cannes_analysis_results_*.json'))
    if cannes_files:
        with open(cannes_files[-1], 'r', encoding='utf-8') as f:
            datasets['cannes'] = json.load(f)

    hungarian_files = sorted(data_dir.glob('hungarian_analysis_results_*.json'))
    if hungarian_files:
        with open(hungarian_files[-1], 'r', encoding='utf-8') as f:
            datasets['hungarian'] = json.load(f)

    return datasets

datasets = load_all_data()
cannes_ads = datasets['cannes'] or []
hungarian_ads = datasets['hungarian'] or []

# Header
st.title("🔍 Individual Ad Analysis")
st.markdown("Explore detailed findings for specific advertisements")

st.markdown("---")

# Dataset selection
dataset = st.radio("Select Dataset", ["🏆 Cannes Grand Prix", "🇭🇺 Hungarian 50-50 Lista"], horizontal=True)

is_cannes = "Cannes" in dataset
ads = cannes_ads if is_cannes else hungarian_ads

if not ads:
    st.warning(f"No {'Cannes' if is_cannes else 'Hungarian'} ads available!")
    st.stop()

# Ad selection
ad_options = []
for ad in ads:
    if is_cannes:
        label = f"{ad.get('brand', 'Unknown')} - {ad.get('title', '')[:60]}"
    else:
        label = f"{ad.get('title', '')[:60]}"
    ad_options.append(label)

selected_idx = st.selectbox("Select Ad", range(len(ads)), format_func=lambda i: ad_options[i])
ad = ads[selected_idx]

st.markdown("---")

# Ad details header
col1, col2, col3 = st.columns([2, 1, 1])

with col1:
    st.subheader(ad.get('brand', ad.get('title', '')[:40]))
    st.caption(ad.get('title', ''))

with col2:
    st.metric("Overall Score", f"{ad.get('overall_score', 0)}/100")

with col3:
    detected_lang = ad.get('detected_language', 'en')
    lang_label = "🇭🇺 Magyar" if detected_lang == 'hu' else "🇬🇧 English"
    st.metric("Language", lang_label)

st.markdown("---")

# Dimension scores
st.subheader("📊 Dimension Scores")

col1, col2, col3, col4 = st.columns(4)

dimensions = ad.get('dimensions', {})

with col1:
    climate_score = ad.get('climate_score', 0)
    st.metric("Climate Responsibility", f"{climate_score}/100")

with col2:
    social_score = ad.get('social_score', 0)
    st.metric("Social Responsibility", f"{social_score}/100")

with col3:
    cultural_score = ad.get('cultural_score', 0)
    st.metric("Cultural Sensitivity", f"{cultural_score}/100")

with col4:
    ethical_score = ad.get('ethical_score', 0)
    st.metric("Ethical Communication", f"{ethical_score}/100")

# Radar chart
fig = go.Figure()

categories = ['Climate', 'Social', 'Cultural', 'Ethical', 'Climate']
values = [climate_score, social_score, cultural_score, ethical_score, climate_score]

fig.add_trace(go.Scatterpolar(
    r=values,
    theta=categories,
    fill='toself',
    name=ad.get('brand', 'Ad'),
    line_color='#667eea',
    fillcolor='rgba(102, 126, 234, 0.3)'
))

fig.update_layout(
    polar=dict(
        radialaxis=dict(
            visible=True,
            range=[0, 100]
        )
    ),
    height=400
)

st.plotly_chart(fig, use_container_width=True)

st.markdown("---")

# Detailed findings
st.subheader("🔍 Detailed Findings")

# Check if bilingual
has_hungarian = detected_lang == 'hu'

if has_hungarian:
    lang_toggle = st.radio("Display Language", ["English", "Magyar"], horizontal=True)
    show_hungarian = lang_toggle == "Magyar"
else:
    show_hungarian = False

tabs = st.tabs(["Climate Responsibility", "Social Responsibility", "Cultural Sensitivity", "Ethical Communication"])

dimension_keys = ['Climate Responsibility', 'Social Responsibility', 'Cultural Sensitivity', 'Ethical Communication']

for tab, dim_key in zip(tabs, dimension_keys):
    with tab:
        dim_data = dimensions.get(dim_key, {})
        score = dim_data.get('score', 0)

        # Score display
        if score >= 80:
            st.success(f"### {score}/100 ⭐⭐⭐⭐⭐")
        elif score >= 60:
            st.warning(f"### {score}/100 ⭐⭐⭐⭐")
        else:
            st.error(f"### {score}/100 ⭐⭐⭐")

        # Findings
        if has_hungarian and show_hungarian and 'findings_hu' in dim_data:
            st.markdown("#### Főbb Megállapítások:")
            for finding in dim_data.get('findings_hu', []):
                st.markdown(f"• {finding}")

            with st.expander("Show English / Angol verzió"):
                for finding in dim_data.get('findings', []):
                    st.markdown(f"• {finding}")
        else:
            st.markdown("#### Key Findings:")
            for finding in dim_data.get('findings', []):
                st.markdown(f"• {finding}")

            if has_hungarian and 'findings_hu' in dim_data:
                with st.expander("Show Hungarian / Magyar verzió"):
                    for finding in dim_data.get('findings_hu', []):
                        st.markdown(f"• {finding}")

st.markdown("---")

# Summary
st.subheader("📝 Summary")

summary = ad.get('summary', {})

col1, col2, col3 = st.columns(3)

with col1:
    if has_hungarian and show_hungarian:
        st.markdown("#### ✅ Erősségek")
        strengths = summary.get('strengths_hu', summary.get('strengths', []))
    else:
        st.markdown("#### ✅ Strengths")
        strengths = summary.get('strengths', [])

    for strength in strengths[:5]:
        st.success(strength)

with col2:
    if has_hungarian and show_hungarian:
        st.markdown("#### ⚠️ Aggályok")
        concerns = summary.get('concerns_hu', summary.get('concerns', []))
    else:
        st.markdown("#### ⚠️ Concerns")
        concerns = summary.get('concerns', [])

    for concern in concerns[:5]:
        st.warning(concern)

with col3:
    if has_hungarian and show_hungarian:
        st.markdown("#### 💡 Ajánlások")
        recommendations = summary.get('recommendations_hu', summary.get('recommendations', []))
    else:
        st.markdown("#### 💡 Recommendations")
        recommendations = summary.get('recommendations', [])

    for rec in recommendations[:5]:
        st.info(rec)

st.markdown("---")

# Transcript
if ad.get('transcript'):
    st.subheader("📜 Full Transcript")

    with st.expander("Show Transcript"):
        st.text(ad.get('transcript', 'No transcript available'))

# Metadata
st.markdown("---")
st.subheader("ℹ️ Metadata")

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown(f"**Filename:** `{ad.get('filename', 'N/A')}`")
    st.markdown(f"**Duration:** {ad.get('duration_analyzed', 'N/A')}")

with col2:
    st.markdown(f"**Analyzed:** {ad.get('analyzed_at', 'N/A')[:10]}")
    if ad.get('award_category'):
        st.markdown(f"**Award:** {ad.get('award_category', 'N/A')}")

with col3:
    if ad.get('url'):
        st.markdown(f"**[View Original]({ad.get('url')})**")

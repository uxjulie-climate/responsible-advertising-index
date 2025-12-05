#!/usr/bin/env python3
"""
Responsible Advertising Index - Analysis Dashboard
Multi-page Streamlit app for exploring Cannes and Hungarian ad analysis results
"""

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from pathlib import Path
import json

# Page config
st.set_page_config(
    page_title="RAI Analysis Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        text-align: center;
        margin-bottom: 1rem;
    }
    .subtitle {
        font-size: 1.2rem;
        text-align: center;
        color: #666;
        margin-bottom: 2rem;
    }
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 20px;
        border-radius: 10px;
        color: white;
        text-align: center;
    }
    .stMetric {
        background-color: #f0f2f6;
        padding: 15px;
        border-radius: 8px;
    }
</style>
""", unsafe_allow_html=True)

# Load data
@st.cache_data
def load_all_data():
    """Load both Cannes and Hungarian analysis results"""
    data_dir = Path(__file__).parent.parent

    datasets = {
        'cannes': None,
        'hungarian': None
    }

    # Load Cannes data
    cannes_files = sorted(data_dir.glob('cannes_analysis_results_*.json'))
    if cannes_files:
        with open(cannes_files[-1], 'r', encoding='utf-8') as f:
            cannes_data = json.load(f)
            datasets['cannes'] = pd.DataFrame(cannes_data)

    # Load Hungarian data
    hungarian_files = sorted(data_dir.glob('hungarian_analysis_results_*.json'))
    if hungarian_files:
        with open(hungarian_files[-1], 'r', encoding='utf-8') as f:
            hungarian_data = json.load(f)
            datasets['hungarian'] = pd.DataFrame(hungarian_data)

    return datasets

try:
    datasets = load_all_data()
    cannes_df = datasets['cannes']
    hungarian_df = datasets['hungarian']

    has_cannes = cannes_df is not None and len(cannes_df) > 0
    has_hungarian = hungarian_df is not None and len(hungarian_df) > 0

except Exception as e:
    st.error(f"Error loading data: {e}")
    st.stop()

# Header
st.markdown('<div class="main-header">📊 Responsible Advertising Index</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Comparative Analysis Dashboard: Cannes Grand Prix vs Hungarian 50-50 Lista</div>', unsafe_allow_html=True)

st.markdown("---")

# Overview metrics
col1, col2, col3, col4 = st.columns(4)

with col1:
    total_ads = (len(cannes_df) if has_cannes else 0) + (len(hungarian_df) if has_hungarian else 0)
    st.metric("Total Ads Analyzed", f"{total_ads}", help="Combined Cannes + Hungarian ads")

with col2:
    cannes_count = len(cannes_df) if has_cannes else 0
    st.metric("Cannes Grand Prix", f"{cannes_count}", help="Award-winning international ads")

with col3:
    hungarian_count = len(hungarian_df) if has_hungarian else 0
    st.metric("Hungarian 50-50 Lista", f"{hungarian_count}", help="Top Hungarian ads from public vote")

with col4:
    if has_cannes and has_hungarian:
        avg_overall = pd.concat([cannes_df['overall_score'], hungarian_df['overall_score']]).mean()
    elif has_cannes:
        avg_overall = cannes_df['overall_score'].mean()
    elif has_hungarian:
        avg_overall = hungarian_df['overall_score'].mean()
    else:
        avg_overall = 0
    st.metric("Average Overall Score", f"{avg_overall:.1f}/100")

st.markdown("---")

# Quick comparison
st.header("📈 Quick Comparison")

if has_cannes and has_hungarian:
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("🏆 Cannes Grand Prix")
        cannes_avg = cannes_df[['overall_score', 'climate_score', 'social_score', 'cultural_score', 'ethical_score']].mean()

        fig = go.Figure(go.Bar(
            x=['Overall', 'Climate', 'Social', 'Cultural', 'Ethical'],
            y=[cannes_avg['overall_score'], cannes_avg['climate_score'],
               cannes_avg['social_score'], cannes_avg['cultural_score'], cannes_avg['ethical_score']],
            marker_color=['#667eea', '#48bb78', '#ed64a6', '#4299e1', '#f6ad55'],
            text=[f"{v:.1f}" for v in [cannes_avg['overall_score'], cannes_avg['climate_score'],
                                         cannes_avg['social_score'], cannes_avg['cultural_score'],
                                         cannes_avg['ethical_score']]],
            textposition='auto'
        ))
        fig.update_layout(
            yaxis_title="Average Score",
            yaxis_range=[0, 100],
            height=300,
            showlegend=False
        )
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.subheader("🇭🇺 Hungarian 50-50 Lista")
        hungarian_avg = hungarian_df[['overall_score', 'climate_score', 'social_score', 'cultural_score', 'ethical_score']].mean()

        fig = go.Figure(go.Bar(
            x=['Overall', 'Climate', 'Social', 'Cultural', 'Ethical'],
            y=[hungarian_avg['overall_score'], hungarian_avg['climate_score'],
               hungarian_avg['social_score'], hungarian_avg['cultural_score'], hungarian_avg['ethical_score']],
            marker_color=['#667eea', '#48bb78', '#ed64a6', '#4299e1', '#f6ad55'],
            text=[f"{v:.1f}" for v in [hungarian_avg['overall_score'], hungarian_avg['climate_score'],
                                         hungarian_avg['social_score'], hungarian_avg['cultural_score'],
                                         hungarian_avg['ethical_score']]],
            textposition='auto'
        ))
        fig.update_layout(
            yaxis_title="Average Score",
            yaxis_range=[0, 100],
            height=300,
            showlegend=False
        )
        st.plotly_chart(fig, use_container_width=True)

elif has_cannes:
    st.info("Hungarian analysis data not yet available. Only showing Cannes data.")
    cannes_avg = cannes_df[['overall_score', 'climate_score', 'social_score', 'cultural_score', 'ethical_score']].mean()

    fig = go.Figure(go.Bar(
        x=['Overall', 'Climate', 'Social', 'Cultural', 'Ethical'],
        y=[cannes_avg['overall_score'], cannes_avg['climate_score'],
           cannes_avg['social_score'], cannes_avg['cultural_score'], cannes_avg['ethical_score']],
        marker_color=['#667eea', '#48bb78', '#ed64a6', '#4299e1', '#f6ad55'],
        text=[f"{v:.1f}" for v in [cannes_avg['overall_score'], cannes_avg['climate_score'],
                                     cannes_avg['social_score'], cannes_avg['cultural_score'],
                                     cannes_avg['ethical_score']]],
        textposition='auto'
    ))
    fig.update_layout(
        yaxis_title="Average Score",
        yaxis_range=[0, 100],
        height=400
    )
    st.plotly_chart(fig, use_container_width=True)

elif has_hungarian:
    st.info("Cannes analysis data not yet available. Only showing Hungarian data.")
    hungarian_avg = hungarian_df[['overall_score', 'climate_score', 'social_score', 'cultural_score', 'ethical_score']].mean()

    fig = go.Figure(go.Bar(
        x=['Overall', 'Climate', 'Social', 'Cultural', 'Ethical'],
        y=[hungarian_avg['overall_score'], hungarian_avg['climate_score'],
           hungarian_avg['social_score'], hungarian_avg['cultural_score'], hungarian_avg['ethical_score']],
        marker_color=['#667eea', '#48bb78', '#ed64a6', '#4299e1', '#f6ad55'],
        text=[f"{v:.1f}" for v in [hungarian_avg['overall_score'], hungarian_avg['climate_score'],
                                     hungarian_avg['social_score'], hungarian_avg['cultural_score'],
                                     hungarian_avg['ethical_score']]],
        textposition='auto'
    ))
    fig.update_layout(
        yaxis_title="Average Score",
        yaxis_range=[0, 100],
        height=400
    )
    st.plotly_chart(fig, use_container_width=True)

st.markdown("---")

# Key insights
st.header("💡 Key Insights")

if has_cannes and has_hungarian:
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Differences")

        diff_overall = hungarian_avg['overall_score'] - cannes_avg['overall_score']
        diff_climate = hungarian_avg['climate_score'] - cannes_avg['climate_score']
        diff_social = hungarian_avg['social_score'] - cannes_avg['social_score']
        diff_cultural = hungarian_avg['cultural_score'] - cannes_avg['cultural_score']
        diff_ethical = hungarian_avg['ethical_score'] - cannes_avg['ethical_score']

        st.metric("Overall", f"{diff_overall:+.1f}",
                 delta_color="normal" if diff_overall > 0 else "inverse",
                 help="Hungarian vs Cannes")
        st.metric("Climate", f"{diff_climate:+.1f}",
                 delta_color="normal" if diff_climate > 0 else "inverse")
        st.metric("Social", f"{diff_social:+.1f}",
                 delta_color="normal" if diff_social > 0 else "inverse")
        st.metric("Cultural", f"{diff_cultural:+.1f}",
                 delta_color="normal" if diff_cultural > 0 else "inverse")
        st.metric("Ethical", f"{diff_ethical:+.1f}",
                 delta_color="normal" if diff_ethical > 0 else "inverse")

    with col2:
        st.subheader("Observations")

        observations = []

        if abs(diff_climate) > 10:
            winner = "Hungarian" if diff_climate > 0 else "Cannes"
            observations.append(f"🌍 **Climate:** {winner} ads score {abs(diff_climate):.1f} points higher")

        if abs(diff_social) > 10:
            winner = "Hungarian" if diff_social > 0 else "Cannes"
            observations.append(f"👥 **Social:** {winner} ads score {abs(diff_social):.1f} points higher")

        if abs(diff_cultural) > 10:
            winner = "Hungarian" if diff_cultural > 0 else "Cannes"
            observations.append(f"🌐 **Cultural:** {winner} ads score {abs(diff_cultural):.1f} points higher")

        if abs(diff_ethical) > 10:
            winner = "Hungarian" if diff_ethical > 0 else "Cannes"
            observations.append(f"⚖️ **Ethical:** {winner} ads score {abs(diff_ethical):.1f} points higher")

        if cannes_avg['overall_score'] > hungarian_avg['overall_score']:
            observations.append(f"⭐ Cannes Grand Prix ads score **{diff_overall:.1f} points higher** overall")
        else:
            observations.append(f"⭐ Hungarian 50-50 Lista ads score **{abs(diff_overall):.1f} points higher** overall")

        for obs in observations:
            st.markdown(obs)

st.markdown("---")

# Navigation guidance
st.header("🗺️ Navigation")

st.markdown("""
Use the sidebar to explore:

- **🏆 Cannes Overview** - Detailed analysis of Cannes Grand Prix ads
- **🇭🇺 Hungarian Overview** - Detailed analysis of Hungarian 50-50 Lista ads
- **⚖️ Comparison** - Side-by-side comparison with interactive charts
- **🔍 Individual Ads** - Drill down into specific ads with full transcripts

""")

# Footer
st.markdown("---")
st.caption("📊 Responsible Advertising Index Dashboard | Data updated: " +
          (cannes_df.iloc[0]['analyzed_at'][:10] if has_cannes else
           hungarian_df.iloc[0]['analyzed_at'][:10] if has_hungarian else "N/A"))

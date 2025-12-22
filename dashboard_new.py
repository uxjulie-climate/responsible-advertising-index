#!/usr/bin/env python3
"""
Responsible Advertising Index - Production Dashboard
Load analyzed ads from analysis_storage/ with video playback
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from pathlib import Path
import json

# Page config
st.set_page_config(
    page_title="Responsible Advertising Index",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-title {font-size: 2.5rem; font-weight: bold; margin-bottom: 1rem;}
    .metric-card {background: #f0f2f6; padding: 1rem; border-radius: 0.5rem; margin: 0.5rem 0;}
    .score-excellent {color: #28a745; font-weight: bold;}
    .score-good {color: #5cb85c; font-weight: bold;}
    .score-moderate {color: #ffc107; font-weight: bold;}
    .score-poor {color: #fd7e14; font-weight: bold;}
    .score-bad {color: #dc3545; font-weight: bold;}
</style>
""", unsafe_allow_html=True)

@st.cache_data
def load_data():
    """Load analyzed ads from analysis_storage"""
    storage_path = Path('analysis_storage')

    if not storage_path.exists():
        st.error("analysis_storage/ folder not found!")
        return pd.DataFrame()

    results = []

    for ad_dir in storage_path.iterdir():
        if not ad_dir.is_dir():
            continue

        metadata_file = ad_dir / 'metadata.json'
        if not metadata_file.exists():
            continue

        with open(metadata_file, 'r') as f:
            data = json.load(f)

        # Handle both old format (nested under 'analysis') and new format (direct keys)
        if 'analysis' in data:
            # Old format
            analysis = data['analysis']
            overall_score = analysis.get('overall_score', 0)
            climate_score = analysis.get('climate_score', 0)
            social_score = analysis.get('social_score', 0)
            cultural_score = analysis.get('cultural_score', 0)
            ethical_score = analysis.get('ethical_score', 0)
            detected_language = analysis.get('detected_language', 'unknown')
            transcript = analysis.get('transcript', '')
            summary = analysis.get('summary', {})
            dimensions = analysis.get('dimensions', {})
            analyzed_at = analysis.get('analyzed_at', '')
        elif 'overall_score' in data and 'dimensions' in data:
            # New format
            overall_score = data.get('overall_score', 0)
            dimensions = data.get('dimensions', {})
            climate_score = dimensions.get('Climate Responsibility', {}).get('score', 0)
            social_score = dimensions.get('Social Responsibility', {}).get('score', 0)
            cultural_score = dimensions.get('Cultural Sensitivity', {}).get('score', 0)
            ethical_score = dimensions.get('Ethical Communication', {}).get('score', 0)
            detected_language = data.get('detected_language', 'unknown')
            transcript = data.get('transcript', '')
            summary = data.get('summary', {})
            analyzed_at = data.get('analyzed_at', '')
        else:
            # Skip if no valid analysis data
            continue

        # Flatten data for DataFrame
        results.append({
            'id': data.get('id', ad_dir.name),
            'url': data.get('url', ''),
            'brand': data.get('brand', 'Unknown'),
            'campaign': data.get('campaign', ''),
            'video_path': str(ad_dir / 'video.mp4'),
            'detected_language': detected_language,
            'overall_score': overall_score,
            'climate_score': climate_score,
            'social_score': social_score,
            'cultural_score': cultural_score,
            'ethical_score': ethical_score,
            'transcript': transcript,
            'summary': summary,
            'dimensions': dimensions,
            'analyzed_at': analyzed_at
        })

    if not results:
        st.warning("No analyzed ads found in analysis_storage/")
        return pd.DataFrame()

    df = pd.DataFrame(results)

    # Add grade column
    def get_grade(score):
        if score >= 95: return 'A+'
        elif score >= 90: return 'A'
        elif score >= 85: return 'A-'
        elif score >= 80: return 'B+'
        elif score >= 75: return 'B'
        elif score >= 70: return 'B-'
        elif score >= 65: return 'C+'
        elif score >= 60: return 'C'
        elif score >= 55: return 'C-'
        elif score >= 50: return 'D'
        else: return 'F'

    df['grade'] = df['overall_score'].apply(get_grade)

    return df

def score_color(score):
    """Get color class for score"""
    if score >= 80: return "score-excellent"
    elif score >= 65: return "score-good"
    elif score >= 50: return "score-moderate"
    elif score >= 35: return "score-poor"
    else: return "score-bad"

def main():
    st.markdown('<div class="main-title">📊 Responsible Advertising Index</div>', unsafe_allow_html=True)

    # Load data
    df = load_data()

    if df.empty:
        st.stop()

    # Sidebar filters
    st.sidebar.header("🔍 Filters")

    # Language filter
    languages = ['All'] + sorted(df['detected_language'].unique().tolist())
    selected_lang = st.sidebar.selectbox("Language", languages)

    # Score range filter
    score_range = st.sidebar.slider(
        "Overall Score Range",
        min_value=0,
        max_value=100,
        value=(0, 100)
    )

    # Grade filter
    grades = ['All'] + sorted(df['grade'].unique().tolist(),
                             key=lambda x: ['A+','A','A-','B+','B','B-','C+','C','C-','D','F'].index(x))
    selected_grade = st.sidebar.selectbox("Grade", grades)

    # Brand search
    brand_search = st.sidebar.text_input("Search Brand/Campaign")

    # Apply filters
    filtered_df = df.copy()

    if selected_lang != 'All':
        filtered_df = filtered_df[filtered_df['detected_language'] == selected_lang]

    filtered_df = filtered_df[
        (filtered_df['overall_score'] >= score_range[0]) &
        (filtered_df['overall_score'] <= score_range[1])
    ]

    if selected_grade != 'All':
        filtered_df = filtered_df[filtered_df['grade'] == selected_grade]

    if brand_search:
        filtered_df = filtered_df[
            filtered_df['brand'].str.contains(brand_search, case=False, na=False) |
            filtered_df['campaign'].str.contains(brand_search, case=False, na=False)
        ]

    # Summary metrics
    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:
        st.metric("Total Ads", len(filtered_df))
    with col2:
        avg_score = filtered_df['overall_score'].mean()
        st.metric("Avg Overall", f"{avg_score:.1f}/100")
    with col3:
        st.metric("Avg Climate", f"{filtered_df['climate_score'].mean():.1f}/100")
    with col4:
        st.metric("Avg Social", f"{filtered_df['social_score'].mean():.1f}/100")
    with col5:
        st.metric("Languages", filtered_df['detected_language'].nunique())

    st.divider()

    # Tabs
    tab1, tab2, tab3 = st.tabs(["📺 Browse Ads", "📊 Analytics", "🏆 Top & Bottom"])

    with tab1:
        st.subheader(f"Showing {len(filtered_df)} ads")

        # Sort options
        sort_col1, sort_col2 = st.columns([3, 1])
        with sort_col1:
            sort_by = st.selectbox(
                "Sort by",
                ['overall_score', 'climate_score', 'social_score', 'cultural_score', 'ethical_score', 'brand'],
                index=0
            )
        with sort_col2:
            sort_order = st.radio("Order", ['Descending', 'Ascending'], horizontal=True)

        sorted_df = filtered_df.sort_values(
            by=sort_by,
            ascending=(sort_order == 'Ascending')
        )

        # Display ads in grid
        for idx, row in sorted_df.iterrows():
            with st.expander(
                f"**{row['brand']}** - {row['campaign'][:60]} | "
                f"Score: {row['overall_score']}/100 ({row['grade']}) | "
                f"{row['detected_language'].upper()}"
            ):
                col_video, col_details = st.columns([1, 1])

                with col_video:
                    video_path = Path(row['video_path'])
                    if video_path.exists():
                        st.video(str(video_path))
                    else:
                        st.error("Video file not found")

                    st.markdown(f"[🔗 Watch on YouTube]({row['url']})")

                with col_details:
                    st.markdown(f"### Scores")

                    # Overall score
                    st.markdown(
                        f"<div class='{score_color(row['overall_score'])}'>"
                        f"Overall: {row['overall_score']}/100 ({row['grade']})"
                        f"</div>",
                        unsafe_allow_html=True
                    )

                    # Dimension scores
                    score_cols = st.columns(4)
                    with score_cols[0]:
                        st.metric("🌱 Climate", f"{row['climate_score']}/100")
                    with score_cols[1]:
                        st.metric("👥 Social", f"{row['social_score']}/100")
                    with score_cols[2]:
                        st.metric("🎨 Cultural", f"{row['cultural_score']}/100")
                    with score_cols[3]:
                        st.metric("⚖️ Ethical", f"{row['ethical_score']}/100")

                    # Radar chart
                    fig = go.Figure()

                    fig.add_trace(go.Scatterpolar(
                        r=[row['climate_score'], row['social_score'],
                           row['cultural_score'], row['ethical_score']],
                        theta=['Climate', 'Social', 'Cultural', 'Ethical'],
                        fill='toself',
                        name=row['brand']
                    ))

                    fig.update_layout(
                        polar=dict(
                            radialaxis=dict(visible=True, range=[0, 100])
                        ),
                        showlegend=False,
                        height=250
                    )

                    st.plotly_chart(fig, use_container_width=True)

                    # Transcript
                    if row['transcript']:
                        with st.expander("📝 Transcript"):
                            st.text(row['transcript'])

    with tab2:
        st.subheader("📊 Analytics Dashboard")

        # Score distribution
        col1, col2 = st.columns(2)

        with col1:
            fig = px.histogram(
                filtered_df,
                x='overall_score',
                nbins=20,
                title="Overall Score Distribution",
                labels={'overall_score': 'Overall Score', 'count': 'Number of Ads'}
            )
            st.plotly_chart(fig, use_container_width=True)

        with col2:
            fig = px.pie(
                filtered_df,
                names='grade',
                title="Grade Distribution",
                hole=0.4
            )
            st.plotly_chart(fig, use_container_width=True)

        # Dimension comparison
        dimension_avg = pd.DataFrame({
            'Dimension': ['Climate', 'Social', 'Cultural', 'Ethical'],
            'Average Score': [
                filtered_df['climate_score'].mean(),
                filtered_df['social_score'].mean(),
                filtered_df['cultural_score'].mean(),
                filtered_df['ethical_score'].mean()
            ]
        })

        fig = px.bar(
            dimension_avg,
            x='Dimension',
            y='Average Score',
            title="Average Scores by Dimension",
            color='Average Score',
            color_continuous_scale='RdYlGn'
        )
        st.plotly_chart(fig, use_container_width=True)

        # Language breakdown
        lang_counts = filtered_df['detected_language'].value_counts().reset_index()
        lang_counts.columns = ['Language', 'Count']

        fig = px.bar(
            lang_counts,
            x='Language',
            y='Count',
            title="Ads by Language"
        )
        st.plotly_chart(fig, use_container_width=True)

    with tab3:
        st.subheader("🏆 Top Performers")

        top_n = st.slider("Show top/bottom N ads", 5, 20, 10)

        col1, col2 = st.columns(2)

        with col1:
            st.markdown("### 🏆 Highest Scoring")
            top_ads = filtered_df.nlargest(top_n, 'overall_score')

            for idx, row in top_ads.iterrows():
                st.markdown(
                    f"**{row['overall_score']}/100** - {row['brand']} - {row['campaign'][:40]}"
                )

        with col2:
            st.markdown("### ⚠️ Lowest Scoring")
            bottom_ads = filtered_df.nsmallest(top_n, 'overall_score')

            for idx, row in bottom_ads.iterrows():
                st.markdown(
                    f"**{row['overall_score']}/100** - {row['brand']} - {row['campaign'][:40]}"
                )

        st.divider()

        # Climate leaders
        st.markdown("### 🌱 Climate Responsibility Leaders")
        climate_leaders = filtered_df.nlargest(10, 'climate_score')[
            ['brand', 'campaign', 'climate_score', 'overall_score']
        ]
        st.dataframe(climate_leaders, use_container_width=True)

if __name__ == "__main__":
    main()

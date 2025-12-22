#!/usr/bin/env python3
"""
Responsible Advertising Index - Enhanced Dashboard
With advanced filters, deep analysis, and colleague sharing
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from pathlib import Path
import json
import numpy as np

# Page config
st.set_page_config(
    page_title="Responsible Advertising Index",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Enhanced CSS
st.markdown("""
<style>
    .main-title {font-size: 2.5rem; font-weight: bold; margin-bottom: 1rem; color: #1f77b4;}
    .subtitle {font-size: 1.2rem; color: #666; margin-bottom: 2rem;}
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 1.5rem;
        border-radius: 10px;
        margin: 0.5rem 0;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    .insight-box {
        background: #f8f9fa;
        border-left: 4px solid #1f77b4;
        padding: 1rem;
        margin: 1rem 0;
        border-radius: 4px;
    }
    .score-excellent {color: #28a745; font-weight: bold; font-size: 1.2rem;}
    .score-good {color: #5cb85c; font-weight: bold; font-size: 1.2rem;}
    .score-moderate {color: #ffc107; font-weight: bold; font-size: 1.2rem;}
    .score-poor {color: #fd7e14; font-weight: bold; font-size: 1.2rem;}
    .score-bad {color: #dc3545; font-weight: bold; font-size: 1.2rem;}
    .stTabs [data-baseweb="tab-list"] {gap: 2rem;}
    .stTabs [data-baseweb="tab"] {
        padding: 1rem 2rem;
        font-size: 1.1rem;
    }
</style>
""", unsafe_allow_html=True)

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

        # Flatten data
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

    # Add category classification
    def categorize_ad(row):
        # Check if all scores are zero (failed analysis)
        if (row['overall_score'] == 0 and row['climate_score'] == 0 and
            row['social_score'] == 0 and row['social_score'] == 0 and
            row['ethical_score'] == 0):
            return 'Failed'

        # Check if stakeholder or reklamgyujto first
        if 'stakeholder' in row['id'] or 'reklamgyujto_extracted' in row['url']:
            return 'Reklámgyűjtő'

        # Check if Hungarian language
        if row['detected_language'] and 'hu' in str(row['detected_language']).lower():
            return '50-50lista'
        else:
            return 'Cannes Lions'

    df['category'] = df.apply(categorize_ad, axis=1)

    # Filter out failed analyses
    df = df[df['category'] != 'Failed']

    # Add derived columns
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

    # Add performance categories
    df['climate_category'] = pd.cut(df['climate_score'],
                                    bins=[0, 20, 50, 80, 100],
                                    labels=['Poor', 'Moderate', 'Good', 'Excellent'])
    df['social_category'] = pd.cut(df['social_score'],
                                   bins=[0, 50, 70, 85, 100],
                                   labels=['Poor', 'Moderate', 'Good', 'Excellent'])

    # Language groups
    df['language_group'] = df['detected_language'].apply(
        lambda x: 'Hungarian' if x == 'hu' else
                 'English' if x == 'en' else
                 'Other'
    )

    return df

def score_color(score):
    """Get color class for score"""
    if score >= 80: return "score-excellent"
    elif score >= 65: return "score-good"
    elif score >= 50: return "score-moderate"
    elif score >= 35: return "score-poor"
    else: return "score-bad"

def generate_insights(df):
    """Generate automated insights from the data"""
    insights = []

    # Check if dataframe is empty
    if len(df) == 0:
        insights.append("📊 **No data matches current filters** - Try adjusting your filter criteria")
        return insights

    # Climate gap
    climate_high = len(df[df['climate_score'] >= 80])
    climate_pct = (climate_high / len(df)) * 100
    insights.append(f"🌱 **Climate Gap:** Only {climate_high} ads ({climate_pct:.0f}%) score 80+ on climate responsibility")

    # Top performer
    if len(df) > 0:
        top_ad = df.nlargest(1, 'overall_score').iloc[0]
        insights.append(f"🏆 **Top Performer:** {top_ad['brand']} with {top_ad['overall_score']}/100")

    # Language diversity
    lang_count = df['detected_language'].nunique()
    insights.append(f"🌍 **Linguistic Diversity:** {lang_count} languages detected across campaigns")

    # Social excellence
    social_high = len(df[df['social_score'] >= 80])
    social_pct = (social_high / len(df)) * 100
    insights.append(f"👥 **Social Excellence:** {social_high} ads ({social_pct:.0f}%) score 80+ on social responsibility")

    return insights

def main():
    # Header
    st.markdown('<div class="main-title">📊 Responsible Advertising Index</div>', unsafe_allow_html=True)
    st.markdown('<div class="subtitle">AI-Powered Analysis of Advertising Responsibility</div>', unsafe_allow_html=True)

    # Load data
    df = load_data()

    if df.empty:
        st.stop()

    # Sidebar - Enhanced Filters
    st.sidebar.header("🔍 Advanced Filters")

    # Navigation link
    st.sidebar.markdown("---")
    st.sidebar.markdown("### 🔗 Navigation")
    st.sidebar.markdown("📤 [Upload & Analyze New Ads](http://localhost:8501)")
    st.sidebar.markdown("---")

    # Category filter
    st.sidebar.subheader("📂 Category")
    categories = ['All'] + sorted(df['category'].unique().tolist())
    selected_category = st.sidebar.selectbox("Ad Category", categories)

    # Quick filters
    st.sidebar.subheader("Quick Filters")
    quick_filter = st.sidebar.radio(
        "Show",
        ["All Ads", "Top Performers (80+)", "Climate Leaders", "Social Champions",
         "Hungarian Ads", "English Ads", "Needs Improvement (<50)"],
        index=0
    )

    st.sidebar.divider()

    # Language filter
    st.sidebar.subheader("Language")
    languages = ['All'] + sorted(df['detected_language'].unique().tolist())
    selected_lang = st.sidebar.selectbox("Detected Language", languages)

    # Score filters
    st.sidebar.subheader("Score Ranges")
    overall_range = st.sidebar.slider("Overall Score", 0, 100, (0, 100))
    climate_range = st.sidebar.slider("Climate Score", 0, 100, (0, 100))
    social_range = st.sidebar.slider("Social Score", 0, 100, (0, 100))
    cultural_range = st.sidebar.slider("Cultural Score", 0, 100, (0, 100))
    ethical_range = st.sidebar.slider("Ethical Score", 0, 100, (0, 100))

    # Grade filter
    st.sidebar.subheader("Performance")
    grades = ['All'] + sorted(df['grade'].unique().tolist(),
                             key=lambda x: ['A+','A','A-','B+','B','B-','C+','C','C-','D','F'].index(x) if x in ['A+','A','A-','B+','B','B-','C+','C','C-','D','F'] else 99)
    selected_grade = st.sidebar.selectbox("Grade", grades)

    # Brand search
    st.sidebar.subheader("Search")
    brand_search = st.sidebar.text_input("Brand/Campaign Name")

    # Advanced filters
    with st.sidebar.expander("🎯 Advanced Filters"):
        climate_cat = st.multiselect(
            "Climate Category",
            options=df['climate_category'].dropna().unique().tolist(),
            default=df['climate_category'].dropna().unique().tolist()
        )

        social_cat = st.multiselect(
            "Social Category",
            options=df['social_category'].dropna().unique().tolist(),
            default=df['social_category'].dropna().unique().tolist()
        )

    # Apply category filter first
    filtered_df = df.copy()

    if selected_category != 'All':
        filtered_df = filtered_df[filtered_df['category'] == selected_category]

    # Apply quick filter
    if quick_filter == "Top Performers (80+)":
        filtered_df = filtered_df[filtered_df['overall_score'] >= 80]
    elif quick_filter == "Climate Leaders":
        filtered_df = filtered_df.nlargest(20, 'climate_score')
    elif quick_filter == "Social Champions":
        filtered_df = filtered_df.nlargest(20, 'social_score')
    elif quick_filter == "Hungarian Ads":
        filtered_df = filtered_df[filtered_df['detected_language'] == 'hu']
    elif quick_filter == "English Ads":
        filtered_df = filtered_df[filtered_df['detected_language'] == 'en']
    elif quick_filter == "Needs Improvement (<50)":
        filtered_df = filtered_df[filtered_df['overall_score'] < 50]

    # Apply other filters
    if selected_lang != 'All':
        filtered_df = filtered_df[filtered_df['detected_language'] == selected_lang]

    filtered_df = filtered_df[
        (filtered_df['overall_score'] >= overall_range[0]) &
        (filtered_df['overall_score'] <= overall_range[1]) &
        (filtered_df['climate_score'] >= climate_range[0]) &
        (filtered_df['climate_score'] <= climate_range[1]) &
        (filtered_df['social_score'] >= social_range[0]) &
        (filtered_df['social_score'] <= social_range[1]) &
        (filtered_df['cultural_score'] >= cultural_range[0]) &
        (filtered_df['cultural_score'] <= cultural_range[1]) &
        (filtered_df['ethical_score'] >= ethical_range[0]) &
        (filtered_df['ethical_score'] <= ethical_range[1])
    ]

    if selected_grade != 'All':
        filtered_df = filtered_df[filtered_df['grade'] == selected_grade]

    if brand_search:
        filtered_df = filtered_df[
            filtered_df['brand'].str.contains(brand_search, case=False, na=False) |
            filtered_df['campaign'].str.contains(brand_search, case=False, na=False)
        ]

    if climate_cat:
        filtered_df = filtered_df[filtered_df['climate_category'].isin(climate_cat)]

    if social_cat:
        filtered_df = filtered_df[filtered_df['social_category'].isin(social_cat)]

    # Category Breakdown
    if selected_category == 'All':
        st.markdown("### 📊 Three-Category Analysis")
        cat_cols = st.columns(3)

        for idx, category in enumerate(['Cannes Lions', '50-50lista', 'Reklámgyűjtő']):
            cat_df = df[df['category'] == category]
            with cat_cols[idx]:
                st.markdown(f"**{category}**")
                st.metric("Ads", len(cat_df))
                if len(cat_df) > 0:
                    st.metric("Avg Score", f"{cat_df['overall_score'].mean():.1f}")
                else:
                    st.metric("Avg Score", "N/A")

        st.divider()

    # Key Metrics Row
    col1, col2, col3, col4, col5, col6 = st.columns(6)

    with col1:
        st.metric("📊 Total Ads", len(filtered_df), delta=f"{len(filtered_df)-len(df)}" if len(filtered_df) != len(df) else None)
    with col2:
        if len(filtered_df) > 0:
            avg_score = filtered_df['overall_score'].mean()
            st.metric("⭐ Avg Overall", f"{avg_score:.1f}", delta=f"{avg_score-df['overall_score'].mean():.1f}")
        else:
            st.metric("⭐ Avg Overall", "N/A")
    with col3:
        if len(filtered_df) > 0:
            st.metric("🌱 Avg Climate", f"{filtered_df['climate_score'].mean():.1f}")
        else:
            st.metric("🌱 Avg Climate", "N/A")
    with col4:
        if len(filtered_df) > 0:
            st.metric("👥 Avg Social", f"{filtered_df['social_score'].mean():.1f}")
        else:
            st.metric("👥 Avg Social", "N/A")
    with col5:
        if len(filtered_df) > 0:
            st.metric("🎨 Avg Cultural", f"{filtered_df['cultural_score'].mean():.1f}")
        else:
            st.metric("🎨 Avg Cultural", "N/A")
    with col6:
        if len(filtered_df) > 0:
            st.metric("⚖️ Avg Ethical", f"{filtered_df['ethical_score'].mean():.1f}")
        else:
            st.metric("⚖️ Avg Ethical", "N/A")

    # Auto Insights
    st.markdown("### 💡 Key Insights")
    insights = generate_insights(filtered_df)
    insight_cols = st.columns(len(insights))
    for idx, insight in enumerate(insights):
        with insight_cols[idx]:
            st.markdown(f'<div class="insight-box">{insight}</div>', unsafe_allow_html=True)

    st.divider()

    # Main Tabs
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "📺 Browse Ads",
        "📊 Analytics Dashboard",
        "🔬 Deep Dive Analysis",
        "🏆 Rankings",
        "📥 Export & Share"
    ])

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

        sorted_df = filtered_df.sort_values(by=sort_by, ascending=(sort_order == 'Ascending'))

        # Display ads
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

                    # Overall score with color
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
                        polar=dict(radialaxis=dict(visible=True, range=[0, 100])),
                        showlegend=False,
                        height=250
                    )

                    st.plotly_chart(fig, use_container_width=True)

                    # Transcript
                    if row['transcript']:
                        with st.expander("📝 View Transcript"):
                            st.text(row['transcript'])

                    # Summary: Strengths, Concerns, Recommendations
                    summary = row['summary'] if 'summary' in row and row['summary'] else {}
                    if summary and isinstance(summary, dict):
                        st.markdown("### 📋 Analysis Summary")

                        # Determine language - check for Hungarian
                        detected_lang = str(row.get('detected_language', '')).lower()
                        is_hungarian = 'hu' in detected_lang

                        # Strengths
                        strengths_key = 'strengths_hu' if is_hungarian else 'strengths'
                        strengths = summary.get(strengths_key, summary.get('strengths', []))
                        if strengths and len(strengths) > 0:
                            st.markdown("#### ✅ Strengths")
                            for strength in strengths:
                                st.markdown(f"- {strength}")

                        # Concerns
                        concerns_key = 'concerns_hu' if is_hungarian else 'concerns'
                        concerns = summary.get(concerns_key, summary.get('concerns', []))
                        if concerns and len(concerns) > 0:
                            st.markdown("#### ⚠️ Concerns")
                            for concern in concerns:
                                st.markdown(f"- {concern}")

                        # Recommendations
                        recommendations_key = 'recommendations_hu' if is_hungarian else 'recommendations'
                        recommendations = summary.get(recommendations_key, summary.get('recommendations', []))
                        if recommendations and len(recommendations) > 0:
                            st.markdown("#### 💡 Recommendations")
                            for rec in recommendations:
                                st.markdown(f"- {rec}")

    with tab2:
        st.subheader("📊 Analytics Dashboard")

        # Category comparison (if all categories shown)
        if selected_category == 'All' and len(filtered_df) > 0:
            st.markdown("### 📊 Category Comparison")
            st.caption(f"Based on {len(filtered_df)} filtered ads")

            # Category scores comparison
            category_stats = []
            for category in ['Cannes Lions', '50-50lista', 'Reklámgyűjtő']:
                cat_df = filtered_df[filtered_df['category'] == category]
                if len(cat_df) > 0:
                    category_stats.append({
                        'Category': category,
                        'Count': len(cat_df),
                        'Overall': cat_df['overall_score'].mean(),
                        'Climate': cat_df['climate_score'].mean(),
                        'Social': cat_df['social_score'].mean(),
                        'Cultural': cat_df['cultural_score'].mean(),
                        'Ethical': cat_df['ethical_score'].mean()
                    })

            if category_stats:
                cat_comparison = pd.DataFrame(category_stats)

                fig = px.bar(
                    cat_comparison,
                    x='Category',
                    y='Overall',
                    title="Average Overall Score by Category",
                    color='Overall',
                    color_continuous_scale='RdYlGn',
                    text='Overall'
                )
                fig.update_traces(texttemplate='%{text:.1f}', textposition='outside')
                st.plotly_chart(fig, use_container_width=True)

                # Dimension comparison by category
                dimension_comparison = cat_comparison.melt(
                    id_vars=['Category'],
                    value_vars=['Climate', 'Social', 'Cultural', 'Ethical'],
                    var_name='Dimension',
                    value_name='Score'
                )

                fig = px.bar(
                    dimension_comparison,
                    x='Dimension',
                    y='Score',
                    color='Category',
                    barmode='group',
                    title="Dimension Scores by Category"
                )
                st.plotly_chart(fig, use_container_width=True)

            st.divider()

        # Score distributions
        col1, col2 = st.columns(2)

        with col1:
            fig = px.histogram(
                filtered_df,
                x='overall_score',
                nbins=20,
                title="Overall Score Distribution",
                labels={'overall_score': 'Overall Score', 'count': 'Number of Ads'},
                color_discrete_sequence=['#1f77b4']
            )
            st.plotly_chart(fig, use_container_width=True)

        with col2:
            fig = px.pie(
                filtered_df,
                names='grade',
                title="Grade Distribution",
                hole=0.4,
                color_discrete_sequence=px.colors.sequential.RdBu
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
            color_continuous_scale='RdYlGn',
            text='Average Score'
        )
        fig.update_traces(texttemplate='%{text:.1f}', textposition='outside')
        st.plotly_chart(fig, use_container_width=True)

        # Language breakdown
        col1, col2 = st.columns(2)

        with col1:
            lang_counts = filtered_df['detected_language'].value_counts().reset_index()
            lang_counts.columns = ['Language', 'Count']

            fig = px.bar(
                lang_counts,
                x='Language',
                y='Count',
                title="Ads by Language",
                color='Count',
                color_continuous_scale='viridis'
            )
            st.plotly_chart(fig, use_container_width=True)

        with col2:
            # Scatter: Climate vs Social
            fig = px.scatter(
                filtered_df,
                x='climate_score',
                y='social_score',
                size='overall_score',
                color='grade',
                hover_data=['brand', 'campaign'],
                title="Climate vs Social Responsibility",
                labels={'climate_score': 'Climate Score', 'social_score': 'Social Score'}
            )
            st.plotly_chart(fig, use_container_width=True)

    with tab3:
        st.subheader("🔬 Deep Dive Analysis")

        # Correlation matrix
        st.markdown("### Dimension Correlations")
        corr_data = filtered_df[['climate_score', 'social_score', 'cultural_score', 'ethical_score', 'overall_score']]
        corr_matrix = corr_data.corr()

        fig = px.imshow(
            corr_matrix,
            labels=dict(color="Correlation"),
            x=['Climate', 'Social', 'Cultural', 'Ethical', 'Overall'],
            y=['Climate', 'Social', 'Cultural', 'Ethical', 'Overall'],
            color_continuous_scale='RdBu_r',
            aspect="auto",
            title="Score Correlation Heatmap"
        )
        st.plotly_chart(fig, use_container_width=True)

        # Statistical summary
        st.markdown("### Statistical Summary")
        summary_stats = filtered_df[['overall_score', 'climate_score', 'social_score', 'cultural_score', 'ethical_score']].describe()
        st.dataframe(summary_stats.style.format("{:.1f}"), use_container_width=True)

        # Box plots
        col1, col2 = st.columns(2)

        with col1:
            fig = px.box(
                filtered_df,
                y=['climate_score', 'social_score', 'cultural_score', 'ethical_score'],
                title="Score Distribution by Dimension",
                labels={'value': 'Score', 'variable': 'Dimension'}
            )
            st.plotly_chart(fig, use_container_width=True)

        with col2:
            # Language comparison
            fig = px.box(
                filtered_df,
                x='language_group',
                y='overall_score',
                title="Scores by Language Group",
                color='language_group'
            )
            st.plotly_chart(fig, use_container_width=True)

    with tab4:
        st.subheader("🏆 Rankings & Leaderboards")

        # Top performers
        col1, col2 = st.columns(2)

        with col1:
            st.markdown("### 🏆 Top 10 Overall")
            top10 = filtered_df.nlargest(10, 'overall_score')[
                ['brand', 'campaign', 'overall_score', 'grade']
            ].reset_index(drop=True)
            top10.index = top10.index + 1
            st.dataframe(top10, use_container_width=True)

        with col2:
            st.markdown("### ⚠️ Bottom 10 Overall")
            bottom10 = filtered_df.nsmallest(10, 'overall_score')[
                ['brand', 'campaign', 'overall_score', 'grade']
            ].reset_index(drop=True)
            bottom10.index = bottom10.index + 1
            st.dataframe(bottom10, use_container_width=True)

        # Dimension leaders
        st.markdown("### 📊 Dimension Leaders")

        dim_cols = st.columns(4)

        with dim_cols[0]:
            st.markdown("**🌱 Climate Top 5**")
            climate_top = filtered_df.nlargest(5, 'climate_score')[['brand', 'climate_score']]
            for idx, row in climate_top.iterrows():
                st.write(f"{row['climate_score']:.0f} - {row['brand'][:30]}")

        with dim_cols[1]:
            st.markdown("**👥 Social Top 5**")
            social_top = filtered_df.nlargest(5, 'social_score')[['brand', 'social_score']]
            for idx, row in social_top.iterrows():
                st.write(f"{row['social_score']:.0f} - {row['brand'][:30]}")

        with dim_cols[2]:
            st.markdown("**🎨 Cultural Top 5**")
            cultural_top = filtered_df.nlargest(5, 'cultural_score')[['brand', 'cultural_score']]
            for idx, row in cultural_top.iterrows():
                st.write(f"{row['cultural_score']:.0f} - {row['brand'][:30]}")

        with dim_cols[3]:
            st.markdown("**⚖️ Ethical Top 5**")
            ethical_top = filtered_df.nlargest(5, 'ethical_score')[['brand', 'ethical_score']]
            for idx, row in ethical_top.iterrows():
                st.write(f"{row['ethical_score']:.0f} - {row['brand'][:30]}")

    with tab5:
        st.subheader("📥 Export & Share")

        st.markdown("### Download Filtered Data")

        # Prepare export data
        export_df = filtered_df[[
            'category', 'brand', 'campaign', 'url', 'detected_language', 'grade',
            'overall_score', 'climate_score', 'social_score', 'cultural_score', 'ethical_score'
        ]].copy()

        # Add rank
        export_df = export_df.sort_values('overall_score', ascending=False)
        export_df.insert(0, 'rank', range(1, len(export_df) + 1))

        csv = export_df.to_csv(index=False)

        st.download_button(
            label="📥 Download as CSV",
            data=csv,
            file_name="rai_filtered_results.csv",
            mime="text/csv"
        )

        st.markdown("### Share Dashboard")
        st.info("""
        **To share with colleagues:**

        1. Find your local IP address:
           ```
           ifconfig | grep "inet " | grep -v 127.0.0.1
           ```

        2. Share this URL with colleagues on the same network:
           ```
           http://YOUR_IP_ADDRESS:8502
           ```

        3. Or use the easy script:
           ```bash
           ./start_dashboard.sh --share
           ```
        """)

        # Show current access URL
        st.markdown("### Current Access")
        st.code("http://localhost:8502")
        st.caption("⚠️ Only accessible from this computer. Use network sharing above for colleague access.")

if __name__ == "__main__":
    main()

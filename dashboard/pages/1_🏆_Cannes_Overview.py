import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from pathlib import Path
import json

st.set_page_config(page_title="Cannes Overview", page_icon="🏆", layout="wide")

# Load data
@st.cache_data
def load_cannes_data():
    data_dir = Path(__file__).parent.parent.parent
    cannes_files = sorted(data_dir.glob('cannes_analysis_results_*.json'))
    if cannes_files:
        with open(cannes_files[-1], 'r', encoding='utf-8') as f:
            return pd.DataFrame(json.load(f))
    return None

df = load_cannes_data()

if df is None or len(df) == 0:
    st.error("No Cannes analysis data found!")
    st.stop()

# Header
st.title("🏆 Cannes Grand Prix Analysis")
st.markdown(f"**{len(df)} ads analyzed** from award-winning international campaigns")

st.markdown("---")

# Summary metrics
col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    avg_overall = df['overall_score'].mean()
    st.metric("Overall Score", f"{avg_overall:.1f}/100")

with col2:
    avg_climate = df['climate_score'].mean()
    st.metric("Climate", f"{avg_climate:.1f}/100",
             delta=f"{avg_climate - avg_overall:.1f}",
             delta_color="off")

with col3:
    avg_social = df['social_score'].mean()
    st.metric("Social", f"{avg_social:.1f}/100",
             delta=f"{avg_social - avg_overall:.1f}",
             delta_color="off")

with col4:
    avg_cultural = df['cultural_score'].mean()
    st.metric("Cultural", f"{avg_cultural:.1f}/100",
             delta=f"{avg_cultural - avg_overall:.1f}",
             delta_color="off")

with col5:
    avg_ethical = df['ethical_score'].mean()
    st.metric("Ethical", f"{avg_ethical:.1f}/100",
             delta=f"{avg_ethical - avg_overall:.1f}",
             delta_color="off")

st.markdown("---")

# Visualization tabs
tab1, tab2, tab3, tab4 = st.tabs(["📊 All Ads", "📈 Distribution", "🎯 Radar Chart", "🏅 Rankings"])

with tab1:
    st.subheader("All Cannes Ads - Score Breakdown")

    # Create bar chart showing all ads
    fig = go.Figure()

    fig.add_trace(go.Bar(
        name='Climate',
        x=df['brand'],
        y=df['climate_score'],
        marker_color='#48bb78'
    ))
    fig.add_trace(go.Bar(
        name='Social',
        x=df['brand'],
        y=df['social_score'],
        marker_color='#ed64a6'
    ))
    fig.add_trace(go.Bar(
        name='Cultural',
        x=df['brand'],
        y=df['cultural_score'],
        marker_color='#4299e1'
    ))
    fig.add_trace(go.Bar(
        name='Ethical',
        x=df['brand'],
        y=df['ethical_score'],
        marker_color='#f6ad55'
    ))

    fig.update_layout(
        barmode='group',
        title="Dimension Scores by Brand",
        xaxis_title="Brand",
        yaxis_title="Score",
        yaxis_range=[0, 100],
        height=500,
        hovermode='x unified'
    )

    st.plotly_chart(fig, use_container_width=True)

    # Data table
    st.subheader("Data Table")
    display_df = df[['brand', 'title', 'overall_score', 'climate_score',
                     'social_score', 'cultural_score', 'ethical_score']].copy()
    display_df['title'] = display_df['title'].str[:60] + '...'
    st.dataframe(display_df, use_container_width=True, height=300)

with tab2:
    st.subheader("Score Distribution")

    col1, col2 = st.columns(2)

    with col1:
        # Overall score distribution
        fig = px.histogram(df, x='overall_score', nbins=10,
                          title="Overall Score Distribution",
                          labels={'overall_score': 'Overall Score'},
                          color_discrete_sequence=['#667eea'])
        fig.update_layout(yaxis_title="Count", height=300)
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        # Box plot for all dimensions
        dimension_data = pd.DataFrame({
            'Climate': df['climate_score'],
            'Social': df['social_score'],
            'Cultural': df['cultural_score'],
            'Ethical': df['ethical_score']
        })

        fig = go.Figure()
        colors = ['#48bb78', '#ed64a6', '#4299e1', '#f6ad55']

        for i, (col, color) in enumerate(zip(dimension_data.columns, colors)):
            fig.add_trace(go.Box(
                y=dimension_data[col],
                name=col,
                marker_color=color
            ))

        fig.update_layout(
            title="Dimension Score Distribution",
            yaxis_title="Score",
            yaxis_range=[0, 100],
            height=300
        )
        st.plotly_chart(fig, use_container_width=True)

    # Scatter plot: Climate vs Social
    st.subheader("Climate vs Social Responsibility")
    fig = px.scatter(df, x='climate_score', y='social_score',
                    hover_data=['brand', 'overall_score'],
                    title="Climate Score vs Social Score",
                    color='overall_score',
                    color_continuous_scale='Viridis',
                    size='overall_score',
                    labels={'climate_score': 'Climate Score',
                           'social_score': 'Social Score'})
    fig.update_layout(height=400)
    st.plotly_chart(fig, use_container_width=True)

with tab3:
    st.subheader("Average Dimension Scores - Radar Chart")

    fig = go.Figure()

    categories = ['Climate', 'Social', 'Cultural', 'Ethical', 'Climate']
    values = [avg_climate, avg_social, avg_cultural, avg_ethical, avg_climate]

    fig.add_trace(go.Scatterpolar(
        r=values,
        theta=categories,
        fill='toself',
        name='Cannes Ads',
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
        showlegend=True,
        height=500
    )

    st.plotly_chart(fig, use_container_width=True)

with tab4:
    st.subheader("Top & Bottom Performers")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("### 🏆 Top 5 Performers")
        top_5 = df.nlargest(5, 'overall_score')[['brand', 'title', 'overall_score']]
        for idx, row in top_5.iterrows():
            st.markdown(f"**{row['overall_score']:.0f}/100** - {row['brand']}")
            st.caption(row['title'][:60] + "...")
            st.markdown("---")

    with col2:
        st.markdown("### ⚠️ Bottom 5 Performers")
        bottom_5 = df.nsmallest(5, 'overall_score')[['brand', 'title', 'overall_score']]
        for idx, row in bottom_5.iterrows():
            st.markdown(f"**{row['overall_score']:.0f}/100** - {row['brand']}")
            st.caption(row['title'][:60] + "...")
            st.markdown("---")

    # Dimension leaders
    st.markdown("### 🎯 Dimension Leaders")

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        climate_leader = df.loc[df['climate_score'].idxmax()]
        st.metric("Climate Leader", climate_leader['brand'],
                 delta=f"{climate_leader['climate_score']:.0f}/100")
        st.caption(climate_leader['title'][:40] + "...")

    with col2:
        social_leader = df.loc[df['social_score'].idxmax()]
        st.metric("Social Leader", social_leader['brand'],
                 delta=f"{social_leader['social_score']:.0f}/100")
        st.caption(social_leader['title'][:40] + "...")

    with col3:
        cultural_leader = df.loc[df['cultural_score'].idxmax()]
        st.metric("Cultural Leader", cultural_leader['brand'],
                 delta=f"{cultural_leader['cultural_score']:.0f}/100")
        st.caption(cultural_leader['title'][:40] + "...")

    with col4:
        ethical_leader = df.loc[df['ethical_score'].idxmax()]
        st.metric("Ethical Leader", ethical_leader['brand'],
                 delta=f"{ethical_leader['ethical_score']:.0f}/100")
        st.caption(ethical_leader['title'][:40] + "...")

# Key findings
st.markdown("---")
st.header("💡 Key Findings")

col1, col2 = st.columns(2)

with col1:
    st.subheader("Strengths")
    if avg_cultural > 70:
        st.success(f"✅ Strong cultural sensitivity (avg: {avg_cultural:.1f})")
    if avg_social > 70:
        st.success(f"✅ Good social responsibility (avg: {avg_social:.1f})")
    if avg_ethical > 70:
        st.success(f"✅ High ethical standards (avg: {avg_ethical:.1f})")

with col2:
    st.subheader("Areas for Improvement")
    if avg_climate < 50:
        st.warning(f"⚠️ Climate messaging needs work (avg: {avg_climate:.1f})")
    if avg_social < 50:
        st.warning(f"⚠️ Social responsibility could improve (avg: {avg_social:.1f})")
    if avg_ethical < 50:
        st.warning(f"⚠️ Ethical communication needs attention (avg: {avg_ethical:.1f})")

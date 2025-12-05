import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from pathlib import Path
import json

st.set_page_config(page_title="Comparison", page_icon="⚖️", layout="wide")

# Load data
@st.cache_data
def load_all_data():
    data_dir = Path(__file__).parent.parent.parent
    datasets = {'cannes': None, 'hungarian': None}

    cannes_files = sorted(data_dir.glob('cannes_analysis_results_*.json'))
    if cannes_files:
        with open(cannes_files[-1], 'r', encoding='utf-8') as f:
            datasets['cannes'] = pd.DataFrame(json.load(f))

    hungarian_files = sorted(data_dir.glob('hungarian_analysis_results_*.json'))
    if hungarian_files:
        with open(hungarian_files[-1], 'r', encoding='utf-8') as f:
            datasets['hungarian'] = pd.DataFrame(json.load(f))

    return datasets

datasets = load_all_data()
cannes_df = datasets['cannes']
hungarian_df = datasets['hungarian']

has_cannes = cannes_df is not None and len(cannes_df) > 0
has_hungarian = hungarian_df is not None and len(hungarian_df) > 0

if not has_cannes or not has_hungarian:
    st.warning("Need both Cannes and Hungarian data for comparison!")
    if not has_cannes:
        st.error("❌ Cannes data not found")
    if not has_hungarian:
        st.error("❌ Hungarian data not found")
    st.stop()

# Header
st.title("⚖️ Cannes vs Hungarian Comparison")
st.markdown(f"Comparing **{len(cannes_df)} Cannes Grand Prix ads** with **{len(hungarian_df)} Hungarian 50-50 Lista ads**")

st.markdown("---")

# Calculate averages
cannes_avg = cannes_df[['overall_score', 'climate_score', 'social_score', 'cultural_score', 'ethical_score']].mean()
hungarian_avg = hungarian_df[['overall_score', 'climate_score', 'social_score', 'cultural_score', 'ethical_score']].mean()

# Summary metrics with differences
col1, col2, col3, col4, col5 = st.columns(5)

metrics = [
    ("Overall", "overall_score"),
    ("Climate", "climate_score"),
    ("Social", "social_score"),
    ("Cultural", "cultural_score"),
    ("Ethical", "ethical_score")
]

for col, (label, key) in zip([col1, col2, col3, col4, col5], metrics):
    with col:
        diff = hungarian_avg[key] - cannes_avg[key]
        winner = "🇭🇺" if diff > 0 else "🏆"

        st.metric(
            label,
            f"{abs(diff):.1f}",
            delta=f"{winner} {'Hungarian' if diff > 0 else 'Cannes'} leads",
            delta_color="off"
        )

st.markdown("---")

# Visualization tabs
tab1, tab2, tab3, tab4 = st.tabs(["📊 Side-by-Side", "🎯 Radar Overlay", "📈 Distribution", "🔍 Detailed Analysis"])

with tab1:
    st.subheader("Average Scores Comparison")

    fig = go.Figure()

    dimensions = ['Overall', 'Climate', 'Social', 'Cultural', 'Ethical']
    cannes_values = [cannes_avg['overall_score'], cannes_avg['climate_score'],
                     cannes_avg['social_score'], cannes_avg['cultural_score'],
                     cannes_avg['ethical_score']]
    hungarian_values = [hungarian_avg['overall_score'], hungarian_avg['climate_score'],
                       hungarian_avg['social_score'], hungarian_avg['cultural_score'],
                       hungarian_avg['ethical_score']]

    fig.add_trace(go.Bar(
        name='Cannes Grand Prix',
        x=dimensions,
        y=cannes_values,
        marker_color='#667eea',
        text=[f"{v:.1f}" for v in cannes_values],
        textposition='auto'
    ))

    fig.add_trace(go.Bar(
        name='Hungarian 50-50 Lista',
        x=dimensions,
        y=hungarian_values,
        marker_color='#48bb78',
        text=[f"{v:.1f}" for v in hungarian_values],
        textposition='auto'
    ))

    fig.update_layout(
        barmode='group',
        yaxis_title="Average Score",
        yaxis_range=[0, 100],
        height=500,
        hovermode='x unified'
    )

    st.plotly_chart(fig, use_container_width=True)

    # Difference table
    st.subheader("Score Differences")

    diff_data = []
    for dim, key in metrics:
        c_val = cannes_avg[key]
        h_val = hungarian_avg[key]
        diff = h_val - c_val
        winner = "Hungarian" if diff > 0 else "Cannes"

        diff_data.append({
            'Dimension': dim,
            'Cannes': f"{c_val:.1f}",
            'Hungarian': f"{h_val:.1f}",
            'Difference': f"{diff:+.1f}",
            'Leader': winner
        })

    diff_df = pd.DataFrame(diff_data)
    st.dataframe(diff_df, use_container_width=True, hide_index=True)

with tab2:
    st.subheader("Radar Chart Overlay")

    fig = go.Figure()

    categories = ['Climate', 'Social', 'Cultural', 'Ethical', 'Climate']

    # Cannes
    cannes_radar = [cannes_avg['climate_score'], cannes_avg['social_score'],
                    cannes_avg['cultural_score'], cannes_avg['ethical_score'],
                    cannes_avg['climate_score']]

    fig.add_trace(go.Scatterpolar(
        r=cannes_radar,
        theta=categories,
        fill='toself',
        name='Cannes Grand Prix',
        line_color='#667eea',
        fillcolor='rgba(102, 126, 234, 0.3)'
    ))

    # Hungarian
    hungarian_radar = [hungarian_avg['climate_score'], hungarian_avg['social_score'],
                       hungarian_avg['cultural_score'], hungarian_avg['ethical_score'],
                       hungarian_avg['climate_score']]

    fig.add_trace(go.Scatterpolar(
        r=hungarian_radar,
        theta=categories,
        fill='toself',
        name='Hungarian 50-50 Lista',
        line_color='#48bb78',
        fillcolor='rgba(72, 187, 120, 0.3)'
    ))

    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 100]
            )
        ),
        showlegend=True,
        height=600
    )

    st.plotly_chart(fig, use_container_width=True)

with tab3:
    st.subheader("Score Distribution Comparison")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("#### Overall Score Distribution")

        fig = go.Figure()

        fig.add_trace(go.Histogram(
            x=cannes_df['overall_score'],
            name='Cannes',
            marker_color='#667eea',
            opacity=0.7,
            nbinsx=10
        ))

        fig.add_trace(go.Histogram(
            x=hungarian_df['overall_score'],
            name='Hungarian',
            marker_color='#48bb78',
            opacity=0.7,
            nbinsx=10
        ))

        fig.update_layout(
            barmode='overlay',
            xaxis_title="Overall Score",
            yaxis_title="Count",
            height=400
        )

        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.markdown("#### Climate Score Distribution")

        fig = go.Figure()

        fig.add_trace(go.Histogram(
            x=cannes_df['climate_score'],
            name='Cannes',
            marker_color='#667eea',
            opacity=0.7,
            nbinsx=10
        ))

        fig.add_trace(go.Histogram(
            x=hungarian_df['climate_score'],
            name='Hungarian',
            marker_color='#48bb78',
            opacity=0.7,
            nbinsx=10
        ))

        fig.update_layout(
            barmode='overlay',
            xaxis_title="Climate Score",
            yaxis_title="Count",
            height=400
        )

        st.plotly_chart(fig, use_container_width=True)

    # Scatter plot comparison
    st.markdown("#### Climate vs Social: Both Datasets")

    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=cannes_df['climate_score'],
        y=cannes_df['social_score'],
        mode='markers',
        name='Cannes',
        marker=dict(size=10, color='#667eea', opacity=0.6),
        text=cannes_df['brand'],
        hovertemplate='<b>%{text}</b><br>Climate: %{x}<br>Social: %{y}<extra></extra>'
    ))

    # Extract brand from Hungarian titles
    hungarian_df['display_brand'] = hungarian_df['title'].str.split('//').str[0].str.strip()

    fig.add_trace(go.Scatter(
        x=hungarian_df['climate_score'],
        y=hungarian_df['social_score'],
        mode='markers',
        name='Hungarian',
        marker=dict(size=10, color='#48bb78', opacity=0.6),
        text=hungarian_df['display_brand'],
        hovertemplate='<b>%{text}</b><br>Climate: %{x}<br>Social: %{y}<extra></extra>'
    ))

    fig.update_layout(
        xaxis_title="Climate Score",
        yaxis_title="Social Score",
        xaxis_range=[0, 100],
        yaxis_range=[0, 100],
        height=500
    )

    st.plotly_chart(fig, use_container_width=True)

with tab4:
    st.subheader("Detailed Statistical Analysis")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("### 🏆 Cannes Statistics")

        stats_df = cannes_df[['overall_score', 'climate_score', 'social_score',
                               'cultural_score', 'ethical_score']].describe()
        st.dataframe(stats_df.round(1), use_container_width=True)

    with col2:
        st.markdown("### 🇭🇺 Hungarian Statistics")

        stats_df = hungarian_df[['overall_score', 'climate_score', 'social_score',
                                  'cultural_score', 'ethical_score']].describe()
        st.dataframe(stats_df.round(1), use_container_width=True)

    # Key observations
    st.markdown("---")
    st.subheader("📝 Key Observations")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("#### Cannes Characteristics")

        observations_cannes = []

        if cannes_avg['climate_score'] > 50:
            observations_cannes.append(f"✅ Strong climate messaging (avg: {cannes_avg['climate_score']:.1f})")
        else:
            observations_cannes.append(f"⚠️ Weak climate messaging (avg: {cannes_avg['climate_score']:.1f})")

        if cannes_df['overall_score'].std() > 20:
            observations_cannes.append(f"📊 High score variance (std: {cannes_df['overall_score'].std():.1f})")
        else:
            observations_cannes.append(f"📊 Consistent scores (std: {cannes_df['overall_score'].std():.1f})")

        best_dimension = cannes_avg[['climate_score', 'social_score', 'cultural_score', 'ethical_score']].idxmax()
        best_score = cannes_avg[best_dimension]
        dim_name = best_dimension.replace('_score', '').title()
        observations_cannes.append(f"⭐ Strongest in {dim_name} ({best_score:.1f})")

        for obs in observations_cannes:
            st.markdown(obs)

    with col2:
        st.markdown("#### Hungarian Characteristics")

        observations_hungarian = []

        if hungarian_avg['climate_score'] > 50:
            observations_hungarian.append(f"✅ Strong climate messaging (avg: {hungarian_avg['climate_score']:.1f})")
        else:
            observations_hungarian.append(f"⚠️ Weak climate messaging (avg: {hungarian_avg['climate_score']:.1f})")

        if hungarian_df['overall_score'].std() > 20:
            observations_hungarian.append(f"📊 High score variance (std: {hungarian_df['overall_score'].std():.1f})")
        else:
            observations_hungarian.append(f"📊 Consistent scores (std: {hungarian_df['overall_score'].std():.1f})")

        best_dimension = hungarian_avg[['climate_score', 'social_score', 'cultural_score', 'ethical_score']].idxmax()
        best_score = hungarian_avg[best_dimension]
        dim_name = best_dimension.replace('_score', '').title()
        observations_hungarian.append(f"⭐ Strongest in {dim_name} ({best_score:.1f})")

        for obs in observations_hungarian:
            st.markdown(obs)

# Winner summary
st.markdown("---")
st.header("🏆 Overall Winner")

if hungarian_avg['overall_score'] > cannes_avg['overall_score']:
    diff = hungarian_avg['overall_score'] - cannes_avg['overall_score']
    st.success(f"🇭🇺 **Hungarian 50-50 Lista ads score {diff:.1f} points higher** on average ({hungarian_avg['overall_score']:.1f} vs {cannes_avg['overall_score']:.1f})")
else:
    diff = cannes_avg['overall_score'] - hungarian_avg['overall_score']
    st.success(f"🏆 **Cannes Grand Prix ads score {diff:.1f} points higher** on average ({cannes_avg['overall_score']:.1f} vs {hungarian_avg['overall_score']:.1f})")

# Dimension winners
st.markdown("#### Dimension Winners")

col1, col2, col3, col4 = st.columns(4)

dimensions_display = [
    ("Climate", "climate_score", col1),
    ("Social", "social_score", col2),
    ("Cultural", "cultural_score", col3),
    ("Ethical", "ethical_score", col4)
]

for dim, key, col in dimensions_display:
    with col:
        if hungarian_avg[key] > cannes_avg[key]:
            diff = hungarian_avg[key] - cannes_avg[key]
            st.metric(dim, "🇭🇺 Hungarian", f"+{diff:.1f}")
        else:
            diff = cannes_avg[key] - hungarian_avg[key]
            st.metric(dim, "🏆 Cannes", f"+{diff:.1f}")

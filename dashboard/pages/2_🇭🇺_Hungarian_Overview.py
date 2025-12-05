import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from pathlib import Path
import json

st.set_page_config(page_title="Hungarian Overview", page_icon="🇭🇺", layout="wide")

# Load data
@st.cache_data
def load_hungarian_data():
    data_dir = Path(__file__).parent.parent.parent
    hungarian_files = sorted(data_dir.glob('hungarian_analysis_results_*.json'))
    if hungarian_files:
        with open(hungarian_files[-1], 'r', encoding='utf-8') as f:
            return pd.DataFrame(json.load(f))
    return None

df = load_hungarian_data()

if df is None or len(df) == 0:
    st.error("No Hungarian analysis data found!")
    st.stop()

# Language toggle
language = st.sidebar.radio("Language / Nyelv", ["English", "Magyar"], index=0)
is_hungarian = language == "Magyar"

# Header
if is_hungarian:
    st.title("🇭🇺 Magyar 50-50 Lista Elemzés")
    st.markdown(f"**{len(df)} reklám elemezve** a közönségszavazás alapján")
else:
    st.title("🇭🇺 Hungarian 50-50 Lista Analysis")
    st.markdown(f"**{len(df)} ads analyzed** from public voting results")

st.markdown("---")

# Summary metrics
col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    avg_overall = df['overall_score'].mean()
    label = "Összpontszám" if is_hungarian else "Overall Score"
    st.metric(label, f"{avg_overall:.1f}/100")

with col2:
    avg_climate = df['climate_score'].mean()
    label = "Klíma" if is_hungarian else "Climate"
    st.metric(label, f"{avg_climate:.1f}/100",
             delta=f"{avg_climate - avg_overall:.1f}",
             delta_color="off")

with col3:
    avg_social = df['social_score'].mean()
    label = "Társadalmi" if is_hungarian else "Social"
    st.metric(label, f"{avg_social:.1f}/100",
             delta=f"{avg_social - avg_overall:.1f}",
             delta_color="off")

with col4:
    avg_cultural = df['cultural_score'].mean()
    label = "Kulturális" if is_hungarian else "Cultural"
    st.metric(label, f"{avg_cultural:.1f}/100",
             delta=f"{avg_cultural - avg_overall:.1f}",
             delta_color="off")

with col5:
    avg_ethical = df['ethical_score'].mean()
    label = "Etikus" if is_hungarian else "Ethical"
    st.metric(label, f"{avg_ethical:.1f}/100",
             delta=f"{avg_ethical - avg_overall:.1f}",
             delta_color="off")

st.markdown("---")

# Visualization tabs
if is_hungarian:
    tab1, tab2, tab3, tab4 = st.tabs(["📊 Minden reklám", "📈 Eloszlás", "🎯 Radar diagram", "🏅 Rangsor"])
else:
    tab1, tab2, tab3, tab4 = st.tabs(["📊 All Ads", "📈 Distribution", "🎯 Radar Chart", "🏅 Rankings"])

with tab1:
    title = "Minden Magyar Reklám - Pontszám Bontás" if is_hungarian else "All Hungarian Ads - Score Breakdown"
    st.subheader(title)

    # Extract brand from title (first part before //)
    df['display_brand'] = df['title'].str.split('//').str[0].str.strip()

    # Create bar chart
    fig = go.Figure()

    labels_hu = ['Klíma', 'Társadalmi', 'Kulturális', 'Etikus']
    labels_en = ['Climate', 'Social', 'Cultural', 'Ethical']
    labels = labels_hu if is_hungarian else labels_en

    fig.add_trace(go.Bar(
        name=labels[0],
        x=df['display_brand'],
        y=df['climate_score'],
        marker_color='#48bb78'
    ))
    fig.add_trace(go.Bar(
        name=labels[1],
        x=df['display_brand'],
        y=df['social_score'],
        marker_color='#ed64a6'
    ))
    fig.add_trace(go.Bar(
        name=labels[2],
        x=df['display_brand'],
        y=df['cultural_score'],
        marker_color='#4299e1'
    ))
    fig.add_trace(go.Bar(
        name=labels[3],
        x=df['display_brand'],
        y=df['ethical_score'],
        marker_color='#f6ad55'
    ))

    x_title = "Márka" if is_hungarian else "Brand"
    y_title = "Pontszám" if is_hungarian else "Score"

    fig.update_layout(
        barmode='group',
        xaxis_title=x_title,
        yaxis_title=y_title,
        yaxis_range=[0, 100],
        height=500,
        hovermode='x unified'
    )

    st.plotly_chart(fig, use_container_width=True)

    # Data table
    table_title = "Adattábla" if is_hungarian else "Data Table"
    st.subheader(table_title)

    display_df = df[['display_brand', 'title', 'overall_score', 'climate_score',
                     'social_score', 'cultural_score', 'ethical_score']].copy()
    display_df['title'] = display_df['title'].str[:60] + '...'

    if is_hungarian:
        display_df.columns = ['Márka', 'Cím', 'Össz', 'Klíma', 'Társad.', 'Kult.', 'Etikus']
    else:
        display_df.columns = ['Brand', 'Title', 'Overall', 'Climate', 'Social', 'Cultural', 'Ethical']

    st.dataframe(display_df, use_container_width=True, height=300)

with tab2:
    title = "Pontszám Eloszlás" if is_hungarian else "Score Distribution"
    st.subheader(title)

    col1, col2 = st.columns(2)

    with col1:
        title_hist = "Összpontszám Eloszlás" if is_hungarian else "Overall Score Distribution"
        x_label = "Összpontszám" if is_hungarian else "Overall Score"

        fig = px.histogram(df, x='overall_score', nbins=10,
                          title=title_hist,
                          labels={'overall_score': x_label},
                          color_discrete_sequence=['#667eea'])
        y_label = "Darabszám" if is_hungarian else "Count"
        fig.update_layout(yaxis_title=y_label, height=300)
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        dimension_data = pd.DataFrame({
            'Klíma' if is_hungarian else 'Climate': df['climate_score'],
            'Társadalmi' if is_hungarian else 'Social': df['social_score'],
            'Kulturális' if is_hungarian else 'Cultural': df['cultural_score'],
            'Etikus' if is_hungarian else 'Ethical': df['ethical_score']
        })

        fig = go.Figure()
        colors = ['#48bb78', '#ed64a6', '#4299e1', '#f6ad55']

        for col, color in zip(dimension_data.columns, colors):
            fig.add_trace(go.Box(
                y=dimension_data[col],
                name=col,
                marker_color=color
            ))

        title_box = "Dimenzió Pontszám Eloszlás" if is_hungarian else "Dimension Score Distribution"
        y_label = "Pontszám" if is_hungarian else "Score"

        fig.update_layout(
            title=title_box,
            yaxis_title=y_label,
            yaxis_range=[0, 100],
            height=300
        )
        st.plotly_chart(fig, use_container_width=True)

    # Scatter plot
    title_scatter = "Klíma vs Társadalmi Felelősség" if is_hungarian else "Climate vs Social Responsibility"
    st.subheader(title_scatter)

    x_label = "Klíma Pontszám" if is_hungarian else "Climate Score"
    y_label = "Társadalmi Pontszám" if is_hungarian else "Social Score"

    fig = px.scatter(df, x='climate_score', y='social_score',
                    hover_data=['display_brand', 'overall_score'],
                    title=title_scatter,
                    color='overall_score',
                    color_continuous_scale='Viridis',
                    size='overall_score',
                    labels={'climate_score': x_label,
                           'social_score': y_label})
    fig.update_layout(height=400)
    st.plotly_chart(fig, use_container_width=True)

with tab3:
    title = "Átlag Dimenzió Pontszámok - Radar Diagram" if is_hungarian else "Average Dimension Scores - Radar Chart"
    st.subheader(title)

    fig = go.Figure()

    if is_hungarian:
        categories = ['Klíma', 'Társadalmi', 'Kulturális', 'Etikus', 'Klíma']
    else:
        categories = ['Climate', 'Social', 'Cultural', 'Ethical', 'Climate']

    values = [avg_climate, avg_social, avg_cultural, avg_ethical, avg_climate]

    trace_name = "Magyar Reklámok" if is_hungarian else "Hungarian Ads"

    fig.add_trace(go.Scatterpolar(
        r=values,
        theta=categories,
        fill='toself',
        name=trace_name,
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
    title = "Legjobb és Leggyengébb Teljesítők" if is_hungarian else "Top & Bottom Performers"
    st.subheader(title)

    col1, col2 = st.columns(2)

    with col1:
        header = "### 🏆 Top 5 Teljesítő" if is_hungarian else "### 🏆 Top 5 Performers"
        st.markdown(header)

        top_5 = df.nlargest(5, 'overall_score')[['display_brand', 'title', 'overall_score']]
        for idx, row in top_5.iterrows():
            st.markdown(f"**{row['overall_score']:.0f}/100** - {row['display_brand']}")
            st.caption(row['title'][:60] + "...")
            st.markdown("---")

    with col2:
        header = "### ⚠️ Alsó 5 Teljesítő" if is_hungarian else "### ⚠️ Bottom 5 Performers"
        st.markdown(header)

        bottom_5 = df.nsmallest(5, 'overall_score')[['display_brand', 'title', 'overall_score']]
        for idx, row in bottom_5.iterrows():
            st.markdown(f"**{row['overall_score']:.0f}/100** - {row['display_brand']}")
            st.caption(row['title'][:60] + "...")
            st.markdown("---")

    # Dimension leaders
    title = "### 🎯 Dimenzió Vezetők" if is_hungarian else "### 🎯 Dimension Leaders"
    st.markdown(title)

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        climate_leader = df.loc[df['climate_score'].idxmax()]
        label = "Klíma Vezető" if is_hungarian else "Climate Leader"
        st.metric(label, climate_leader['display_brand'],
                 delta=f"{climate_leader['climate_score']:.0f}/100")
        st.caption(climate_leader['title'][:40] + "...")

    with col2:
        social_leader = df.loc[df['social_score'].idxmax()]
        label = "Társadalmi Vezető" if is_hungarian else "Social Leader"
        st.metric(label, social_leader['display_brand'],
                 delta=f"{social_leader['social_score']:.0f}/100")
        st.caption(social_leader['title'][:40] + "...")

    with col3:
        cultural_leader = df.loc[df['cultural_score'].idxmax()]
        label = "Kulturális Vezető" if is_hungarian else "Cultural Leader"
        st.metric(label, cultural_leader['display_brand'],
                 delta=f"{cultural_leader['cultural_score']:.0f}/100")
        st.caption(cultural_leader['title'][:40] + "...")

    with col4:
        ethical_leader = df.loc[df['ethical_score'].idxmax()]
        label = "Etikus Vezető" if is_hungarian else "Ethical Leader"
        st.metric(label, ethical_leader['display_brand'],
                 delta=f"{ethical_leader['ethical_score']:.0f}/100")
        st.caption(ethical_leader['title'][:40] + "...")

# Key findings
st.markdown("---")
title = "💡 Főbb Megállapítások" if is_hungarian else "💡 Key Findings"
st.header(title)

col1, col2 = st.columns(2)

with col1:
    header = "Erősségek" if is_hungarian else "Strengths"
    st.subheader(header)

    if avg_cultural > 70:
        text = f"✅ Erős kulturális érzékenység (átlag: {avg_cultural:.1f})" if is_hungarian else f"✅ Strong cultural sensitivity (avg: {avg_cultural:.1f})"
        st.success(text)
    if avg_social > 70:
        text = f"✅ Jó társadalmi felelősség (átlag: {avg_social:.1f})" if is_hungarian else f"✅ Good social responsibility (avg: {avg_social:.1f})"
        st.success(text)
    if avg_ethical > 70:
        text = f"✅ Magas etikus standardok (átlag: {avg_ethical:.1f})" if is_hungarian else f"✅ High ethical standards (avg: {avg_ethical:.1f})"
        st.success(text)

with col2:
    header = "Fejlesztendő Területek" if is_hungarian else "Areas for Improvement"
    st.subheader(header)

    if avg_climate < 50:
        text = f"⚠️ Klíma üzenetek fejlesztésre szorulnak (átlag: {avg_climate:.1f})" if is_hungarian else f"⚠️ Climate messaging needs work (avg: {avg_climate:.1f})"
        st.warning(text)
    if avg_social < 50:
        text = f"⚠️ Társadalmi felelősség javítható (átlag: {avg_social:.1f})" if is_hungarian else f"⚠️ Social responsibility could improve (avg: {avg_social:.1f})"
        st.warning(text)
    if avg_ethical < 50:
        text = f"⚠️ Etikus kommunikáció figyelmet igényel (átlag: {avg_ethical:.1f})" if is_hungarian else f"⚠️ Ethical communication needs attention (avg: {avg_ethical:.1f})"
        st.warning(text)

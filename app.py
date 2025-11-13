import streamlit as st
import google.generativeai as genai
import base64
from PIL import Image, ImageDraw, ImageFont
import io
import json
import plotly.graph_objects as go
from typing import Dict, List
from datetime import datetime
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageBreak, Image as RLImage
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')
import pandas as pd

# Page config
st.set_page_config(
    page_title="Responsible Advertising Index Demo",
    page_icon="📊",
    layout="wide"
)

# Initialize session state for history
if 'analysis_history' not in st.session_state:
    st.session_state.analysis_history = []

# Helper function to create realistic example ad images
def create_example_image(ad_type: str) -> bytes:
    """Create a realistic-looking placeholder image for example ads"""
    # Create image with appropriate theme
    img = Image.new('RGB', (1200, 800), color=(255, 255, 255))
    draw = ImageDraw.Draw(img)
    
    if ad_type == "sustainable":
        # Green/eco theme
        draw.rectangle([0, 0, 1200, 800], fill=(230, 245, 230))
        draw.rectangle([50, 50, 1150, 150], fill=(34, 139, 34))
        draw.text((100, 80), "EcoThreads", fill=(255, 255, 255), font=None)
        draw.text((100, 200), "REPAIR REVOLUTION", fill=(34, 139, 34), font=None)
        draw.text((100, 250), "Community Repair Cafe - Every Saturday", fill=(80, 80, 80), font=None)
        draw.ellipse([900, 400, 1100, 600], fill=(100, 180, 100))
        draw.text((920, 480), "100%\nOrganic", fill=(255, 255, 255), font=None)
        
    elif ad_type == "weight_loss":
        # Before/after style
        draw.rectangle([0, 0, 1200, 800], fill=(240, 240, 250))
        draw.rectangle([50, 50, 1150, 150], fill=(138, 43, 226))
        draw.text((100, 80), "SlimFit Pro", fill=(255, 255, 255), font=None)
        draw.line([600, 200, 600, 750], fill=(200, 200, 200), width=3)
        draw.text((200, 300), "BEFORE", fill=(100, 100, 100), font=None)
        draw.text((800, 300), "AFTER", fill=(100, 100, 100), font=None)
        draw.rectangle([150, 400, 450, 700], fill=(200, 150, 150))
        draw.rectangle([750, 400, 1050, 700], fill=(150, 200, 150))
        
    elif ad_type == "ev":
        # Modern EV aesthetic
        draw.rectangle([0, 0, 1200, 800], fill=(240, 248, 255))
        draw.rectangle([50, 50, 1150, 150], fill=(30, 60, 90))
        draw.text((100, 80), "DriveForward Motors", fill=(255, 255, 255), font=None)
        draw.rectangle([200, 300, 1000, 600], fill=(60, 80, 100))
        draw.text((400, 420), "E7 - ELECTRIC SUV", fill=(255, 255, 255), font=None)
        draw.text((400, 500), "300 Mile Range | 0-60 in 4.2s", fill=(200, 220, 240), font=None)
    
    # Convert to bytes
    img_byte_arr = io.BytesIO()
    img.save(img_byte_arr, format='PNG')
    return img_byte_arr.getvalue()

# Example ads database - now with generated images
EXAMPLE_ADS = {
    "Excellent: Sustainable Fashion": {
        "brand": "EcoThreads",
        "copy": """Repair Revolution

Every EcoThreads garment comes with a lifetime repair guarantee. 
Broken zipper? We'll fix it. Torn seam? We'll mend it.

Since 2019, we've repaired 14,000 items, keeping them out of landfills.

Our fabric: 100% organic cotton, GOTS certified.
Our factories: Fair Trade certified, transparent supply chain.
Our promise: Buy less, wear longer.

Visit our repair café every Saturday 10am-4pm.
Bring any clothing item - ours or not - we'll help you fix it for free.

#RepairRevolution #WearItOut #SlowFashion""",
        "image_description": "Diverse group of people of different ages, races, and body types sitting at a communal table repairing clothes together. Natural lighting, authentic documentary style. Tools and fabric visible. Community atmosphere.",
        "expected_score": 90,
        "image_type": "sustainable"
    },
    "Problematic: Weight Loss": {
        "brand": "SlimFit Pro",
        "copy": """Get Your Dream Body in Just 30 Days!

Tired of feeling uncomfortable in your own skin?
Want to finally fit into those jeans?

SlimFit Pro's revolutionary formula helps you:
✓ Drop pounds fast
✓ Feel confident again
✓ Turn heads everywhere you go

Before: Unhappy. After: Unstoppable.

"I lost 15 pounds in 3 weeks!" - Sarah M.
"Finally, I feel beautiful." - Jessica T.

Limited time offer: Buy 2, Get 1 FREE

Results may vary. Not a substitute for diet and exercise.

#DreamBody #Transformation #SlimFitPro""",
        "image_description": "Before/after style image with a person looking sad on left, happy on right. Focus on weight loss transformation. Poses emphasize body shape changes.",
        "expected_score": 35,
        "image_type": "weight_loss"
    },
    "Mixed: Electric Vehicle": {
        "brand": "DriveForward Motors",
        "copy": """The future is electric.

Introducing the DriveForward E7 - our first all-electric SUV.

✓ 300-mile range per charge
✓ 0-60 in 4.2 seconds
✓ Advanced safety features
✓ Spacious interior for the whole family

Going electric doesn't mean compromising on performance.

Starting at $55,000. Test drive today.

*Based on EPA estimates. Actual range may vary.

#ElectricFuture #E7Launch #DriveForward""",
        "image_description": "Sleek electric SUV on open road with mountains in background. Modern, aspirational aesthetic. Family visible through windows. Clean, professional photography.",
        "expected_score": 65,
        "image_type": "ev"
    },
    "Magyar: Fenntartható Divat": {
        "brand": "ÖkoFonál",
        "copy": """Javítási Forradalom

Minden ÖkoFonál ruhadarab élethosszig tartó javítási garanciával érkezik.
Elromlott cipzár? Megjavítjuk. Elszakadt varrás? Megfoltozuk.

2019 óta 14 000 darabot javítottunk meg, távol tartva őket a hulladéklerakóktól.

Anyagunk: 100% organikus pamut, GOTS minősítéssel.
Gyáraink: Fair Trade tanúsítvánnyal, átlátható ellátási lánccal.
Ígéretünk: Vásárolj kevesebbet, viselj tovább.

Látogass el javító kávézónkba minden szombaton 10:00-16:00 között.
Hozz bármilyen ruhadarabot - akár a miénk, akár nem - ingyen segítünk megjavítani.

#JavításiForradalom #ViseljTovább #LassúDivat""",
        "image_description": "Diverse group of people of different ages, races, and body types sitting at a communal table repairing clothes together. Natural lighting, authentic documentary style. Tools and fabric visible. Community atmosphere.",
        "expected_score": 90,
        "image_type": "sustainable"
    }
}

# Scoring framework definition (English and Hungarian)
FRAMEWORK = {
    "Climate Responsibility": {
        "weight": 0.25,
        "indicators": [
            "Sustainability messaging presence and authenticity",
            "Absence of greenwashing or exaggerated claims",
            "Climate-positive products/behaviors shown",
            "Transparency in environmental framing"
        ],
        "hu_name": "Klímafelelősség",
        "hu_indicators": [
            "Fenntarthatósági üzenetek jelenléte és hitelessége",
            "Zöldre festés és túlzó állítások hiánya",
            "Klímapozitív termékek/viselkedések bemutatása",
            "Átláthatóság a környezeti kommunikációban"
        ]
    },
    "Social Responsibility": {
        "weight": 0.25,
        "indicators": [
            "Diversity in representation (gender, race, age, body type, ability)",
            "Avoidance of harmful stereotypes",
            "Empowering depiction of underrepresented groups",
            "Inclusive language and messaging"
        ],
        "hu_name": "Társadalmi Felelősség",
        "hu_indicators": [
            "Sokszínűség a megjelenítésben (nem, faj, kor, testalkat, képesség)",
            "Káros sztereotípiák elkerülése",
            "Alulreprezentált csoportok megerősítő ábrázolása",
            "Befogadó nyelvezet és üzenet"
        ]
    },
    "Cultural Sensitivity": {
        "weight": 0.25,
        "indicators": [
            "Respectful use of cultural symbols and traditions",
            "Sensitivity to local norms and values",
            "Awareness of geopolitical contexts",
            "Balance between global and local resonance"
        ],
        "hu_name": "Kulturális Érzékenység",
        "hu_indicators": [
            "Kulturális szimbólumok és hagyományok tiszteletteljes használata",
            "Érzékenység a helyi normák és értékek iránt",
            "Geopolitikai kontextusok tudatossága",
            "Egyensúly a globális és helyi rezonancia között"
        ]
    },
    "Ethical Communication": {
        "weight": 0.25,
        "indicators": [
            "Transparency in intent and disclosures",
            "Avoidance of manipulative techniques",
            "Truthful and verifiable claims",
            "Encouragement of informed choice over exploitation"
        ],
        "hu_name": "Etikus Kommunikáció",
        "hu_indicators": [
            "Átláthatóság a szándékban és közlésekben",
            "Manipulatív technikák elkerülése",
            "Igazolható és valós állítások",
            "Tájékozott döntéshozatal ösztönzése a kizsákmányolás helyett"
        ]
    }
}

# Language-specific UI text
UI_TEXT = {
    "en": {
        "title": "Responsible Advertising Index",
        "subtitle": "AI-Powered Assessment Tool Demo",
        "api_key_label": "Google AI API Key",
        "analyze_button": "🔍 Analyze Advertisement",
        "results_header": "📊 Analysis Results",
        "overall_score": "Overall Score",
        "dimension_breakdown": "Dimension Breakdown",
        "strengths": "✅ Strengths",
        "concerns": "⚠️ Concerns",
        "recommendations": "💡 Recommendations"
    },
    "hu": {
        "title": "Felelős Reklámindex",
        "subtitle": "AI-alapú Értékelő Eszköz Demó",
        "api_key_label": "Google AI API Kulcs",
        "analyze_button": "🔍 Reklám Elemzése",
        "results_header": "📊 Elemzési Eredmények",
        "overall_score": "Összpontszám",
        "dimension_breakdown": "Dimenziók Részletezése",
        "strengths": "✅ Erősségek",
        "concerns": "⚠️ Aggályok",
        "recommendations": "💡 Ajánlások"
    }
}

def detect_language(text: str) -> str:
    """Detect if the text is primarily Hungarian or English"""
    # Simple detection based on common Hungarian characters and words
    hungarian_chars = sum(1 for c in text if c in 'áéíóöőúüűÁÉÍÓÖŐÚÜŰ')
    hungarian_words = ['és', 'hogy', 'van', 'nem', 'egy', 'az', 'ezt', 'csak', 'még', 'vagy']
    hungarian_word_count = sum(1 for word in hungarian_words if word in text.lower())

    if hungarian_chars > 5 or hungarian_word_count > 2:
        return 'hu'
    return 'en'

def create_analysis_prompt(ad_copy: str, output_language: str = 'bilingual') -> str:
    """Create the prompt for Gemini to analyze the ad with language support"""

    # Detect the ad language
    ad_language = detect_language(ad_copy)

    if output_language == 'bilingual' or ad_language == 'hu':
        # Bilingual prompt for Hungarian ads or when bilingual output is requested
        prompt = f"""You are an expert in responsible advertising assessment. Analyze this advertisement across four key dimensions.

IMPORTANT: This ad may be in Hungarian. Please provide your analysis in BOTH English and Hungarian for maximum accessibility.

ADVERTISEMENT COPY:
{ad_copy}

FRAMEWORK / KERETRENDSZER:
{json.dumps(FRAMEWORK, indent=2)}

Please analyze this ad and provide:

1. A score (0-100) for each of the four dimensions:
   - Climate Responsibility / Klímafelelősség
   - Social Responsibility / Társadalmi Felelősség
   - Cultural Sensitivity / Kulturális Érzékenység
   - Ethical Communication / Etikus Kommunikáció

2. For each dimension, provide:
   - The score
   - 2-3 key findings in BOTH English and Hungarian (both strengths and risks)
   - Specific examples from the ad

3. An overall Responsibility Score (weighted average of the four dimensions)

4. A summary with:
   - Top 3 strengths (in both English and Hungarian)
   - Top 3 areas of concern or risk (in both English and Hungarian)
   - 2-3 recommendations for improvement (in both English and Hungarian)

CRITICAL: For Hungarian ads, be sensitive to Hungarian cultural context, local norms, and language nuances.

Please return your response in this EXACT JSON format (no markdown, just pure JSON):
{{
    "overall_score": <number 0-100>,
    "ad_language": "{ad_language}",
    "dimensions": {{
        "Climate Responsibility": {{
            "score": <number 0-100>,
            "findings": ["finding 1 (EN)", "finding 2 (EN)", "finding 3 (EN)"],
            "findings_hu": ["megállapítás 1 (HU)", "megállapítás 2 (HU)", "megállapítás 3 (HU)"]
        }},
        "Social Responsibility": {{
            "score": <number 0-100>,
            "findings": ["finding 1 (EN)", "finding 2 (EN)", "finding 3 (EN)"],
            "findings_hu": ["megállapítás 1 (HU)", "megállapítás 2 (HU)", "megállapítás 3 (HU)"]
        }},
        "Cultural Sensitivity": {{
            "score": <number 0-100>,
            "findings": ["finding 1 (EN)", "finding 2 (EN)", "finding 3 (EN)"],
            "findings_hu": ["megállapítás 1 (HU)", "megállapítás 2 (HU)", "megállapítás 3 (HU)"]
        }},
        "Ethical Communication": {{
            "score": <number 0-100>,
            "findings": ["finding 1 (EN)", "finding 2 (EN)", "finding 3 (EN)"],
            "findings_hu": ["megállapítás 1 (HU)", "megállapítás 2 (HU)", "megállapítás 3 (HU)"]
        }}
    }},
    "summary": {{
        "strengths": ["strength 1 (EN)", "strength 2 (EN)", "strength 3 (EN)"],
        "strengths_hu": ["erősség 1 (HU)", "erősség 2 (HU)", "erősség 3 (HU)"],
        "concerns": ["concern 1 (EN)", "concern 2 (EN)", "concern 3 (EN)"],
        "concerns_hu": ["aggály 1 (HU)", "aggály 2 (HU)", "aggály 3 (HU)"],
        "recommendations": ["rec 1 (EN)", "rec 2 (EN)", "rec 3 (EN)"],
        "recommendations_hu": ["ajánlás 1 (HU)", "ajánlás 2 (HU)", "ajánlás 3 (HU)"]
    }}
}}

Be specific and reference actual elements from the ad copy and image. For Hungarian content, maintain cultural sensitivity and understanding of local context."""
    else:
        # English-only prompt for English ads
        prompt = f"""You are an expert in responsible advertising assessment. Analyze this advertisement across four key dimensions.

ADVERTISEMENT COPY:
{ad_copy}

FRAMEWORK:
{json.dumps(FRAMEWORK, indent=2)}

Please analyze this ad and provide:

1. A score (0-100) for each of the four dimensions:
   - Climate Responsibility
   - Social Responsibility
   - Cultural Sensitivity
   - Ethical Communication

2. For each dimension, provide:
   - The score
   - 2-3 key findings (both strengths and risks)
   - Specific examples from the ad

3. An overall Responsibility Score (weighted average of the four dimensions)

4. A summary with:
   - Top 3 strengths
   - Top 3 areas of concern or risk
   - 2-3 recommendations for improvement

Please return your response in this EXACT JSON format (no markdown, just pure JSON):
{{
    "overall_score": <number 0-100>,
    "ad_language": "en",
    "dimensions": {{
        "Climate Responsibility": {{
            "score": <number 0-100>,
            "findings": ["finding 1", "finding 2", "finding 3"]
        }},
        "Social Responsibility": {{
            "score": <number 0-100>,
            "findings": ["finding 1", "finding 2", "finding 3"]
        }},
        "Cultural Sensitivity": {{
            "score": <number 0-100>,
            "findings": ["finding 1", "finding 2", "finding 3"]
        }},
        "Ethical Communication": {{
            "score": <number 0-100>,
            "findings": ["finding 1", "finding 2", "finding 3"]
        }}
    }},
    "summary": {{
        "strengths": ["strength 1", "strength 2", "strength 3"],
        "concerns": ["concern 1", "concern 2", "concern 3"],
        "recommendations": ["rec 1", "rec 2", "rec 3"]
    }}
}}

Be specific and reference actual elements from the ad copy and image."""

    return prompt

def analyze_ad(image_data: bytes, ad_copy: str, api_key: str) -> Dict:
    """Send the ad to Gemini for analysis"""
    
    # Configure Gemini
    genai.configure(api_key=api_key)
    
    # Use Gemini 2.5 Flash
    model = genai.GenerativeModel('models/gemini-2.5-flash')
    
    # Open image
    img = Image.open(io.BytesIO(image_data))
    
    # Create the prompt
    prompt = create_analysis_prompt(ad_copy)
    
    try:
        # Generate content with both image and text
        response = model.generate_content(
            [prompt, img],
            generation_config=genai.types.GenerationConfig(
                temperature=0.4,
                max_output_tokens=8000,  # Increased for bilingual detailed output
            )
        )
        
        # Get the response text
        response_text = response.text
        
        # Parse JSON from response
        try:
            # Try to find JSON in the response
            # Remove markdown code blocks if present
            if "```json" in response_text:
                start_idx = response_text.find("```json") + 7
                end_idx = response_text.find("```", start_idx)
                json_str = response_text[start_idx:end_idx].strip()
            elif "```" in response_text:
                start_idx = response_text.find("```") + 3
                end_idx = response_text.find("```", start_idx)
                json_str = response_text[start_idx:end_idx].strip()
            else:
                # Try to find JSON object directly
                start_idx = response_text.find('{')
                end_idx = response_text.rfind('}') + 1
                json_str = response_text[start_idx:end_idx]
            
            result = json.loads(json_str)
            return result
        except json.JSONDecodeError as e:
            st.error("Error parsing AI response. Raw response:")
            st.code(response_text)
            st.error(f"JSON Error: {str(e)}")
            return None
            
    except Exception as e:
        st.error(f"Error calling Gemini API: {str(e)}")
        return None

def create_radar_chart(scores: Dict, ad_name: str = "Ad") -> go.Figure:
    """Create a radar chart for the four dimensions"""
    
    categories = list(scores.keys())
    values = [scores[cat]["score"] for cat in categories]
    
    # Close the radar chart
    categories_closed = categories + [categories[0]]
    values_closed = values + [values[0]]
    
    fig = go.Figure()
    
    fig.add_trace(go.Scatterpolar(
        r=values_closed,
        theta=categories_closed,
        fill='toself',
        fillcolor='rgba(99, 110, 250, 0.3)',
        line=dict(color='rgb(99, 110, 250)', width=2),
        name=ad_name
    ))
    
    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 100],
                tickmode='linear',
                tick0=0,
                dtick=20
            )
        ),
        showlegend=False,
        height=400,
        margin=dict(l=80, r=80, t=40, b=40)
    )
    
    return fig

def create_comparison_radar_chart(analyses: List[Dict]) -> go.Figure:
    """Create an overlay radar chart comparing multiple ads"""
    
    fig = go.Figure()
    
    # Color palette for different ads
    colors_list = [
        'rgb(99, 110, 250)',
        'rgb(239, 85, 59)',
        'rgb(0, 204, 150)',
        'rgb(171, 99, 250)',
        'rgb(255, 161, 90)'
    ]
    
    for idx, analysis in enumerate(analyses):
        scores = analysis['result']['dimensions']
        categories = list(scores.keys())
        values = [scores[cat]["score"] for cat in categories]
        
        # Close the radar chart
        categories_closed = categories + [categories[0]]
        values_closed = values + [values[0]]
        
        color = colors_list[idx % len(colors_list)]
        
        fig.add_trace(go.Scatterpolar(
            r=values_closed,
            theta=categories_closed,
            fill='toself',
            fillcolor=color.replace('rgb', 'rgba').replace(')', ', 0.2)'),
            line=dict(color=color, width=2),
            name=analysis['brand_name']
        ))
    
    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 100],
                tickmode='linear',
                tick0=0,
                dtick=20
            )
        ),
        showlegend=True,
        height=500,
        margin=dict(l=80, r=80, t=40, b=40),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="center",
            x=0.5
        )
    )
    
    return fig

def create_gauge_chart(score: float) -> go.Figure:
    """Create a gauge chart for the overall score"""
    
    # Determine color based on score
    if score >= 80:
        color = "green"
    elif score >= 60:
        color = "orange"
    else:
        color = "red"
    
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=score,
        domain={'x': [0, 1], 'y': [0, 1]},
        title={'text': "Overall Responsibility Score"},
        gauge={
            'axis': {'range': [None, 100]},
            'bar': {'color': color},
            'steps': [
                {'range': [0, 40], 'color': "rgba(255, 0, 0, 0.1)"},
                {'range': [40, 70], 'color': "rgba(255, 165, 0, 0.1)"},
                {'range': [70, 100], 'color': "rgba(0, 255, 0, 0.1)"}
            ],
            'threshold': {
                'line': {'color': "black", 'width': 4},
                'thickness': 0.75,
                'value': score
            }
        }
    ))
    
    fig.update_layout(
        height=300,
        margin=dict(l=20, r=20, t=60, b=20)
    )
    
    return fig

def export_to_excel(analyses: List[Dict]) -> bytes:
    """Export analysis results to Excel format"""
    
    # Create DataFrame
    data = []
    for analysis in analyses:
        result = analysis['result']
        row = {
            'Brand': analysis['brand_name'],
            'Analysis Date': analysis['timestamp'],
            'Overall Score': result['overall_score'],
            'Climate Responsibility': result['dimensions']['Climate Responsibility']['score'],
            'Social Responsibility': result['dimensions']['Social Responsibility']['score'],
            'Cultural Sensitivity': result['dimensions']['Cultural Sensitivity']['score'],
            'Ethical Communication': result['dimensions']['Ethical Communication']['score'],
            'Rating': '⭐⭐⭐⭐⭐' if result['overall_score'] >= 90 else (
                     '⭐⭐⭐⭐' if result['overall_score'] >= 75 else (
                     '⭐⭐⭐' if result['overall_score'] >= 60 else '⭐⭐')),
            'Key Strengths': ' | '.join(result['summary']['strengths']),
            'Key Concerns': ' | '.join(result['summary']['concerns']),
            'Recommendations': ' | '.join(result['summary']['recommendations']),
            'Ad Copy (excerpt)': analysis['ad_copy'][:200] + '...' if len(analysis['ad_copy']) > 200 else analysis['ad_copy']
        }
        data.append(row)
    
    df = pd.DataFrame(data)
    
    # Create Excel file in memory
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df.to_excel(writer, sheet_name='RAI Analysis', index=False)
        
        # Get the workbook and worksheet
        workbook = writer.book
        worksheet = writer.sheets['RAI Analysis']
        
        # Adjust column widths
        for column in worksheet.columns:
            max_length = 0
            column_letter = column[0].column_letter
            for cell in column:
                try:
                    if len(str(cell.value)) > max_length:
                        max_length = len(str(cell.value))
                except:
                    pass
            adjusted_width = min(max_length + 2, 50)
            worksheet.column_dimensions[column_letter].width = adjusted_width
    
    return output.getvalue()

def generate_pdf_report(result: Dict, brand_name: str = "Unknown Brand", ad_copy: str = "") -> bytes:
    """Generate a PDF report of the analysis"""
    
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter,
                           rightMargin=72, leftMargin=72,
                           topMargin=72, bottomMargin=18)
    
    # Container for the 'Flowable' objects
    elements = []
    
    # Define styles
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=24,
        textColor=colors.HexColor('#1f77b4'),
        spaceAfter=30,
        alignment=TA_CENTER
    )
    
    heading_style = ParagraphStyle(
        'CustomHeading',
        parent=styles['Heading2'],
        fontSize=16,
        textColor=colors.HexColor('#1f77b4'),
        spaceAfter=12,
        spaceBefore=12
    )
    
    # Title
    title = Paragraph("Responsible Advertising Index", title_style)
    elements.append(title)
    
    subtitle = Paragraph(f"Analysis Report - {brand_name}", styles['Heading2'])
    elements.append(subtitle)
    
    date_para = Paragraph(f"Generated: {datetime.now().strftime('%B %d, %Y at %I:%M %p')}", styles['Normal'])
    elements.append(date_para)
    elements.append(Spacer(1, 20))
    
    # Executive Summary Box
    exec_summary = Paragraph("Executive Summary", heading_style)
    elements.append(exec_summary)
    
    overall_score = result['overall_score']
    score_color = colors.green if overall_score >= 80 else (colors.orange if overall_score >= 60 else colors.red)
    
    summary_data = [
        ['Overall Responsibility Score', f"{overall_score}/100"],
        ['Rating', 'Excellent' if overall_score >= 80 else ('Good' if overall_score >= 60 else 'Needs Improvement')]
    ]
    
    summary_table = Table(summary_data, colWidths=[4*inch, 2*inch])
    summary_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.lightgrey),
        ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 12),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
        ('BACKGROUND', (1, 0), (1, 0), score_color),
        ('TEXTCOLOR', (1, 0), (1, 0), colors.white),
    ]))
    
    elements.append(summary_table)
    elements.append(Spacer(1, 20))
    
    # Dimension Scores
    dimensions_header = Paragraph("Dimension Scores", heading_style)
    elements.append(dimensions_header)
    
    dim_data = [['Dimension', 'Score', 'Assessment']]
    for dim_name, dim_data_dict in result['dimensions'].items():
        score = dim_data_dict['score']
        assessment = '⭐⭐⭐⭐⭐' if score >= 90 else ('⭐⭐⭐⭐' if score >= 75 else ('⭐⭐⭐' if score >= 60 else '⭐⭐'))
        dim_data.append([dim_name, f"{score}/100", assessment])
    
    dim_table = Table(dim_data, colWidths=[3*inch, 1.5*inch, 1.5*inch])
    dim_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 12),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.lightgrey]),
    ]))
    
    elements.append(dim_table)
    elements.append(Spacer(1, 20))
    
    # Key Findings
    findings_header = Paragraph("Detailed Findings", heading_style)
    elements.append(findings_header)
    
    for dim_name, dim_data_dict in result['dimensions'].items():
        dim_title = Paragraph(f"<b>{dim_name}</b> ({dim_data_dict['score']}/100)", styles['Heading3'])
        elements.append(dim_title)
        
        for finding in dim_data_dict['findings']:
            finding_para = Paragraph(f"• {finding}", styles['Normal'])
            elements.append(finding_para)
        
        elements.append(Spacer(1, 10))
    
    # Page break before summary
    elements.append(PageBreak())
    
    # Strengths
    strengths_header = Paragraph("Key Strengths", heading_style)
    elements.append(strengths_header)
    
    for strength in result['summary']['strengths']:
        strength_para = Paragraph(f"✓ {strength}", styles['Normal'])
        elements.append(strength_para)
    
    elements.append(Spacer(1, 15))
    
    # Concerns
    concerns_header = Paragraph("Areas of Concern", heading_style)
    elements.append(concerns_header)
    
    for concern in result['summary']['concerns']:
        concern_para = Paragraph(f"⚠ {concern}", styles['Normal'])
        elements.append(concern_para)
    
    elements.append(Spacer(1, 15))
    
    # Recommendations
    recs_header = Paragraph("Recommendations", heading_style)
    elements.append(recs_header)
    
    for i, rec in enumerate(result['summary']['recommendations'], 1):
        rec_para = Paragraph(f"{i}. {rec}", styles['Normal'])
        elements.append(rec_para)
    
    elements.append(Spacer(1, 30))
    
    # Footer
    footer = Paragraph("This report was generated by the Responsible Advertising Index assessment tool.", 
                      styles['Italic'])
    elements.append(footer)
    
    # Build PDF
    doc.build(elements)
    
    # Get the value of the BytesIO buffer
    pdf_bytes = buffer.getvalue()
    buffer.close()
    
    return pdf_bytes

def generate_comparison_pdf(analyses: List[Dict]) -> bytes:
    """Generate a comparison PDF report for multiple ads"""
    
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter,
                           rightMargin=72, leftMargin=72,
                           topMargin=72, bottomMargin=18)
    
    elements = []
    styles = getSampleStyleSheet()
    
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=24,
        textColor=colors.HexColor('#1f77b4'),
        spaceAfter=30,
        alignment=TA_CENTER
    )
    
    heading_style = ParagraphStyle(
        'CustomHeading',
        parent=styles['Heading2'],
        fontSize=16,
        textColor=colors.HexColor('#1f77b4'),
        spaceAfter=12,
        spaceBefore=12
    )
    
    # Title
    title = Paragraph("Responsible Advertising Index", title_style)
    elements.append(title)
    
    subtitle = Paragraph(f"Comparison Report - {len(analyses)} Advertisements", styles['Heading2'])
    elements.append(subtitle)
    
    date_para = Paragraph(f"Generated: {datetime.now().strftime('%B %d, %Y at %I:%M %p')}", styles['Normal'])
    elements.append(date_para)
    elements.append(Spacer(1, 20))
    
    # Comparison Summary Table
    comp_header = Paragraph("Overall Comparison", heading_style)
    elements.append(comp_header)
    
    # Create comparison table
    table_data = [['Brand', 'Overall Score', 'Climate', 'Social', 'Cultural', 'Ethical']]
    
    for analysis in analyses:
        result = analysis['result']
        row = [
            analysis['brand_name'],
            f"{result['overall_score']}/100",
            f"{result['dimensions']['Climate Responsibility']['score']}",
            f"{result['dimensions']['Social Responsibility']['score']}",
            f"{result['dimensions']['Cultural Sensitivity']['score']}",
            f"{result['dimensions']['Ethical Communication']['score']}"
        ]
        table_data.append(row)
    
    comp_table = Table(table_data, colWidths=[2*inch, 1*inch, 0.8*inch, 0.8*inch, 0.8*inch, 0.8*inch])
    comp_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.lightgrey]),
    ]))
    
    elements.append(comp_table)
    elements.append(Spacer(1, 20))
    
    # Winner section
    winner = max(analyses, key=lambda x: x['result']['overall_score'])
    winner_header = Paragraph("🏆 Highest Score", heading_style)
    elements.append(winner_header)
    
    winner_text = Paragraph(
        f"<b>{winner['brand_name']}</b> achieved the highest overall score of "
        f"<b>{winner['result']['overall_score']}/100</b>",
        styles['Normal']
    )
    elements.append(winner_text)
    elements.append(Spacer(1, 30))
    
    # Individual analyses
    for idx, analysis in enumerate(analyses, 1):
        elements.append(PageBreak())
        
        brand_header = Paragraph(f"Advertisement {idx}: {analysis['brand_name']}", heading_style)
        elements.append(brand_header)
        
        result = analysis['result']
        
        # Score summary
        score_data = [
            ['Overall Score', f"{result['overall_score']}/100"],
            ['Climate Responsibility', f"{result['dimensions']['Climate Responsibility']['score']}/100"],
            ['Social Responsibility', f"{result['dimensions']['Social Responsibility']['score']}/100"],
            ['Cultural Sensitivity', f"{result['dimensions']['Cultural Sensitivity']['score']}/100"],
            ['Ethical Communication', f"{result['dimensions']['Ethical Communication']['score']}/100"]
        ]
        
        score_table = Table(score_data, colWidths=[3*inch, 2*inch])
        score_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, -1), colors.lightgrey),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ]))
        
        elements.append(score_table)
        elements.append(Spacer(1, 15))
        
        # Key strengths
        strengths_para = Paragraph("<b>Key Strengths:</b>", styles['Normal'])
        elements.append(strengths_para)
        for strength in result['summary']['strengths']:
            elements.append(Paragraph(f"✓ {strength}", styles['Normal']))
        
        elements.append(Spacer(1, 10))
        
        # Key concerns
        concerns_para = Paragraph("<b>Areas of Concern:</b>", styles['Normal'])
        elements.append(concerns_para)
        for concern in result['summary']['concerns']:
            elements.append(Paragraph(f"⚠ {concern}", styles['Normal']))
    
    # Build PDF
    doc.build(elements)
    
    pdf_bytes = buffer.getvalue()
    buffer.close()
    
    return pdf_bytes

# Main app
def main():
    # Initialize language preference in session state
    if 'display_language' not in st.session_state:
        st.session_state.display_language = 'en'

    # Display title based on language preference
    if st.session_state.display_language == 'hu':
        st.title("📊 Felelős Reklámindex")
        st.markdown("### AI-alapú Értékelő Eszköz Demó (Google Gemini)")
    else:
        st.title("📊 Responsible Advertising Index")
        st.markdown("### AI-Powered Assessment Tool Demo (Google Gemini)")

    st.markdown("---")

    # Sidebar for API key and info
    with st.sidebar:
        st.header("⚙️ Configuration / Konfiguráció")

        # Language selector
        display_lang = st.selectbox(
            "Interface Language / Felület Nyelve",
            options=['en', 'hu'],
            format_func=lambda x: "English 🇬🇧" if x == 'en' else "Magyar 🇭🇺",
            key='display_language'
        )

        # Try to load API key from .env file
        import os
        from pathlib import Path

        default_api_key = ""
        env_file = Path(__file__).parent / ".env"
        if env_file.exists():
            try:
                with open(env_file) as f:
                    for line in f:
                        if line.startswith("GOOGLE_API_KEY="):
                            default_api_key = line.split("=", 1)[1].strip()
                            break
            except:
                pass

        api_key = st.text_input("Google AI API Key",
                                value=default_api_key,
                                type="password",
                                help="Get your free API key at https://aistudio.google.com/app/apikey")

        st.markdown("---")
        st.markdown("""
        **💡 Getting Your API Key:**
        1. Go to [Google AI Studio](https://aistudio.google.com/app/apikey)
        2. Sign in with your Google account
        3. Click "Create API Key"
        4. Copy and paste it here
        """)
        
        st.markdown("---")
        
        # NEW: Analysis History Section
        st.header("📚 Analysis History")
        history_count = len(st.session_state.analysis_history)
        st.metric("Total Analyses", history_count)
        
        if history_count > 0:
            if st.button("🗑️ Clear History", use_container_width=True):
                st.session_state.analysis_history = []
                st.rerun()
            
            st.markdown("**Recent Analyses:**")
            for idx, analysis in enumerate(reversed(st.session_state.analysis_history[-5:]), 1):
                score = analysis['result']['overall_score']
                emoji = "🟢" if score >= 80 else ("🟡" if score >= 60 else "🔴")
                st.markdown(f"{emoji} {analysis['brand_name']} ({score})")
        
        st.markdown("---")
        st.header("📖 About / Rólunk")
        if st.session_state.display_language == 'hu':
            st.markdown("""
            Ez az eszköz négy dimenzió mentén értékeli a reklámokat:

            1. **Klímafelelősség** - Fenntarthatósági üzenetek és állítások
            2. **Társadalmi Felelősség** - Sokszínűség és befogadás
            3. **Kulturális Érzékenység** - Tiszteletteljes megjelenítés
            4. **Etikus Kommunikáció** - Átláthatóság és őszinteség

            Töltsön fel egy reklámképet és adja meg a szöveget egy átfogó felelősségi értékeléshez.
            """)
        else:
            st.markdown("""
            This tool evaluates advertisements across four dimensions:

            1. **Climate Responsibility** - Sustainability messaging and claims
            2. **Social Responsibility** - Diversity and inclusion
            3. **Cultural Sensitivity** - Respectful representation
            4. **Ethical Communication** - Transparency and truthfulness

            Upload an ad image and provide the copy to get a comprehensive responsibility assessment.
            """)
        
        st.markdown("---")
        st.header("🎯 Framework")
        for dimension, details in FRAMEWORK.items():
            with st.expander(dimension):
                st.markdown(f"**Weight:** {details['weight']*100}%")
                st.markdown("**Key Indicators:**")
                for indicator in details['indicators']:
                    st.markdown(f"- {indicator}")
    
    # Main content
    # NEW: Add tab navigation for single vs comparison analysis
    main_tab, video_tab, comparison_tab, export_tab = st.tabs(["📤 Image Analysis", "📹 Video Analysis", "🔄 Compare Ads", "📊 Export Data"])
    
    # ============ TAB 1: SINGLE ANALYSIS ============
    with main_tab:
        st.header("📤 Advertisement Input")
        
        # Example ads section
        st.subheader("🎨 Try an Example Ad")

        # Create columns based on number of example ads
        num_examples = len(EXAMPLE_ADS)
        cols = st.columns(num_examples)

        for idx, (example_name, example_data) in enumerate(EXAMPLE_ADS.items()):
            with cols[idx]:
                if st.button(example_name, key=f"example_{idx}", use_container_width=True):
                    st.session_state['example_ad'] = example_data
                    st.session_state['brand_name'] = example_data['brand']
                    st.session_state['ad_copy'] = example_data['copy']
                    st.rerun()
        
        st.markdown("---")
        st.subheader("📋 Or Upload Your Own")
        
        col1, col2 = st.columns([1, 1])
        
        with col1:
            uploaded_file = st.file_uploader("Upload ad image", type=['png', 'jpg', 'jpeg'])
            
            # Show example ad image if selected
            if 'example_ad' in st.session_state and not uploaded_file:
                # Generate example image
                example_image_data = create_example_image(st.session_state['example_ad']['image_type'])
                st.image(example_image_data, caption=f"Example: {st.session_state['brand_name']}", use_column_width=True)
                st.info(f"📝 {st.session_state['example_ad']['image_description']}")
                st.info(f"⭐ Expected score: ~{st.session_state['example_ad']['expected_score']}/100")
            
            if uploaded_file:
                st.image(uploaded_file, caption="Uploaded Advertisement", use_column_width=True)
        
        with col2:
            # Pre-fill with example if selected
            default_copy = st.session_state.get('ad_copy', '')
            default_brand = st.session_state.get('brand_name', '')
            
            brand_name = st.text_input("Brand Name", value=default_brand, placeholder="e.g., Nike, Patagonia...")
            
            ad_copy = st.text_area(
                "Advertisement Copy/Text",
                value=default_copy,
                height=300,
                placeholder="Paste the headline, body copy, and any text that appears in the ad..."
            )
            
            if st.button("🔍 Analyze Advertisement", type="primary", use_container_width=True):
                if not api_key:
                    st.error("⚠️ Please enter your Google AI API key in the sidebar")
                    st.info("👉 Get a free API key at: https://aistudio.google.com/app/apikey")
                elif not uploaded_file and 'example_ad' not in st.session_state:
                    st.error("⚠️ Please upload an advertisement image or select an example")
                elif not ad_copy:
                    st.error("⚠️ Please provide the advertisement copy")
                else:
                    with st.spinner("Analyzing advertisement with Google Gemini..."):
                        # Get image data
                        if not uploaded_file and 'example_ad' in st.session_state:
                            image_data = create_example_image(st.session_state['example_ad']['image_type'])
                        else:
                            image_data = uploaded_file.read()
                        
                        # Analyze
                        result = analyze_ad(image_data, ad_copy, api_key)
                        
                        if result:
                            # Store in session state
                            st.session_state['result'] = result
                            st.session_state['current_brand'] = brand_name
                            st.session_state['current_copy'] = ad_copy
                            
                            # NEW: Add to history
                            analysis_entry = {
                                'brand_name': brand_name,
                                'ad_copy': ad_copy,
                                'result': result,
                                'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                            }
                            st.session_state.analysis_history.append(analysis_entry)
                            
                            st.success("✅ Analysis complete!")
                            # Clear example selection
                            if 'example_ad' in st.session_state:
                                del st.session_state['example_ad']
        
        # Display results if available
        if 'result' in st.session_state:
            result = st.session_state['result']
            brand_name = st.session_state.get('current_brand', 'Unknown Brand')
            ad_copy = st.session_state.get('current_copy', '')
            
            st.markdown("---")
            st.header("📊 Analysis Results")
            
            # Overall score with better visual
            col1, col2, col3 = st.columns([1, 2, 1])
            
            with col1:
                st.markdown("### Overall Score")
                score = result['overall_score']
                if score >= 80:
                    st.success(f"# {score}")
                    st.success("⭐ Excellent")
                elif score >= 60:
                    st.warning(f"# {score}")
                    st.warning("⚠️ Good")
                else:
                    st.error(f"# {score}")
                    st.error("❌ Needs Improvement")
            
            with col2:
                st.markdown("### Dimension Breakdown")
                st.plotly_chart(create_radar_chart(result['dimensions'], brand_name), use_container_width=True)
            
            with col3:
                st.markdown("### Quick Stats")
                avg_score = sum([d['score'] for d in result['dimensions'].values()]) / len(result['dimensions'])
                st.metric("Average Dimension", f"{avg_score:.1f}")
                
                high_scores = sum(1 for d in result['dimensions'].values() if d['score'] >= 80)
                st.metric("High Scores (80+)", high_scores)
                
                low_scores = sum(1 for d in result['dimensions'].values() if d['score'] < 60)
                st.metric("Areas for Improvement", low_scores)
            
            st.markdown("---")
            
            # Detailed findings with better layout
            st.header("🔍 Detailed Analysis")
            
            tabs = st.tabs(list(result['dimensions'].keys()) + ["Summary"])
            
            # Dimension tabs
            for i, (dimension, data) in enumerate(result['dimensions'].items()):
                with tabs[i]:
                    score = data['score']
                    
                    # Score with color coding and visual indicator
                    col1, col2 = st.columns([1, 3])
                    with col1:
                        if score >= 80:
                            st.success(f"# {score}/100")
                            st.success("⭐⭐⭐⭐⭐")
                        elif score >= 60:
                            st.warning(f"# {score}/100")
                            st.warning("⭐⭐⭐⭐")
                        else:
                            st.error(f"# {score}/100")
                            st.error("⭐⭐⭐")
                    
                    with col2:
                        # Check if bilingual findings exist
                        has_hungarian = 'findings_hu' in data

                        if has_hungarian and st.session_state.display_language == 'hu':
                            st.markdown("### Főbb Megállapítások:")
                            for finding in data['findings_hu']:
                                st.markdown(f"• {finding}")
                            with st.expander("Show English / Angol verzió"):
                                for finding in data['findings']:
                                    st.markdown(f"• {finding}")
                        elif has_hungarian:
                            st.markdown("### Key Findings:")
                            for finding in data['findings']:
                                st.markdown(f"• {finding}")
                            with st.expander("Show Hungarian / Magyar verzió"):
                                for finding in data['findings_hu']:
                                    st.markdown(f"• {finding}")
                        else:
                            st.markdown("### Key Findings:")
                            for finding in data['findings']:
                                st.markdown(f"• {finding}")

            # Summary tab with better visualization
            with tabs[-1]:
                col1, col2, col3 = st.columns(3)

                # Check if bilingual summary exists
                has_hungarian_summary = 'strengths_hu' in result['summary']
                display_lang = st.session_state.display_language

                with col1:
                    if display_lang == 'hu' and has_hungarian_summary:
                        st.markdown("### ✅ Erősségek")
                        for i, strength in enumerate(result['summary']['strengths_hu'], 1):
                            st.success(f"{i}. {strength}")
                        with st.expander("English"):
                            for i, strength in enumerate(result['summary']['strengths'], 1):
                                st.markdown(f"{i}. {strength}")
                    else:
                        st.markdown("### ✅ Strengths")
                        for i, strength in enumerate(result['summary']['strengths'], 1):
                            st.success(f"{i}. {strength}")
                        if has_hungarian_summary:
                            with st.expander("Magyar"):
                                for i, strength in enumerate(result['summary']['strengths_hu'], 1):
                                    st.markdown(f"{i}. {strength}")

                with col2:
                    if display_lang == 'hu' and has_hungarian_summary:
                        st.markdown("### ⚠️ Aggályok")
                        for i, concern in enumerate(result['summary']['concerns_hu'], 1):
                            st.warning(f"{i}. {concern}")
                        with st.expander("English"):
                            for i, concern in enumerate(result['summary']['concerns'], 1):
                                st.markdown(f"{i}. {concern}")
                    else:
                        st.markdown("### ⚠️ Concerns")
                        for i, concern in enumerate(result['summary']['concerns'], 1):
                            st.warning(f"{i}. {concern}")
                        if has_hungarian_summary:
                            with st.expander("Magyar"):
                                for i, concern in enumerate(result['summary']['concerns_hu'], 1):
                                    st.markdown(f"{i}. {concern}")

                with col3:
                    if display_lang == 'hu' and has_hungarian_summary:
                        st.markdown("### 💡 Ajánlások")
                        for i, rec in enumerate(result['summary']['recommendations_hu'], 1):
                            st.info(f"{i}. {rec}")
                        with st.expander("English"):
                            for i, rec in enumerate(result['summary']['recommendations'], 1):
                                st.markdown(f"{i}. {rec}")
                    else:
                        st.markdown("### 💡 Recommendations")
                        for i, rec in enumerate(result['summary']['recommendations'], 1):
                            st.info(f"{i}. {rec}")
                        if has_hungarian_summary:
                            with st.expander("Magyar"):
                                for i, rec in enumerate(result['summary']['recommendations_hu'], 1):
                                    st.markdown(f"{i}. {rec}")
            
            st.markdown("---")
            
            # Export options
            st.header("📥 Export Results")
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                # PDF Download
                pdf_bytes = generate_pdf_report(result, brand_name, ad_copy)
                st.download_button(
                    label="📄 Download PDF Report",
                    data=pdf_bytes,
                    file_name=f"RAI_Report_{brand_name.replace(' ', '_')}_{datetime.now().strftime('%Y%m%d')}.pdf",
                    mime="application/pdf",
                    use_container_width=True
                )
            
            with col2:
                # JSON Download
                json_str = json.dumps(result, indent=2)
                st.download_button(
                    label="📊 Download JSON Data",
                    data=json_str,
                    file_name=f"RAI_Data_{brand_name.replace(' ', '_')}_{datetime.now().strftime('%Y%m%d')}.json",
                    mime="application/json",
                    use_container_width=True
                )
            
            with col3:
                # Share/Copy button (copies JSON to clipboard)
                if st.button("📋 Copy Results", use_container_width=True):
                    st.code(json_str, language="json")
                    st.success("✅ Results displayed above - copy as needed")

    # ============ TAB 2: VIDEO ANALYSIS ============
    with video_tab:
        st.header("📹 Video Advertisement Analysis")

        st.info("""
        📋 **Supported Formats:** MP4, MOV, AVI, WebM
        ⏱️ **Duration:** Up to 3 minutes recommended
        📦 **File Size:** Max 200MB
        🌍 **Languages:** English, Hungarian
        💰 **Cost:** ~$0.01-0.02 per video
        """)

        col1, col2 = st.columns([1, 1])

        with col1:
            uploaded_video = st.file_uploader(
                "Upload video advertisement",
                type=['mp4', 'mov', 'avi', 'webm'],
                help="Maximum 200MB, 3 minutes duration"
            )

            if uploaded_video:
                st.video(uploaded_video)

                # Show video metadata
                try:
                    from video_utils import get_video_metadata, format_duration, estimate_cost

                    video_bytes = uploaded_video.read()
                    uploaded_video.seek(0)  # Reset for later use

                    metadata = get_video_metadata(video_bytes)

                    col_a, col_b, col_c = st.columns(3)
                    col_a.metric("File Size", f"{metadata['size_mb']:.1f} MB")
                    col_b.metric("Duration", format_duration(metadata['duration']))
                    col_c.metric("Est. Cost", f"${estimate_cost(metadata['duration']):.3f}")

                    st.caption(f"Resolution: {metadata['width']}x{metadata['height']} | FPS: {metadata['fps']:.1f} | Codec: {metadata['codec']}")

                except Exception as e:
                    st.warning(f"Could not read video metadata: {e}")

        with col2:
            brand_name_video = st.text_input(
                "Brand Name (Video)",
                placeholder="e.g., Telekom, Nike..."
            )

            ad_copy_video = st.text_area(
                "Additional Context (Optional)",
                placeholder="Any text from the ad, script, or additional context...",
                height=200,
                help="Optional: Provide any text, script, or context about the video"
            )

            st.markdown("---")

            analyze_button_video = st.button(
                "🎬 Analyze Video",
                type="primary",
                use_container_width=True,
                disabled=not uploaded_video or not api_key
            )

        # Analysis section
        if analyze_button_video and uploaded_video and api_key:
            from video_processor import VideoAnalyzer
            from video_utils import validate_video

            # Read video
            video_bytes = uploaded_video.read()

            # Validate video
            with st.spinner("Validating video..."):
                is_valid, message, metadata = validate_video(video_bytes)

            if not is_valid:
                st.error(f"❌ Video validation failed: {message}")
            else:
                st.success(f"✅ Video validation passed: {message}")

                # Detect language from ad copy
                detected_lang = detect_language(ad_copy_video) if ad_copy_video else 'en'

                # Analyze video
                progress_bar = st.progress(0)
                status_text = st.empty()

                try:
                    status_text.text("⬆️ Uploading video to Google's servers...")
                    progress_bar.progress(20)

                    analyzer = VideoAnalyzer(api_key=api_key)

                    status_text.text("🤖 Analyzing video with Gemini AI...")
                    progress_bar.progress(40)

                    result = analyzer.analyze_video(
                        video_bytes=video_bytes,
                        ad_copy=ad_copy_video,
                        detected_language=detected_lang
                    )

                    progress_bar.progress(100)
                    status_text.success("✅ Analysis complete!")

                    # Store in history
                    st.session_state.analysis_history.append({
                        'timestamp': datetime.now(),
                        'brand': brand_name_video or "Unknown",
                        'type': 'video',
                        'duration': metadata['duration'] if metadata else 0,
                        'result': result
                    })

                    # Display results
                    st.markdown("---")
                    st.subheader("📊 Analysis Results")

                    # Overall score with gauge
                    col1, col2 = st.columns([1, 2])

                    with col1:
                        st.metric("Overall Score", f"{result.get('overall_score', 0)}/100")
                        st.caption(f"Duration: {result.get('duration_analyzed', 'N/A')}")
                        st.caption(f"Language: {result.get('detected_language', 'N/A').upper()}")

                    with col2:
                        # Create gauge chart
                        fig_gauge = create_gauge_chart(result.get('overall_score', 0))
                        st.plotly_chart(fig_gauge, use_container_width=True)

                    # Radar chart
                    st.subheader("📈 Dimension Scores")
                    dimension_scores = {
                        dim: data.get('score', 0)
                        for dim, data in result.get('dimensions', {}).items()
                    }
                    fig_radar = create_radar_chart(dimension_scores, brand_name_video or "Video Ad")
                    st.plotly_chart(fig_radar, use_container_width=True)

                    # Video transcript
                    if 'transcript' in result and result['transcript']:
                        with st.expander("📝 Video Transcript"):
                            st.text(result['transcript'])

                    # Temporal analysis
                    if 'temporal_analysis' in result:
                        st.subheader("⏱️ Temporal Analysis")
                        temporal = result['temporal_analysis']

                        if 'messaging_evolution' in temporal:
                            st.markdown(f"**Message Evolution:** {temporal['messaging_evolution']}")

                        if 'key_moments' in temporal and temporal['key_moments']:
                            st.markdown("**Key Moments:**")
                            for moment in temporal['key_moments']:
                                st.markdown(f"- **{moment.get('timestamp', 'N/A')}**: {moment.get('event', 'N/A')}")

                        if 'audio_visual_alignment' in temporal:
                            alignment = temporal['audio_visual_alignment']
                            if alignment == 'consistent':
                                st.success(f"✅ Audio-Visual Alignment: {alignment}")
                            else:
                                st.warning(f"⚠️ Audio-Visual Alignment: {alignment}")

                    # Scene breakdown
                    if 'scenes' in result and result['scenes']:
                        st.subheader("🎬 Scene-by-Scene Breakdown")
                        for idx, scene in enumerate(result['scenes']):
                            with st.expander(f"Scene {idx+1}: {scene.get('timestamp', 'N/A')}"):
                                st.markdown(f"**Description:** {scene.get('description', 'N/A')}")

                                if 'visual_elements' in scene:
                                    st.markdown("**Visual Elements:**")
                                    for elem in scene['visual_elements']:
                                        st.markdown(f"- {elem}")

                                if 'audio_content' in scene:
                                    st.markdown(f"**Audio:** {scene['audio_content']}")

                                # Scene scores
                                scene_cols = st.columns(4)
                                scene_cols[0].metric("Climate", f"{scene.get('climate_score', 0)}")
                                scene_cols[1].metric("Social", f"{scene.get('social_score', 0)}")
                                scene_cols[2].metric("Cultural", f"{scene.get('cultural_score', 0)}")
                                scene_cols[3].metric("Ethical", f"{scene.get('ethical_score', 0)}")

                    # Detailed findings per dimension
                    st.subheader("🔍 Detailed Findings")

                    # Determine which language to show first
                    show_language = ui_language  # Use interface language setting

                    for dim_name, dim_data in result.get('dimensions', {}).items():
                        with st.expander(f"{dim_name}: {dim_data.get('score', 0)}/100"):
                            # Show findings in primary language
                            findings_key = 'findings_hu' if show_language == 'hu' and 'findings_hu' in dim_data else 'findings'
                            findings = dim_data.get(findings_key, [])

                            for finding in findings:
                                st.markdown(f"- {finding}")

                            # Option to toggle language
                            if 'findings_hu' in dim_data and 'findings' in dim_data:
                                alt_lang = 'en' if show_language == 'hu' else 'hu'
                                alt_findings_key = 'findings' if show_language == 'hu' else 'findings_hu'
                                alt_findings = dim_data.get(alt_findings_key, [])

                                lang_label = "Show in English" if show_language == 'hu' else "Mutasd magyarul"
                                if st.checkbox(lang_label, key=f"lang_toggle_video_{dim_name}"):
                                    st.markdown(f"**{dim_name} ({'English' if alt_lang == 'en' else 'Magyar'}):**")
                                    for finding in alt_findings:
                                        st.markdown(f"- {finding}")

                    # Summary
                    if 'summary' in result:
                        st.subheader("📝 Summary")
                        summary = result['summary']

                        # Determine summary language
                        strengths_key = 'strengths_hu' if show_language == 'hu' and 'strengths_hu' in summary else 'strengths'
                        concerns_key = 'concerns_hu' if show_language == 'hu' and 'concerns_hu' in summary else 'concerns'
                        recs_key = 'recommendations_hu' if show_language == 'hu' and 'recommendations_hu' in summary else 'recommendations'

                        col1, col2, col3 = st.columns(3)

                        with col1:
                            st.markdown("**✅ Strengths:**")
                            for strength in summary.get(strengths_key, []):
                                st.markdown(f"- {strength}")

                        with col2:
                            st.markdown("**⚠️ Concerns:**")
                            for concern in summary.get(concerns_key, []):
                                st.markdown(f"- {concern}")

                        with col3:
                            st.markdown("**💡 Recommendations:**")
                            for rec in summary.get(recs_key, []):
                                st.markdown(f"- {rec}")

                except Exception as e:
                    progress_bar.progress(0)
                    status_text.error(f"❌ Analysis failed: {str(e)}")
                    st.exception(e)

    # ============ TAB 3: COMPARISON ============
    with comparison_tab:
        st.header("🔄 Compare Multiple Advertisements")
        
        if len(st.session_state.analysis_history) < 2:
            st.info("📝 You need at least 2 analyzed ads to use comparison. Analyze some ads in the 'Single Analysis' tab first!")
        else:
            st.markdown("### Select Ads to Compare (2-5 ads)")
            
            # Create selection options
            ad_options = {
                f"{analysis['brand_name']} ({analysis['result']['overall_score']})": idx 
                for idx, analysis in enumerate(st.session_state.analysis_history)
            }
            
            selected_ad_names = st.multiselect(
                "Choose ads to compare:",
                options=list(ad_options.keys()),
                max_selections=5,
                help="Select 2-5 ads for comparison"
            )
            
            if len(selected_ad_names) >= 2:
                # Get selected analyses
                selected_indices = [ad_options[name] for name in selected_ad_names]
                selected_analyses = [st.session_state.analysis_history[idx] for idx in selected_indices]
                
                st.markdown("---")
                st.header("📊 Comparison Results")
                
                # Overall comparison table
                st.subheader("Overall Scores")
                
                comp_data = []
                for analysis in selected_analyses:
                    result = analysis['result']
                    comp_data.append({
                        'Brand': analysis['brand_name'],
                        'Overall': result['overall_score'],
                        'Climate': result['dimensions']['Climate Responsibility']['score'],
                        'Social': result['dimensions']['Social Responsibility']['score'],
                        'Cultural': result['dimensions']['Cultural Sensitivity']['score'],
                        'Ethical': result['dimensions']['Ethical Communication']['score']
                    })
                
                comp_df = pd.DataFrame(comp_data)
                
                # Highlight winner
                winner_idx = comp_df['Overall'].idxmax()
                
                # Display with styling
                def highlight_winner(row):
                    if row.name == winner_idx:
                        return ['background-color: #d4edda'] * len(row)
                    return [''] * len(row)
                
                styled_df = comp_df.style.apply(highlight_winner, axis=1)
                st.dataframe(styled_df, use_container_width=True)
                
                st.success(f"🏆 **Winner:** {comp_df.loc[winner_idx, 'Brand']} with overall score of {comp_df.loc[winner_idx, 'Overall']}")
                
                st.markdown("---")
                
                # Radar chart comparison
                st.subheader("Dimension Comparison")
                comparison_radar = create_comparison_radar_chart(selected_analyses)
                st.plotly_chart(comparison_radar, use_container_width=True)
                
                st.markdown("---")
                
                # Side-by-side detailed comparison
                st.subheader("Detailed Comparison")
                
                cols = st.columns(len(selected_analyses))
                
                for idx, (col, analysis) in enumerate(zip(cols, selected_analyses)):
                    with col:
                        result = analysis['result']
                        is_winner = idx == winner_idx
                        
                        if is_winner:
                            st.markdown(f"### 🏆 {analysis['brand_name']}")
                        else:
                            st.markdown(f"### {analysis['brand_name']}")
                        
                        st.metric("Overall Score", result['overall_score'])
                        
                        st.markdown("**Top Strengths:**")
                        for strength in result['summary']['strengths'][:2]:
                            st.success(f"✓ {strength}")
                        
                        st.markdown("**Key Concerns:**")
                        for concern in result['summary']['concerns'][:2]:
                            st.warning(f"⚠ {concern}")
                
                st.markdown("---")
                
                # Export comparison
                st.header("📥 Export Comparison")
                
                col1, col2 = st.columns(2)
                
                with col1:
                    # Comparison PDF
                    comp_pdf_bytes = generate_comparison_pdf(selected_analyses)
                    st.download_button(
                        label="📄 Download Comparison PDF",
                        data=comp_pdf_bytes,
                        file_name=f"RAI_Comparison_{len(selected_analyses)}ads_{datetime.now().strftime('%Y%m%d')}.pdf",
                        mime="application/pdf",
                        use_container_width=True
                    )
                
                with col2:
                    # Comparison Excel
                    comp_excel_bytes = export_to_excel(selected_analyses)
                    st.download_button(
                        label="📊 Download Comparison Excel",
                        data=comp_excel_bytes,
                        file_name=f"RAI_Comparison_{len(selected_analyses)}ads_{datetime.now().strftime('%Y%m%d')}.xlsx",
                        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                        use_container_width=True
                    )
            
            elif len(selected_ad_names) == 1:
                st.info("👉 Select at least one more ad to compare")
    
    # ============ TAB 3: EXPORT DATA ============
    with export_tab:
        st.header("📊 Export All Analysis Data")
        
        if len(st.session_state.analysis_history) == 0:
            st.info("📝 No analyses to export yet. Analyze some ads first!")
        else:
            st.markdown(f"### You have {len(st.session_state.analysis_history)} analyses in your history")
            
            # Preview data
            st.subheader("Data Preview")
            
            preview_data = []
            for analysis in st.session_state.analysis_history[-10:]:  # Show last 10
                result = analysis['result']
                preview_data.append({
                    'Brand': analysis['brand_name'],
                    'Date': analysis['timestamp'],
                    'Score': result['overall_score'],
                    'Climate': result['dimensions']['Climate Responsibility']['score'],
                    'Social': result['dimensions']['Social Responsibility']['score']
                })
            
            preview_df = pd.DataFrame(preview_data)
            st.dataframe(preview_df, use_container_width=True)
            
            st.markdown("---")
            
            # Export options
            st.subheader("Export Options")
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                # Export all as Excel
                all_excel_bytes = export_to_excel(st.session_state.analysis_history)
                st.download_button(
                    label=f"📊 Export All ({len(st.session_state.analysis_history)} ads) to Excel",
                    data=all_excel_bytes,
                    file_name=f"RAI_All_Analyses_{datetime.now().strftime('%Y%m%d')}.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                    use_container_width=True
                )
            
            with col2:
                # Export all as JSON
                all_json = json.dumps(st.session_state.analysis_history, indent=2)
                st.download_button(
                    label=f"📄 Export All ({len(st.session_state.analysis_history)} ads) to JSON",
                    data=all_json,
                    file_name=f"RAI_All_Analyses_{datetime.now().strftime('%Y%m%d')}.json",
                    mime="application/json",
                    use_container_width=True
                )
            
            with col3:
                # Export summary stats
                st.metric("Average Score", f"{sum(a['result']['overall_score'] for a in st.session_state.analysis_history) / len(st.session_state.analysis_history):.1f}")
                st.metric("Highest Score", max(a['result']['overall_score'] for a in st.session_state.analysis_history))
                st.metric("Lowest Score", min(a['result']['overall_score'] for a in st.session_state.analysis_history))

if __name__ == "__main__":
    main()

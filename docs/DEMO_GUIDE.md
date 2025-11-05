# Responsible Advertising Index Demo - Complete Guide

## Table of Contents
1. How Streamlit Works
2. Detailed Scoring Framework
3. Sample Ads for Demo
4. Setup & Running Instructions
5. Demo Tips

---

## 1. HOW STREAMLIT WORKS

### The Basics
Streamlit is a Python framework that turns data scripts into interactive web apps with minimal code. Here's what makes it special:

**Key Concepts:**

1. **Script-based**: Your entire app is just a Python script that runs top-to-bottom
2. **Automatic re-runs**: When a user interacts (clicks button, uploads file), the entire script re-runs
3. **State management**: Use `st.session_state` to persist data between re-runs
4. **Built-in widgets**: Input boxes, buttons, file uploads, charts - all pre-built

**How Our App Works:**

```python
import streamlit as st

# This runs every time the user interacts
st.title("My App")  # Creates a title

# Widget - this creates an upload button
uploaded_file = st.file_uploader("Upload image")

# Button - returns True when clicked
if st.button("Analyze"):
    # This code only runs when button is clicked
    result = analyze(uploaded_file)
    st.write(result)  # Display result
```

**The Magic:**
- You never write HTML/CSS/JavaScript
- You never manage server state manually
- Streamlit handles all the web stuff for you
- You just write Python with `st.` commands

**Layout:**
```python
# Columns
col1, col2 = st.columns(2)
with col1:
    st.write("Left side")
with col2:
    st.write("Right side")

# Sidebar
with st.sidebar:
    st.write("This appears in sidebar")

# Tabs
tab1, tab2 = st.tabs(["Tab 1", "Tab 2"])
with tab1:
    st.write("Tab 1 content")
```

---

## 2. DETAILED SCORING FRAMEWORK

### How Scoring Works

Each dimension is scored 0-100 based on multiple indicators. The AI (Claude) evaluates both the image and text together.

### Dimension 1: Climate Responsibility (25% weight)

**What we're measuring:**
- Is there sustainability messaging? Is it genuine or greenwashing?
- Are environmental claims specific and verifiable?
- Does the ad promote climate-positive behaviors?

**Scoring Guide:**
- **90-100**: Strong, authentic sustainability messaging with verifiable claims
- **70-89**: Positive environmental messaging but may lack specifics
- **50-69**: Minimal or vague environmental references
- **30-49**: No environmental messaging OR contains greenwashing red flags
- **0-29**: Actively promotes unsustainable practices or clear greenwashing

**Red Flags (lowers score):**
- Vague terms: "eco-friendly," "green," "natural" without specifics
- Unsubstantiated claims about carbon neutrality
- Focus on minor improvements while ignoring major impacts
- "Green" imagery not backed by actual practices

**Green Flags (raises score):**
- Specific certifications or standards mentioned
- Transparent about limitations ("we're working toward...")
- Promotes repair, reuse, or circular economy
- Shows concrete actions with measurable outcomes

---

### Dimension 2: Social Responsibility (25% weight)

**What we're measuring:**
- Diversity and representation across multiple dimensions
- Avoidance of stereotypes
- Empowerment vs. tokenism

**Scoring Guide:**
- **90-100**: Authentic, diverse representation with people in empowered roles
- **70-89**: Good diversity but may be surface-level or limited to one dimension
- **50-69**: Limited diversity or some stereotypical representations
- **30-49**: Homogeneous representation or reinforces stereotypes
- **0-29**: Actively harmful stereotypes or exclusionary messaging

**What to look for:**
- Gender: Are women shown in leadership/technical roles or just caregiving?
- Race/Ethnicity: Is diversity tokenistic (one person of color in background)?
- Age: Are older adults shown as active and capable?
- Body type: Is there size diversity beyond fashion/beauty ads?
- Disability: Are people with disabilities present and not defined by disability?

**Red Flags:**
- Women only in domestic/beauty contexts
- People of color as props in background
- Older adults shown as confused by technology
- Only thin, able-bodied people shown
- LGBTQ+ people used for "pride-washing" without authentic support

**Green Flags:**
- Diverse casting that reflects reality
- People in roles that challenge stereotypes
- Disability inclusion that feels natural
- Multi-generational representation
- Intersectional representation (not just one dimension)

---

### Dimension 3: Cultural Sensitivity (25% weight)

**What we're measuring:**
- Respect for cultural symbols and traditions
- Awareness of local contexts
- Avoidance of appropriation

**Scoring Guide:**
- **90-100**: Culturally informed, respectful, locally resonant
- **70-89**: Generally respectful but may miss some nuances
- **50-69**: Surface-level cultural references, some insensitivity
- **30-49**: Cultural appropriation or insensitive imagery
- **0-29**: Offensive cultural misrepresentation

**Key Questions:**
- Are cultural symbols used meaningfully or as aesthetic?
- Does humor translate across cultures or rely on stereotypes?
- Is religious imagery used respectfully?
- Are geopolitical sensitivities considered?
- Does the ad feel locally relevant or just globally imposed?

**Red Flags:**
- Sacred symbols used decoratively
- Cultural traditions shown inaccurately
- Insensitive timing (e.g., tone-deaf during local crisis)
- Stereotypical accents or costumes
- Reducing cultures to clichés

**Green Flags:**
- Consultants or creators from the culture represented
- Nuanced understanding of local context
- Respectful adaptation rather than appropriation
- Cultural celebration done authentically

---

### Dimension 4: Ethical Communication (25% weight)

**What we're measuring:**
- Honesty and transparency
- Avoidance of manipulation
- Respect for consumer autonomy

**Scoring Guide:**
- **90-100**: Transparent, honest, empowering communication
- **70-89**: Generally truthful but may use mild persuasion tactics
- **50-69**: Some exaggeration or emotional manipulation
- **30-49**: Misleading claims or exploitative tactics
- **0-29**: Deceptive or harmful manipulation

**Key Questions:**
- Are claims verifiable?
- Is sponsored content clearly disclosed?
- Does it manipulate through fear, shame, or insecurity?
- Are comparisons fair and accurate?
- Does it respect consumer intelligence?

**Red Flags:**
- "Miracle" claims without evidence
- Before/after images that are misleading
- Creating fear/anxiety to sell products
- Body-shaming or insecurity-driven messaging
- Hidden costs or conditions
- Influencer partnerships without #ad disclosure

**Green Flags:**
- Clear, honest product claims
- Transparent about partnerships
- Educational rather than manipulative
- Acknowledges product limitations
- Empowers rather than exploits

---

## 3. SAMPLE ADS FOR DEMO

### Strategy: Use 5 Contrasting Examples

You want ads that will score differently to show the tool's range. Here's what to look for:

---

### **AD 1: "The Excellent Example" (Expected Score: 85-95)**

**What to look for:**
- Authentic sustainability story (not just buzzwords)
- Diverse, empowered representation
- Culturally respectful
- Honest, transparent messaging

**Real Examples to Consider:**
- **Patagonia** - "Don't Buy This Jacket" campaign or "Worn Wear"
- **Dove** - Real Beauty campaign (but check for specific executions)
- **REI** - #OptOutside campaign
- **TOMS** - Giving campaigns (if specific about impact)

**What to look for in the image:**
- Multiple ages, races, body types shown naturally
- People in active/empowered roles
- Real people (not just models)
- Specific claims you can verify
- Minimal manipulation

**Copy example elements:**
"We repair what breaks. We help you find what you need. We recycle what's worn out." (Specific actions)

---

### **AD 2: "The Mixed Bag" (Expected Score: 60-75)**

**What to look for:**
- Good on some dimensions, weak on others
- Maybe diverse casting but stereotypical roles
- Or sustainability messaging but vague claims

**Real Examples to Consider:**
- **Nike** - Often diverse but may have stereotypical role assignments
- **H&M Conscious** - "Green" messaging but fast fashion contradiction
- **Most automotive ads** - Often diverse but weak on climate

**Issues you might flag:**
- Women only shown in yoga/lifestyle contexts
- "Eco-friendly" without specifics
- Diversity that feels like quota-filling
- Aspirational messaging that creates insecurity

---

### **AD 3: "The Problematic One" (Expected Score: 30-50)**

**What to look for:**
- Clear greenwashing
- Stereotypical representation
- Manipulative messaging
- Cultural insensitivity

**Types to look for:**
- **Weight loss ads** - Often body-shaming
- **"Green" oil/gas company ads** - Greenwashing
- **Luxury goods** - Often homogeneous, aspirational manipulation
- **Beauty products** - Often unrealistic standards

**Red flags you'd catch:**
- "All natural" for heavily processed products
- Only thin, white, young people
- Before/after that shame normal bodies
- Cultural elements as decoration
- Fear-based messaging

---

### **AD 4: "Tech/Modern Example" (Expected Score: 55-70)**

**What to look for:**
- Tech companies often do well on diversity visually
- But may lack substance or have ethical issues

**Real Examples:**
- **Apple** - Clean visuals, diverse, but environmental claims to check
- **Google** - Often diverse but question manipulation/data ethics
- **Microsoft** - Accessibility focus but verify claims

**Interesting to analyze:**
- Visual diversity vs. messaging substance
- Privacy/data ethics in communication
- Accessibility claims - real or performative?

---

### **AD 5: "Traditional/Aspirational" (Expected Score: 45-65)**

**What to look for:**
- Luxury brands, traditional companies
- Often homogeneous representation
- Status-based messaging

**Examples:**
- Luxury fashion (Chanel, Gucci - unless specific campaign)
- Premium automotive
- High-end spirits/watches
- Traditional banks/finance

**Why they score lower:**
- Narrow beauty standards
- Exclusionary messaging ("for the elite")
- Status anxiety messaging
- Limited diversity

---

## WHERE TO FIND SAMPLE ADS

### Quick Sources:

1. **Google Images**
   - Search: "[brand] advertisement 2024"
   - Filter by usage rights if needed
   - Screenshot and crop

2. **Brand Websites**
   - Most brands showcase campaigns on their site
   - Look for "Campaigns" or "News" sections

3. **Ad Libraries (mentioned in your doc)**
   - Facebook Ad Library: facebook.com/ads/library
   - Google Ad Transparency: adstransparency.google.com
   - TikTok Creative Center: ads.tiktok.com/business/creativecenter

4. **Award Sites**
   - Cannes Lions: canneslions.com (winners)
   - D&AD: dandad.org
   - One Show: oneclub.org
   - These have high-quality images

5. **Create Mock Ads**
   - Use Canva or Figma
   - Stock photos + generic copy
   - Useful for testing specific scenarios

---

## 4. SETUP & RUNNING INSTRUCTIONS

### Prerequisites
- Python 3.8 or higher
- Anthropic API key (get from console.anthropic.com)

### Installation

```bash
# 1. Navigate to the project folder
cd rai_demo

# 2. Install dependencies
pip install -r requirements.txt

# 3. Run the app
streamlit run app.py
```

### First Time Setup

1. The app will open in your browser automatically (usually localhost:8501)
2. Enter your Anthropic API key in the sidebar (left side)
3. Upload an ad image
4. Paste the ad copy/text
5. Click "Analyze Advertisement"

### Troubleshooting

**"Module not found" error:**
```bash
pip install --upgrade -r requirements.txt
```

**App won't start:**
```bash
# Check Python version
python --version  # Should be 3.8+

# Check Streamlit installation
streamlit --version
```

**API key error:**
- Make sure you copied the entire key
- Check it's valid at console.anthropic.com
- Try regenerating the key

---

## 5. DEMO TIPS

### Before the Demo

1. **Pre-load your sample ads**
   - Save images and copy to a folder
   - Test each one beforehand
   - Note which scores high/low

2. **Have API key ready**
   - Keep it in a secure note
   - Don't share screen while entering it

3. **Test your internet connection**
   - API calls need connectivity
   - Have a backup plan if offline

### During the Demo

**Opening (2 minutes):**
- Show the concept document first
- Explain the four dimensions quickly
- Set expectations: "This is a working prototype"

**Demo Flow (10 minutes):**

1. **Start with pre-analyzed results** (if you saved them)
   - Show the "excellent" ad result
   - Walk through each dimension
   - Highlight the radar chart
   - Show specific findings

2. **Show the contrast**
   - Show a problematic ad's results
   - Point out the differences
   - Show how it flags specific issues

3. **Live analysis** (if time and connection permits)
   - Upload a new ad
   - Let them watch it analyze
   - This proves it's real and working

**Key Points to Emphasize:**

- ✅ "This analyzes both text AND visuals together"
- ✅ "It provides specific, actionable feedback"
- ✅ "Scores are consistent - same ad, same score"
- ✅ "Can scale to thousands of ads for the Index"
- ✅ "Framework based on ESG and cultural standards"

**Questions You'll Get:**

Q: "How accurate is it?"
A: "It's as good as the framework we define. The AI is consistent - we're refining the evaluation criteria."

Q: "Can it handle video?"
A: "Not yet - that's Phase 4. Right now it's images and text, which covers static ads."

Q: "How fast can it process lots of ads?"
A: "This demo processes one at a time. The production version would use batch processing - potentially thousands per day."

Q: "What if an ad has no text?"
A: "The visual analysis still works - it evaluates representation, symbols, imagery."

Q: "Who decides what's 'responsible'?"
A: "Great question! The framework combines ESG standards, cultural research, and expert input. It's continuously refined."

### Common Demo Mistakes to Avoid

❌ Don't apologize excessively ("this is just a demo")
✅ Be confident: "This is a working prototype showing the core concept"

❌ Don't get stuck on one ad
✅ Show variety - different scores, different issues

❌ Don't let technical issues derail you
✅ Have screenshots of results as backup

❌ Don't promise features that don't exist yet
✅ Be clear about current vs. future capabilities

---

## QUICK START CHECKLIST

Before your demo:

- [ ] Python and packages installed
- [ ] Anthropic API key obtained and tested
- [ ] 3-5 sample ads collected (images + copy)
- [ ] Each sample ad tested in the tool
- [ ] Screenshots of results taken (as backup)
- [ ] Demo script/talking points prepared
- [ ] Technical backup plan (recorded video or screenshots)
- [ ] Laptop charged, internet connection tested

---

## NEXT STEPS AFTER DEMO

### If the demo goes well:

1. **Gather feedback on the framework**
   - Which dimensions matter most to stakeholders?
   - Are there indicators missing?
   - What industries to focus on first?

2. **Refine the scoring**
   - Test with more ads
   - Compare scores with human experts
   - Adjust weights and indicators

3. **Plan Phase 2**
   - Which brands to pilot with?
   - What data sources to use?
   - How to present the Index?

4. **Consider enhancements**
   - Competitor comparison view
   - Historical tracking (brand over time)
   - Industry benchmarks
   - Export reports as PDF

### Technical improvements:
- Add database to store results
- Batch processing for multiple ads
- API for integration with other tools
- User authentication for brand access

---

## APPENDIX: HOW THE AI ANALYSIS WORKS

The Claude API receives:
1. The ad image (as base64)
2. The ad copy text
3. A detailed prompt with the framework

Claude analyzes:
- Visual elements (diversity, symbols, imagery)
- Text elements (claims, tone, language)
- The combination (do visuals match messaging?)

It returns:
- Scores for each dimension
- Specific findings (what it saw)
- Overall assessment
- Recommendations

The scoring is based on:
- Pattern recognition (has it seen similar issues before?)
- Framework criteria (does it match indicators?)
- Contextual understanding (how do elements work together?)

This is NOT a black box - you can refine the framework and prompt to improve accuracy.

---

**Questions? Issues? Improvements?**
This is your demo - modify anything that doesn't work for your audience!

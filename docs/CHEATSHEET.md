# RAI Demo - Quick Reference Cheatsheet

## 📁 PROJECT STRUCTURE

```
rai_demo/
├── app.py                    # Main Streamlit app (run this!)
├── requirements.txt          # Python packages needed
├── README.md                 # Quick start guide
├── DEMO_GUIDE.md            # Complete guide (read this!)
├── SAMPLE_AD_COPY.md        # Example ad texts to test with
└── CHEATSHEET.md            # This file
```

## ⚡ ULTRA-QUICK START

```bash
# 1. Install
pip install -r requirements.txt

# 2. Run
streamlit run app.py

# 3. In browser:
# - Enter API key (sidebar)
# - Upload image
# - Paste ad copy
# - Click Analyze
```

## 🎯 THE 4 DIMENSIONS

| Dimension | What It Checks | Score Well When... |
|-----------|---------------|-------------------|
| Climate Responsibility | Sustainability claims | Specific, verified, transparent |
| Social Responsibility | Diversity, inclusion | Authentic representation, no stereotypes |
| Cultural Sensitivity | Respectful representation | Culturally informed, locally resonant |
| Ethical Communication | Honesty, transparency | Truthful claims, no manipulation |

## 🎨 STREAMLIT BASICS

```python
# Display text
st.title("Big Title")
st.write("Regular text")

# Get user input
name = st.text_input("Enter name")
uploaded = st.file_uploader("Upload file")

# Show things conditionally  
if st.button("Click me"):
    st.write("Button was clicked!")

# Layout
col1, col2 = st.columns(2)
with col1:
    st.write("Left side")
```

**Key concept:** The script re-runs from top to bottom every time user interacts!

## 📊 SAMPLE ADS TO TEST

### High Score (85-95):
- **Copy:** See #1 or #8 in SAMPLE_AD_COPY.md
- **Image:** Diverse people, authentic scenario, specific sustainability claims
- **Keywords:** "Repair", "certified", "transparent", diverse representation

### Medium Score (60-75):
- **Copy:** See #2 or #4 in SAMPLE_AD_COPY.md  
- **Image:** Some diversity, general claims
- **Keywords:** "Eco-friendly" (vague), "for everyone" (generic)

### Low Score (30-50):
- **Copy:** See #3, #5, or #6 in SAMPLE_AD_COPY.md
- **Image:** Homogeneous, stereotypical, before/after
- **Keywords:** "Dream body", greenwashing, stereotypes

## 🔍 WHAT THE AI LOOKS FOR

### Visual Analysis:
- Who's shown? (age, race, gender, body type, ability)
- What roles are they in? (active, passive, empowered, stereotypical)
- What symbols/imagery? (cultural, environmental, status)
- What's the setting? (aspirational, realistic, inclusive)

### Text Analysis:
- Claims specific or vague?
- Language inclusive or exclusive?
- Emotional manipulation present?
- Transparency or deception?

### Combined Analysis:
- Do visuals match messaging?
- Is diversity superficial or substantive?
- Are environmental claims backed by visual evidence?

## 🎤 DEMO SCRIPT (5 MIN VERSION)

**0:00-0:30** - Context
"Brands are judged not just on what they sell, but what values they convey. 
This tool measures responsibility across 4 dimensions."

**0:30-1:00** - Show Framework
"Climate, Social, Cultural, Ethical - each scored 0-100."

**1:00-3:00** - Show Results
"Here's an ad we analyzed..." [Show pre-loaded excellent example]
"And here's a problematic one..." [Show contrast]

**3:00-4:30** - Live Demo (optional)
"Let me analyze a new one right now..." [Upload and analyze]

**4:30-5:00** - Vision
"Scale this across thousands of ads → Annual Responsibility Index"

## 🐛 QUICK TROUBLESHOOTING

| Problem | Solution |
|---------|----------|
| Module not found | `pip install --upgrade -r requirements.txt` |
| API error | Check key is valid at console.anthropic.com |
| Slow analysis | Normal - API calls take 10-30s |
| Can't find uploaded file | Check file is .png or .jpg |
| Wrong score format | Check API returned valid JSON |

## 💡 CUSTOMIZATION POINTS

In `app.py`, you can modify:

```python
# Line ~24: Dimension weights
FRAMEWORK = {
    "Climate Responsibility": {
        "weight": 0.25,  # Change this!
        ...
    }
}

# Line ~180: Model choice
model="claude-sonnet-4-20250514"  # Try different models

# Line ~400: Chart colors
if score >= 80:
    color = "green"  # Customize thresholds
```

## 📈 SCORING RUBRIC

- **90-100**: Exemplary - Best in class
- **80-89**: Strong - Minor improvements possible
- **70-79**: Good - Some gaps to address
- **60-69**: Adequate - Notable concerns
- **50-59**: Concerning - Significant issues
- **40-49**: Problematic - Major red flags
- **0-39**: Failing - Multiple serious issues

## 🎯 DEMO SUCCESS FACTORS

✅ **DO:**
- Pre-test all sample ads
- Have screenshots as backup
- Show score diversity (not all 90s or all 40s)
- Emphasize "working prototype"
- Focus on the framework, not the tech

❌ **DON'T:**
- Apologize excessively
- Promise features that don't exist
- Let technical issues derail you
- Spend too long on one ad
- Get defensive about scores

## 🔐 API KEY

Get yours: https://console.anthropic.com/

Costs: ~$0.05-0.10 per ad analyzed (vision model)

For demo: $5-10 credit sufficient for 50-100 analyses

## 🚀 NEXT STEPS AFTER DEMO

1. **Immediate:** Gather feedback on framework
2. **Week 1:** Refine scoring based on feedback  
3. **Month 1:** Test with 100+ real ads
4. **Month 2:** Build batch processing
5. **Month 3:** Create first mini-Index report

## 📞 NEED HELP?

Check DEMO_GUIDE.md for:
- Detailed Streamlit tutorial
- Complete scoring framework
- Where to find ads
- Advanced troubleshooting

---

**Remember:** This is a prototype that proves the concept. 
It's about the framework and vision, not perfect technical execution.

Good luck with your demo! 🎉

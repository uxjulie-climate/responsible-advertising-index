# Analyze Advertisement

This command walks through how to analyze an advertisement using the RAI demo.

## Prerequisites

- Demo app running (`streamlit run app.py`)
- Google AI API key entered in sidebar
- Ad image file (PNG, JPG, or JPEG)
- Ad copy text prepared

## Analysis Steps

### 1. Prepare the Advertisement

**Collect these materials:**
- **Image**: The visual ad creative (screenshot, download, or photo)
- **Copy**: All text from the ad including:
  - Headline
  - Body copy
  - Tagline
  - Hashtags
  - Fine print (if relevant)
  - Any text visible in the image

### 2. Upload to Demo

1. Click "Upload ad image" in the app
2. Select your image file
3. Paste the ad copy into "Advertisement Copy/Text" field
4. Enter brand name (optional but recommended)
5. Click "🔍 Analyze Advertisement"

### 3. What the AI Analyzes

The Gemini 2.5 Flash model evaluates:

**Visual Elements:**
- People shown (diversity, roles, representation)
- Products and settings
- Colors and visual messaging
- Cultural symbols or imagery
- Body language and power dynamics

**Text Elements:**
- Environmental claims (specific vs. vague)
- Inclusive language
- Truthfulness and transparency
- Manipulative techniques
- Cultural references

**Combined Analysis:**
- Do visuals match messaging?
- Authenticity vs. tokenism
- Greenwashing indicators
- Stereotype patterns

### 4. Understanding Results

**Overall Score (0-100):**
- 80-100: Excellent - highly responsible
- 60-79: Good - mostly responsible with some areas for improvement
- 40-59: Mixed - significant concerns alongside positives
- 0-39: Problematic - major responsibility issues

**Dimension Scores:**
Each dimension (Climate, Social, Cultural, Ethical) is scored 0-100:
- Review the radar chart to see strength across dimensions
- Read specific findings for each dimension
- Note which areas score high vs. low

**Key Outputs:**
- **Strengths**: What the ad does well
- **Concerns**: Problematic elements or risks
- **Recommendations**: How to improve

### 5. Export Results

**PDF Report (Single Ad):**
- Click "📄 Download PDF Report"
- Includes scores, findings, and recommendations
- Good for sharing with stakeholders

**JSON Data:**
- Click "📊 Download JSON Data"
- Structured data for analysis/archival

**Comparison (Multiple Ads):**
- Analyze 2+ ads
- Go to "Compare Ads" tab
- Select ads to compare
- Export comparison PDF or Excel

## Example: Analyzing a Sustainability Ad

**Sample Ad:**
Brand: EcoThreads
Image: Diverse group repairing clothes together
Copy: "Repair Revolution - Every garment comes with lifetime repair guarantee..."

**Expected Scores:**
- Climate: 90-95 (specific sustainability claims, promotes repair)
- Social: 85-90 (diverse representation, inclusive)
- Cultural: 80-85 (community-focused, respectful)
- Ethical: 90-95 (transparent, honest claims)
- **Overall: 85-92**

**Key Findings Gemini Would Identify:**
✓ Specific, verifiable claims (GOTS, Fair Trade certified)
✓ Promotes circular economy (repair over consumption)
✓ Diverse, authentic representation
✓ Transparent about practices
✓ No manipulative tactics

## Tips for Better Analysis

**Do:**
- Include ALL text from the ad (even fine print)
- Use high-quality images (clear, readable)
- Provide context if culturally specific
- Analyze multiple ads for comparison

**Don't:**
- Omit important disclaimers
- Use blurry or cropped images
- Expect identical scores on re-analysis (AI has some variance)
- Upload ads with sensitive data without permission

## Understanding the Scoring Framework

Each dimension has specific indicators (see app.py:148-185):

**Climate Responsibility (25% weight):**
- Sustainability messaging authenticity
- Absence of greenwashing
- Climate-positive behaviors
- Transparency

**Social Responsibility (25% weight):**
- Diversity across multiple dimensions
- Avoidance of stereotypes
- Empowerment vs. tokenism
- Inclusive language

**Cultural Sensitivity (25% weight):**
- Respectful use of cultural elements
- Local awareness
- Geopolitical sensitivity
- Global/local balance

**Ethical Communication (25% weight):**
- Transparency and disclosures
- Avoidance of manipulation
- Truthful claims
- Informed choice vs. exploitation

## Interpreting Findings

**Green Flags (raise scores):**
- Specific certifications mentioned
- Diverse casting in empowered roles
- Transparent limitations acknowledged
- Educational rather than manipulative

**Red Flags (lower scores):**
- Vague claims ("eco-friendly" without proof)
- Homogeneous or stereotypical representation
- Cultural appropriation
- Body-shaming or fear-based messaging
- Unsubstantiated "miracle" claims

## Next Steps After Analysis

1. **Review findings**: Read all dimension findings carefully
2. **Export results**: Save PDF for records
3. **Compare**: Analyze similar ads to see patterns
4. **Act**: Use recommendations to improve future ads

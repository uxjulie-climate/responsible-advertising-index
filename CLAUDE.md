# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

The Responsible Advertising Index (RAI) is an AI-powered assessment tool that evaluates advertising content across four responsibility dimensions:
1. **Climate Responsibility**: Sustainability messaging and greenwashing detection
2. **Social Responsibility**: Diversity, stereotyping, and inclusivity analysis
3. **Cultural Sensitivity**: Respectful cultural representation and local awareness
4. **Ethical Communication**: Transparency, truthfulness, and non-manipulation assessment

Each advertisement receives dimension scores (0-100) that combine into an overall letter grade (A+, A, B+, etc.).

## Current Development Phase

**Phase 1: Telekom Demo (1-2 weeks)** - Priority focus
- Simple web interface for uploading 3 ads and displaying scores
- Basic scoring for static images + text using Claude Sonnet 4.5 / GPT-4V
- Manual scoring validation against lookup tables
- Dashboard showing ad thumbnails, score breakdown, overall grade, and 2-3 key insights

Future phases include automated scraping (Phase 2) and full index launch with public API (Phase 3).

## Current Tech Stack (Gemini Demo)

**The working demo uses:**
- **AI/ML**: Google Gemini 2.5 Flash (multimodal vision API)
- **Backend**: Python with Streamlit (single-file web app)
- **Frontend**: Streamlit (built-in UI components)
- **Storage**: Session state (in-memory for demo)
- **Export**: ReportLab (PDF), Pandas/OpenPyxl (Excel)
- **Visualization**: Plotly (radar charts, gauges)

**Future production stack:**
- **AI/ML**: Vertex AI (Gemini) using Google Cloud credits, fallback to Claude/GPT-4V
- **Backend**: Python (Flask/FastAPI) for API
- **Frontend**: React or Vue.js for dashboard
- **Database**: PostgreSQL (scores), MongoDB (ad metadata)
- **Storage**: Cloud Storage (GCS/S3) for ad images/videos
- **Ad Sources**: Meta Ad Library API, Google Ads Transparency, TikTok Ad Library

## Project Structure

**Current Demo Structure (Streamlit):**
```
responsible-advertising-index/
├── app.py                    # Main Streamlit application (single file, ~1250 lines)
├── requirements.txt          # Python dependencies
├── CLAUDE.md                 # This file
├── .claude/
│   └── commands/
│       ├── demo-setup.md     # Command to set up demo
│       └── analyze-ad.md     # Command to analyze individual ads
└── Reference materials from /Users/julieschiller/Downloads/rai_demo_gemini/:
    ├── SAMPLE_AD_COPY.md     # Example ad copy for testing
    ├── DEMO_GUIDE.md         # Complete demo preparation guide
    ├── CHEATSHEET.md         # Quick reference for demo day
    ├── GEMINI_VS_CLAUDE.md   # Why Gemini was chosen
    └── VERTEX_AI_SETUP.md    # How to use Google Cloud credits
```

**Future Production Structure:**
```
rai/
├── backend/
│   ├── api/              # API endpoints (Flask/FastAPI)
│   ├── models/           # AI model integrations (Gemini, Claude, GPT-4V)
│   ├── scoring/          # Scoring algorithms for each dimension
│   ├── scrapers/         # Ad library scrapers (Phase 2+)
│   └── utils/            # Helper functions
├── frontend/
│   ├── components/       # React/Vue components
│   ├── pages/            # Dashboard views
│   └── utils/            # Frontend helpers
├── data/
│   ├── ads/              # Downloaded ad samples
│   └── lookup_tables/    # Reference tables for validation
└── tests/
```

## Development Commands

**Current Demo (Streamlit):**
```bash
# Setup (from project root)
pip3 install -r requirements.txt

# Run development server
streamlit run app.py
# Opens browser automatically at http://localhost:8501

# Get free Google AI API key
# https://makersuite.google.com/app/apikey
```

**Future Production Backend** (when migrating to Flask/FastAPI):
```bash
# Setup
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt

# Run development server
uvicorn backend.api.main:app --reload

# Run tests
pytest tests/

# Linting
flake8 backend/
black backend/
```

**Future Production Frontend** (when building React dashboard):
```bash
# Setup
cd frontend
npm install

# Run development server
npm run dev

# Run tests
npm test

# Build for production
npm run build
```

## Architecture Considerations

### Current Demo Implementation (Streamlit + Gemini)

The working demo (`app.py`) implements a simplified scoring pipeline:
1. **Input**: User uploads image + provides ad copy text
2. **Preprocessing**: Image loaded via PIL, text passed as-is
3. **AI Analysis**: Single API call to Gemini 2.5 Flash with:
   - Multimodal prompt (image + text combined)
   - Framework definition (4 dimensions with indicators)
   - Structured JSON output request
4. **Response Parsing**: Extract scores, findings, summary from JSON
5. **Visualization**: Plotly radar charts, gauge charts
6. **Export**: PDF generation via ReportLab, Excel via Pandas/OpenPyxl
7. **History**: Session state tracking for multi-ad comparison

**Key function:** `analyze_ad(image_data, ad_copy, api_key)` at app.py:250
- Configures Gemini API client
- Creates scoring prompt via `create_analysis_prompt()`
- Sends multimodal request: `model.generate_content([prompt, img])`
- Parses JSON response (handles markdown code blocks)
- Returns structured dict with scores and findings

### Future Production Pipeline
Each ad will go through a multi-stage analysis pipeline:
1. **Preprocessing**: Extract text, images, frames from video
2. **AI Analysis**: Send to multimodal AI (Gemini Vertex AI primary) with dimension-specific prompts
3. **Claim Verification**: Cross-reference sustainability/factual claims against lookup tables and external databases
4. **Bias Detection**: Check for stereotypes, cultural appropriation, manipulative patterns
5. **Scoring**: Calculate 0-100 scores per dimension based on AI findings + validation rules
6. **Aggregation**: Weighted average → overall score → letter grade
7. **Insight Generation**: Extract 2-3 key findings per ad for dashboard display

### Critical Design Principles

**Explainability First**: All AI decisions must be logged with rationale. The scoring logic should be traceable and auditable. Use comprehensive logging in `backend/scoring/` to capture:
- Which AI model made the assessment
- Specific criteria that affected the score
- Any lookup table or external validation used

**Multilingual Support**: Handle Hungarian and English at minimum. Design prompts and interfaces to be language-agnostic where possible. Store language metadata with each ad.

**Bias Mitigation**: AI models may perpetuate biases. Always validate AI assessments against:
- Miklos's reference lookup tables in `data/lookup_tables/`
- Established ESG frameworks (GRI, SASB)
- Cultural sensitivity databases (UNESCO)

**API Resilience**: External APIs (Anthropic, OpenAI, ad libraries) can fail or rate-limit. Implement:
- Async operations with proper timeout handling
- Retry logic with exponential backoff
- Fallback models (e.g., if Claude fails, try GPT-4V)
- Queue system for batch processing

### Greenwashing Detection Approach

This is the most technically challenging dimension. Cannot rely on AI alone:
1. Extract sustainability claims from ad content (AI)
2. Cross-reference against company's actual ESG reports/data (external APIs)
3. Check against greenwashing patterns (lookup tables)
4. Flag vague terms ("eco-friendly", "natural") without substantiation
5. Verify certifications (B-Corp, Carbon Neutral, etc.) are legitimate

Maintain a greenwashing pattern database in `data/lookup_tables/greenwashing_patterns.json`.

### Cultural Sensitivity Implementation

Requires regional context awareness:
- Maintain regional sensitivity guidelines per market (Hungarian, US, EU, etc.)
- Check for cultural appropriation patterns (indigenous symbols, religious imagery)
- Validate local relevance (Hungarian holidays, traditions for Telekom demo)
- Flag potentially offensive imagery based on local norms

Store regional rules in `data/lookup_tables/cultural_guidelines/`.

## Integration Points

**AI Model APIs**:
- Google Gemini (current): Use `google-generativeai` Python SDK, requires `GOOGLE_API_KEY` from https://makersuite.google.com/app/apikey
  - Demo uses: `gemini-2.5-flash` model
  - Production path: Migrate to Vertex AI to use Google Cloud startup credits
- Anthropic Claude (future fallback): Use `anthropic` Python SDK, requires `ANTHROPIC_API_KEY`
- OpenAI GPT-4V (future fallback): Use `openai` Python SDK, requires `OPENAI_API_KEY`

**Ad Library APIs** (Phase 2+):
- Meta Ad Library: Requires Facebook app credentials
- Google Ads Transparency: Public API, rate-limited
- TikTok Ad Library: Requires TikTok developer account

**Validation Data Sources**:
- ESG databases for greenwashing checks
- Fact-checking APIs for claim verification
- UNESCO cultural databases for sensitivity checks

All API keys should be stored in `.env` (never committed) and loaded via `python-dotenv` or similar.

## Testing Strategy

**Unit Tests**: Core scoring logic in `backend/scoring/` must have >80% coverage
- Test score calculation for each dimension
- Test edge cases (empty text, corrupted images, multiple languages)
- Mock AI responses to test scoring consistency

**Integration Tests**: Test AI model integration
- Real API calls to Claude/GPT-4V (use test ads)
- Validate response parsing and error handling
- Test fallback behavior when primary model fails

**End-to-End Tests**: Frontend → Backend → AI → Dashboard
- Upload test ad → verify correct score display
- Test with 3 sample Telekom ads for demo validation

## Demo-Specific Requirements (Telekom)

**The current Streamlit demo already provides:**
- ✅ File upload for ad images (PNG, JPG, JPEG)
- ✅ Text input for ad copy
- ✅ Multimodal analysis via Gemini 2.5 Flash
- ✅ Radar chart visualization for 4 dimensions
- ✅ Overall score with color-coded gauge
- ✅ Detailed findings per dimension
- ✅ PDF report export (single ad)
- ✅ Excel/PDF comparison export (multiple ads)
- ✅ Analysis history tracking
- ✅ Example ads built-in (sustainable fashion, weight loss, EV)

**For Telekom demo:**
- **Input**: Upload 3 Telekom advertisements (supports Hungarian + English text via Gemini's multilingual capabilities)
- **Performance**: Analysis takes 10-30 seconds per ad (API-dependent)
- **Validation**: Test with sample ads first, verify scores make sense before demo
- **Backup Plan**: Take screenshots of successful analyses in case of internet/API issues during demo

**Demo Preparation Steps:**
1. Get free Google AI API key: https://makersuite.google.com/app/apikey
2. Test with 3 sample ads (different score ranges) - use examples in `SAMPLE_AD_COPY.md`
3. Screenshot results as backup
4. Prepare 3 Telekom ads (images + copy)
5. Pre-run Telekom ads to verify results before demo
6. Review CHEATSHEET.md for talking points

## Key Technical Challenges

1. **Video Processing** (Phase 2): Extracting representative frames, handling large files, compute costs
2. **Claim Verification**: Requires external data sources that may not have APIs
3. **Cultural Context**: No single database covers all regional sensitivities - may require manual curation
4. **AI Consistency**: Same ad may get different scores on repeated analysis - need confidence intervals
5. **Rate Limits**: Ad library APIs restrict request frequency - implement queueing and caching

## Code Quality Standards

- **Type Safety**: Use Python type hints or TypeScript
- **Async First**: All external API calls should be async (use `asyncio` in Python)
- **Error Handling**: Never fail silently - log errors and provide fallback scores if AI unavailable
- **Environment Config**: Use `.env` for all secrets and configuration
- **Logging**: Use structured logging (JSON format) with levels (DEBUG, INFO, WARNING, ERROR)
- **Comments**: Explain *why* scoring decisions are made, especially for weighted calculations

## External Standards & References

- **Greenwashing Guidelines**: ASA (UK Advertising Standards Authority), FTC Green Guides (US)
- **ESG Frameworks**: GRI (Global Reporting Initiative), SASB (Sustainability Accounting Standards Board)
- **Cultural Resources**: UNESCO cultural databases, regional advertising standards bodies
- **Ad Libraries**: Meta Ad Library (facebook.com/ads/library), Google Ads Transparency Center, TikTok Ad Library

## Development Workflow Notes

- **Branch Strategy**: Use feature branches for each dimension implementation
- **Commit Messages**: Reference dimension being worked on (e.g., "feat: add climate greenwashing detection")
- **Documentation**: Update this file as architecture decisions are made
- **Demo Preparation**: Test with actual Telekom ads 48 hours before demo to allow refinement time

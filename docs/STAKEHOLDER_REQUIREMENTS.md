# Stakeholder Requirements & Implementation Plan

**Date:** 2025-01-13
**Context:** Post-demo feedback and feature requests

---

## Overview

Four key requirements from stakeholder demo:

1. **Ad Submission Form** - Allow external parties to submit ads for analysis
2. **Storage & Leaderboard System** - Track advertisers over time, create rankings
3. **Development & Operations Costs** - Calculate total investment required
4. **Sarcasm Handling** - Test with Oatly "Wow No Cow!" ad

---

## 1. Ad Submission Form

### Requirements

**Purpose:** Allow stakeholders, partners, or the public to submit ads for RAI analysis without needing direct access to the tool.

**User Flow:**
1. User fills out web form
2. Uploads ad image/video + provides metadata
3. Submits to queue
4. Receives analysis results via email or portal
5. Optional: Public or private results

### Implementation Options

#### Option A: Google Forms + Manual Processing (Quick Start - €0)
**Timeline:** 1-2 days
**Cost:** Free

**Setup:**
- Google Form collecting:
  - Advertiser name
  - Brand/product
  - Ad type (image/video)
  - File upload
  - Contact email
  - Language (EN/HU)
  - Purpose (internal/research/external)
- Responses go to Google Sheets
- Manual download and processing
- Email results back

**Pros:**
- Zero cost
- Immediate deployment
- No infrastructure needed
- Easy to modify

**Cons:**
- Manual processing required
- No automation
- Not scalable
- Poor UX

#### Option B: Streamlit Public Form (Low Cost - €10-30/month)
**Timeline:** 3-5 days
**Cost:** €10-30/month (Streamlit Cloud Community or hosting)

**Setup:**
- New Streamlit app: `submit_ad.py`
- Form fields same as Option A
- Auto-saves to Cloud Storage
- Triggers analysis pipeline
- Email notification with results
- Simple queue system

**Pros:**
- Automated end-to-end
- Professional appearance
- Integrated with existing stack
- Moderate cost

**Cons:**
- Requires hosting
- API costs for analysis
- Need email service

#### Option C: Full Web Portal (Production - €200-500/month)
**Timeline:** 3-4 weeks
**Cost:** €200-500/month

**Setup:**
- React/Next.js frontend
- FastAPI backend
- PostgreSQL database
- Authentication (OAuth)
- User dashboard
- Analysis history
- Results download
- Admin panel

**Pros:**
- Professional product
- Scalable architecture
- User accounts
- Full analytics
- White-label ready

**Cons:**
- Significant development time
- Higher cost
- Maintenance burden
- Infrastructure complexity

### Recommendation

**Start with Option B (Streamlit Public Form)** because:
- Balances automation with cost
- Integrates seamlessly with existing codebase
- Can iterate quickly based on feedback
- Easy upgrade path to Option C if needed

**Implementation Plan:**
1. Create `submit_ad.py` - public submission form
2. Set up Cloud Storage bucket for submissions
3. Create analysis queue (simple JSON file or Cloud Tasks)
4. Implement email notification (SendGrid free tier)
5. Add admin dashboard to review queue

---

## 2. Storage System & Leaderboard

### Requirements

**Purpose:**
- Store all analyzed ads with metadata
- Track advertiser performance over time
- Create rankings and benchmarks
- Enable year-over-year comparison
- Generate industry insights

### Database Schema

```sql
-- Advertisers Table
CREATE TABLE advertisers (
    id UUID PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    industry VARCHAR(100),
    country VARCHAR(2),
    created_at TIMESTAMP,
    updated_at TIMESTAMP
);

-- Ads Table
CREATE TABLE ads (
    id UUID PRIMARY KEY,
    advertiser_id UUID REFERENCES advertisers(id),
    brand VARCHAR(255),
    product VARCHAR(255),
    ad_type ENUM('image', 'video'),
    language VARCHAR(2),
    analyzed_at TIMESTAMP,

    -- File storage
    file_url TEXT,
    file_size_mb DECIMAL(10,2),
    duration_seconds INT, -- null for images

    -- Metadata
    ad_copy TEXT,
    detected_language VARCHAR(2),

    -- Scores
    overall_score DECIMAL(5,2),
    climate_score DECIMAL(5,2),
    social_score DECIMAL(5,2),
    cultural_score DECIMAL(5,2),
    ethical_score DECIMAL(5,2),

    -- Analysis results (JSON)
    full_analysis JSONB,

    -- Submission info
    submitted_by VARCHAR(255),
    submission_source ENUM('internal', 'form', 'api', 'demo'),

    -- Visibility
    is_public BOOLEAN DEFAULT FALSE,

    created_at TIMESTAMP,
    updated_at TIMESTAMP
);

-- Findings Table (for detailed querying)
CREATE TABLE findings (
    id UUID PRIMARY KEY,
    ad_id UUID REFERENCES ads(id),
    dimension VARCHAR(50),
    finding_type ENUM('strength', 'concern', 'recommendation'),
    finding_text TEXT,
    language VARCHAR(2),
    created_at TIMESTAMP
);

-- Leaderboard Views
CREATE VIEW advertiser_leaderboard AS
SELECT
    a.id,
    a.name,
    a.industry,
    COUNT(ads.id) as total_ads,
    AVG(ads.overall_score) as avg_score,
    AVG(ads.climate_score) as avg_climate,
    AVG(ads.social_score) as avg_social,
    AVG(ads.cultural_score) as avg_cultural,
    AVG(ads.ethical_score) as avg_ethical,
    MAX(ads.analyzed_at) as latest_analysis
FROM advertisers a
LEFT JOIN ads ON ads.advertiser_id = a.id
GROUP BY a.id, a.name, a.industry;

CREATE VIEW best_ads_by_dimension AS
SELECT
    dimension,
    ad_id,
    brand,
    product,
    score,
    analyzed_at,
    RANK() OVER (PARTITION BY dimension ORDER BY score DESC) as rank
FROM (
    SELECT 'climate' as dimension, id as ad_id, brand, product, climate_score as score, analyzed_at FROM ads
    UNION ALL
    SELECT 'social', id, brand, product, social_score, analyzed_at FROM ads
    UNION ALL
    SELECT 'cultural', id, brand, product, cultural_score, analyzed_at FROM ads
    UNION ALL
    SELECT 'ethical', id, brand, product, ethical_score, analyzed_at FROM ads
) sub;
```

### Implementation Options

#### Option A: SQLite + Local Storage (Development - €0)
**Timeline:** 2-3 days
**Cost:** Free

**Setup:**
- SQLite database file
- Python SQLAlchemy ORM
- Files stored locally
- Simple query interface

**Pros:**
- Zero cost
- Easy setup
- Good for testing
- Portable

**Cons:**
- Not scalable
- Single machine only
- No concurrent access
- No cloud benefits

#### Option B: Cloud SQL + Cloud Storage (Production - €50-150/month)
**Timeline:** 1 week
**Cost:**
- Cloud SQL PostgreSQL: €30-100/month
- Cloud Storage: €10-30/month
- Backups: €10-20/month

**Setup:**
- PostgreSQL on Cloud SQL
- Ad files in Cloud Storage
- Prisma/SQLAlchemy ORM
- Automated backups
- Read replicas for analytics

**Pros:**
- Scalable
- Reliable
- Professional
- Multi-user support
- Geographic redundancy

**Cons:**
- Monthly cost
- Some complexity
- Requires cloud management

#### Option C: Supabase (Quick Cloud - €25-100/month)
**Timeline:** 3-5 days
**Cost:** €25-100/month

**Setup:**
- Supabase (PostgreSQL + storage + auth)
- Instant REST API
- Built-in auth
- Real-time subscriptions
- Dashboard included

**Pros:**
- Fast setup
- All-in-one solution
- Great developer experience
- Built-in features
- Free tier available

**Cons:**
- Vendor lock-in
- Less control
- Custom queries harder

### Recommendation

**Start with Option C (Supabase)** because:
- Fastest time to value
- Includes auth, storage, database
- Free tier for development/testing
- Easy upgrade to paid plans
- Built-in admin dashboard

### Leaderboard Features

**Public Leaderboard (if appropriate):**
1. **Top Advertisers Overall** - Ranked by average score across all ads
2. **Best Ads by Dimension** - Top 10 in Climate, Social, Cultural, Ethical
3. **Most Improved** - Year-over-year change
4. **Industry Leaders** - Best in Fashion, Tech, Food, etc.
5. **Rising Stars** - New entrants with high scores

**Private Dashboard (for advertiser):**
1. **Your Performance** - Average scores, trend over time
2. **Your Ranking** - Position vs. industry peers
3. **Best Practices** - Top-performing ads to learn from
4. **Improvement Areas** - Dimensions needing work
5. **Historical Comparison** - This year vs. last year

**Filters:**
- Time period (last 30 days, quarter, year)
- Industry
- Country/language
- Ad type (image/video)
- Minimum sample size (e.g., advertisers with 5+ ads)

---

## 3. Development & Operations Costs

### Current Status (Demo Phase)

**Invested So Far:**
- Development time: ~40 hours × €50-100/hr = **€2,000-4,000**
- API costs (Gemini): ~€5/month for testing
- Hosting: €0 (local development)
- **Total invested: €2,000-4,000**

### Future Costs Breakdown

#### A. Development Costs (One-Time)

| Feature | Timeline | Cost Estimate |
|---------|----------|---------------|
| **Core RAI (Done)** | 2 weeks | €2,000-4,000 |
| **Submission Form (Option B)** | 3-5 days | €1,000-2,000 |
| **Database & Leaderboard** | 1 week | €2,000-3,000 |
| **User Authentication** | 3-5 days | €1,000-2,000 |
| **Admin Dashboard** | 1 week | €2,000-3,000 |
| **Email Notifications** | 2-3 days | €500-1,000 |
| **API Development** | 1 week | €2,000-3,000 |
| **Testing & QA** | 1 week | €1,500-2,500 |
| **Documentation** | 3-5 days | €1,000-1,500 |
| **Validation Studies** | 6 months | €65,000-110,000 |
| **TOTAL DEVELOPMENT** | **3-4 months** | **€78,000-131,000** |

**Without validation studies:** €13,000-21,000

#### B. Operations Costs (Monthly)

| Service | Usage Tier | Monthly Cost |
|---------|-----------|--------------|
| **Gemini API** | | |
| - Image analysis | 1000 images/month | €10-20 |
| - Video analysis | 100 videos/month | €30-50 |
| **Cloud Storage** | | |
| - Video storage (temp) | 1 TB turnover | €20-30 |
| - Ad archive | 100 GB | €5-10 |
| **Database (Supabase/Cloud SQL)** | | |
| - Small (< 10K ads) | Low usage | €25-50 |
| - Medium (10K-100K ads) | Moderate | €100-200 |
| - Large (> 100K ads) | High usage | €300-500 |
| **Hosting** | | |
| - Streamlit Community | Basic | €0-10 |
| - Cloud Run / App Engine | Low traffic | €20-50 |
| - Dedicated server | High traffic | €100-200 |
| **Email Service (SendGrid)** | | |
| - Up to 40K emails/month | Free tier | €0 |
| - 40K-100K emails/month | Pro tier | €15-20 |
| **Monitoring & Logging** | | €10-20 |
| **Backups** | | €10-20 |
| **Domain & SSL** | | €5-10 |
| **TOTAL OPERATIONS** | **Low scale** | **€125-210/month** |
| | **Medium scale** | **€250-450/month** |
| | **High scale** | **€500-800/month** |

#### C. Cost Per Analysis

**Image Analysis:**
- API cost: ~€0.01-0.02 per image
- Storage: ~€0.001
- Processing: ~€0.005
- **Total: ~€0.02 per image**

**Video Analysis:**
- API cost: ~€0.30-0.60 per minute
- Storage: ~€0.01-0.02
- Processing: ~€0.01
- **Total: ~€0.35-0.65 per minute of video**

**Example: 1000 image ads + 100 video ads (avg 30 sec each):**
- Images: 1000 × €0.02 = €20
- Videos: 100 × 0.5 min × €0.50 = €25
- **Monthly total: €45 in variable costs**

#### D. Revenue Models (to offset costs)

**Option 1: Freemium**
- Free: 5 analyses/month
- Pro (€49/month): 50 analyses/month
- Business (€199/month): Unlimited + leaderboard access
- Enterprise (€999/month): Custom features + API access

**Option 2: Pay-Per-Analysis**
- €2-5 per image analysis
- €10-20 per video analysis
- Bulk discounts available

**Option 3: Subscription Tiers**
- Internal Use (Telekom): €500/month flat fee
- Partner Access: €1,000/month (includes leaderboard)
- Public Service: Ad-supported or grant-funded

**Option 4: Certification Program**
- Advertisers pay €500-2,000 for "RAI Verified" badge
- Requires minimum score + validation
- Annual renewal

### Cost Summary

**Year 1 Investment:**
- Development (without validation): €13,000-21,000
- Operations (12 months @ medium scale): €3,000-5,400
- Validation studies: €65,000-110,000
- **Total Year 1: €81,000-136,400**

**Year 2+ (Steady State):**
- Maintenance (10 hrs/month × €75): €9,000/year
- Operations: €3,000-5,400/year
- Incremental features: €5,000-10,000/year
- **Total Year 2+: €17,000-24,400/year**

**ROI Scenarios:**
- **Internal tool:** Improves Telekom ad quality, hard to quantify but high value
- **Partner service:** 20 partners × €1,000/month = €240K/year revenue
- **Public platform:** 500 users × €49/month = €294K/year revenue
- **Certification:** 100 brands × €1,000/year = €100K/year revenue

---

## 4. Sarcasm & Irony Handling

### The Challenge

**Example:** Oatly "Wow No Cow!" ad (https://www.youtube.com/watch?v=j4IFNKYmLa8)
- Known for ironic, self-aware advertising
- Uses humor and sarcasm to critique traditional dairy ads
- Tests whether RAI understands tone vs. literal meaning

### How RAI Currently Handles Tone

**Gemini 2.5 Flash Capabilities:**
- ✅ Generally good at detecting tone and intent
- ✅ Can identify sarcasm when context is clear
- ⚠️ May struggle with subtle or cultural-specific irony
- ❌ No explicit "sarcasm detection" in current prompt

**Current Prompt Approach:**
- Analyzes "overall message and intent"
- Looks at context clues
- But doesn't explicitly check for irony/sarcasm

### Testing Plan

**Let me test the Oatly ad once you upload it:**

1. **Manual Upload Method:**
   - Screen record the ad: Cmd+Shift+5 on Mac
   - Save as .mp4
   - Upload via Video Analysis tab
   - Analyze with RAI

2. **What to Look For:**
   - Does RAI recognize the ironic tone?
   - Does it understand Oatly is mocking traditional dairy ads?
   - Does it correctly assess the responsible messaging underneath the humor?
   - Or does it take the sarcasm literally?

### Expected Results

**Best Case (RAI understands sarcasm):**
- Recognizes self-aware, ironic tone
- Identifies that humor is used to critique unsustainable practices
- Scores positively for ethical communication (transparency, honesty)
- Notes "uses satire to challenge conventional advertising"

**Worst Case (RAI misses sarcasm):**
- Takes ironic statements literally
- May flag satirical exaggerations as misleading claims
- Misunderstands the intent
- Lower ethical score due to misinterpretation

### Improving Sarcasm Detection

**Prompt Enhancement:**

Add to the analysis prompt:
```
Before analyzing, consider:
- Is this ad using humor, satire, irony, or sarcasm?
- What is the INTENDED message vs. literal words?
- Is the brand being self-aware or self-critical?
- Does irony serve a responsible purpose (e.g., criticizing greenwashing)?

If sarcasm/irony is detected:
- Analyze the UNDERLYING message, not just surface words
- Note that humor is being used as a communication strategy
- Assess whether the irony serves a responsible purpose
```

**Additional Context:**

Add field to submission form:
- "Tone of ad" dropdown: Serious / Humorous / Satirical / Ironic
- "Ad intent" field: Brief description of what the ad is trying to achieve

This helps RAI interpret correctly.

### Testing Oatly Ad - Action Needed

**To test sarcasm handling:**

1. **Download the Oatly ad:**
   ```bash
   # Screen record from browser (Cmd+Shift+5)
   # Or try VLC: Media > Open Network Stream > paste URL > Convert/Save
   ```

2. **Analyze via RAI:**
   - Upload video file
   - Add ad copy if any text overlay
   - Run analysis

3. **Evaluate results:**
   - Did it catch the sarcasm?
   - Is the score fair given the ironic tone?
   - Are findings relevant?

4. **Share results** - I'll review and suggest prompt improvements if needed

---

## Implementation Priorities

### Phase 1: Quick Wins (1-2 weeks)
1. ✅ Create cost breakdown document (done above)
2. ⏳ Test Oatly ad for sarcasm handling (needs manual upload)
3. 🔄 Implement Streamlit submission form
4. 🔄 Set up Supabase database
5. 🔄 Add basic ad storage

### Phase 2: Core Features (2-4 weeks)
1. Build leaderboard UI
2. Add user authentication
3. Implement email notifications
4. Create admin dashboard
5. Enhance sarcasm detection in prompts

### Phase 3: Scale & Polish (4-8 weeks)
1. API development
2. Advanced analytics
3. Public leaderboard (if desired)
4. White-label branding
5. Performance optimization

---

## Next Steps

**Immediate Actions:**
1. **Test sarcasm handling:**
   - Screen record Oatly ad
   - Upload to RAI
   - Share results for evaluation

2. **Decide on architecture:**
   - Submission form: Option A, B, or C?
   - Database: SQLite, Cloud SQL, or Supabase?
   - Budget approval?

3. **Define use case:**
   - Internal Telekom tool?
   - Partner service?
   - Public platform?
   - This determines features and costs

**Questions for Stakeholder:**
1. What's the primary use case? (Internal / Partner / Public)
2. What's the budget range? (€20K? €50K? €100K+?)
3. Timeline expectations? (MVP in 1 month? Full platform in 3 months?)
4. Who is the target user? (Telekom marketers? Agencies? Advertisers?)
5. Should leaderboard be public or private?
6. Revenue model required or cost center?

---

## Cost Summary Table

| Scenario | Development | Year 1 Ops | Year 1 Total | Ongoing/Year |
|----------|-------------|------------|--------------|--------------|
| **Minimum (Internal Tool)** | €13K | €1.5K | €14.5K | €10K |
| **Standard (Partner Service)** | €20K | €3K | €23K | €18K |
| **Full Platform** | €78K | €5K | €83K | €24K |
| **With Validation** | €131K | €5K | €136K | €24K |

*Note: Validation studies (€65-110K) are for establishing scientific credibility, not operational requirements.*

---

**Document Status:** Draft for stakeholder review
**Next Update:** After Oatly ad testing and architecture decisions

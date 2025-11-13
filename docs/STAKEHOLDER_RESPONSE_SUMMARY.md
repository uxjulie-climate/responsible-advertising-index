# Stakeholder Questions - Response Summary

**Date:** 2025-01-13
**Context:** Post-demo follow-up
**Stakeholder Request:** 4 key questions about RAI capabilities and costs

---

## Quick Answers

### 1. Can we make a form for people to send us ads? ✅

**YES** - Three options created:

| Option | Timeline | Cost | Best For |
|--------|----------|------|----------|
| **Google Forms** | 1-2 days | Free | Internal testing |
| **Streamlit Form** ⭐ | 3-5 days | €10-30/month | Partner service |
| **Full Web Portal** | 3-4 weeks | €200-500/month | Public platform |

**Recommendation:** Start with **Streamlit Form** (Option B)
- Automated end-to-end
- Professional appearance
- Low cost, integrated with current stack
- **Prototype already built** → `submit_ad.py`

**Demo the submission form:**
```bash
streamlit run submit_ad.py
```

---

### 2. Can we create a leaderboard for advertisers? ✅

**YES** - Database schema and architecture designed:

**Features Available:**
- 🏆 **Top Advertisers** - Ranked by average score
- 📊 **Best Ads by Dimension** - Top performers in Climate, Social, Cultural, Ethical
- 📈 **Most Improved** - Track progress over time
- 🏭 **Industry Leaders** - Best in Fashion, Tech, Food, etc.
- 🔒 **Private Dashboards** - Individual advertiser performance tracking

**Technology Options:**

| Option | Cost | Timeline | Best For |
|--------|------|----------|----------|
| SQLite | Free | 2-3 days | Development/testing |
| **Supabase** ⭐ | €25-100/month | 3-5 days | Quick cloud deployment |
| Cloud SQL | €50-150/month | 1 week | Enterprise production |

**Recommendation:** Start with **Supabase**
- Database + storage + auth included
- Instant REST API
- Built-in admin dashboard
- Free tier for development

**See full schema:** `docs/STAKEHOLDER_REQUIREMENTS.md` (Section 2)

---

### 3. How much does development and operation cost? ✅

**DETAILED COST BREAKDOWN:**

#### Development (One-Time)

| Scope | Timeline | Cost |
|-------|----------|------|
| **Minimum (Internal Tool)** | 2-3 weeks | €13K-21K |
| **Standard (Partner Service)** | 6-8 weeks | €20K-35K |
| **Full Platform** | 3-4 months | €78K-131K |

#### Operations (Monthly)

| Scale | Users/Month | Cost |
|-------|-------------|------|
| **Low** | <100 analyses | €125-210/month |
| **Medium** | 100-500 analyses | €250-450/month |
| **High** | 500+ analyses | €500-800/month |

#### Per-Analysis Cost

- **Image:** ~€0.02 per ad
- **Video:** ~€0.35-0.65 per minute

#### Year 1 Investment Summary

```
WITHOUT Validation Studies:
Development: €13K-21K
Operations:  €1.5K-5K
TOTAL:       €15K-26K

WITH Validation Studies (for credibility):
Development: €13K-21K
Validation:  €65K-110K
Operations:  €1.5K-5K
TOTAL:       €80K-136K
```

#### Revenue Models (to offset costs)

**Freemium:**
- Free: 5 analyses/month
- Pro (€49/month): 50 analyses/month
- Business (€199/month): Unlimited
- Enterprise (€999/month): Custom + API

**Pay-Per-Use:**
- €2-5 per image
- €10-20 per video

**Certification:**
- €500-2,000 per "RAI Verified" badge
- Annual renewal

**See full breakdown:** `docs/STAKEHOLDER_REQUIREMENTS.md` (Section 3)

---

### 4. How does RAI handle sarcasm? 🧪

**NEEDS TESTING** - Test guide created

**The Challenge:**
- Oatly ad uses satirical, ironic tone
- Tests whether RAI understands intent vs. literal meaning
- Critical for brands using humor/satire

**Expected Performance:**
- **Best case:** Gemini 2.5 Flash detects satire, scores appropriately (75-85/100)
- **Worst case:** Takes irony literally, misinterprets intent (40-55/100)

**How to Test:**

1. **Download the Oatly ad:**
   - Screen record: `Cmd+Shift+5` → https://www.youtube.com/watch?v=j4IFNKYmLa8
   - Save as .mp4

2. **Analyze via RAI:**
   ```bash
   ./start.sh
   # Upload video via Video Analysis tab
   # Add context note about satirical tone
   ```

3. **Check results:**
   - Does it mention "satirical" or "ironic"?
   - Is ethical score appropriate for the tone?
   - Any literal misinterpretations?

**Potential Improvements (if needed):**
- Add explicit tone detection to prompt
- Add "Tone" field to submission form
- Add confidence scores for tone interpretation
- Provide more context examples

**Complete testing guide:** `docs/SARCASM_TEST_GUIDE.md`

---

## What's Been Delivered

### 📄 Documents Created

1. **STAKEHOLDER_REQUIREMENTS.md** - Full analysis of all 4 questions
   - Detailed options for each requirement
   - Technical specifications
   - Cost breakdowns
   - Implementation roadmaps

2. **SARCASM_TEST_GUIDE.md** - Complete testing protocol
   - How to download/test Oatly ad
   - What to look for in results
   - Interpretation guide
   - Prompt improvements if needed

3. **STAKEHOLDER_RESPONSE_SUMMARY.md** - This document
   - Quick reference for all answers
   - Links to detailed docs

### 💻 Code Created

1. **submit_ad.py** - Ad submission form prototype
   - Public-facing interface
   - Collects all metadata
   - Saves to queue
   - Ready to test

**Try it now:**
```bash
streamlit run submit_ad.py
```

---

## Decision Points for Stakeholder

### 1. Primary Use Case?
- [ ] Internal tool (Telekom only)
- [ ] Partner service (agencies, advertisers)
- [ ] Public platform (anyone can submit)

### 2. Budget Range?
- [ ] Minimum (~€15K year 1)
- [ ] Standard (~€25K year 1)
- [ ] Full platform (~€80K year 1)
- [ ] With validation (~€136K year 1)

### 3. Timeline?
- [ ] MVP in 1 month
- [ ] Beta in 2-3 months
- [ ] Full platform in 4-6 months

### 4. Leaderboard Public or Private?
- [ ] Public rankings (industry transparency)
- [ ] Private only (advertisers see their own data)
- [ ] Hybrid (public aggregate, private details)

### 5. Revenue Model?
- [ ] Cost center (internal tool, no revenue)
- [ ] Freemium (free tier + paid plans)
- [ ] Pay-per-use (per analysis pricing)
- [ ] Certification program (badges/verification)

---

## Immediate Next Steps

### 🧪 Test Sarcasm Handling (You)
1. Screen record Oatly ad
2. Upload to RAI via Video Analysis
3. Share results
4. Decide if prompt improvements needed

**Time:** 15-30 minutes

### 🎨 Demo Submission Form (You)
1. Run `streamlit run submit_ad.py`
2. Try submitting a test ad
3. Check the `submissions/` folder
4. Provide feedback on UX

**Time:** 10 minutes

### 💰 Get Budget Approval (Stakeholder)
1. Review cost breakdown in STAKEHOLDER_REQUIREMENTS.md
2. Decide on scope (minimum/standard/full)
3. Approve initial phase budget
4. Confirm timeline expectations

**Time:** 1-2 business days

### 🎯 Define Use Case (Both)
1. Who are the primary users?
2. Public or private leaderboard?
3. Revenue model required?
4. What features are must-haves vs. nice-to-haves?

**Time:** 30-60 minute meeting

---

## Files to Review

| File | Purpose | Size |
|------|---------|------|
| `docs/STAKEHOLDER_REQUIREMENTS.md` | Full technical analysis | 15K words |
| `docs/SARCASM_TEST_GUIDE.md` | Testing protocol | 3K words |
| `submit_ad.py` | Working submission form | Functional code |
| `docs/STAKEHOLDER_RESPONSE_SUMMARY.md` | This quick reference | 2K words |

---

## Questions?

**Technical questions?**
→ See detailed docs above

**Cost questions?**
→ See Section 3 of STAKEHOLDER_REQUIREMENTS.md

**Timeline questions?**
→ See implementation roadmaps in each section

**Want to discuss strategy?**
→ Schedule 30-min call to go through decision points

---

## Summary of Answers

✅ **Form for ad submissions:** YES - Prototype built (submit_ad.py)
✅ **Storage & leaderboard:** YES - Schema designed, 3 options provided
✅ **Development costs:** YES - Full breakdown: €15K-136K year 1 depending on scope
🧪 **Sarcasm handling:** NEEDS TESTING - Guide created, awaiting Oatly test results

**Status:** Ready for stakeholder review and decision on next phase.

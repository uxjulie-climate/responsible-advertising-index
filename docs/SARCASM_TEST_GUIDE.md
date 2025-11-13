# Sarcasm & Irony Testing Guide

**Test Case:** Oatly "Wow No Cow!" Ad
**URL:** https://www.youtube.com/watch?v=j4IFNKYmLa8
**Challenge:** Does RAI understand satirical tone and ironic messaging?

---

## About the Oatly Ad

**Oatly's Brand Strategy:**
- Known for self-aware, ironic advertising
- Often satirizes traditional dairy advertising
- Uses humor to critique conventional marketing tactics
- Deliberately "anti-advertising" advertising

**Expected Characteristics:**
- Satirical tone
- Self-aware humor
- Ironic claims or exaggerations
- Meta-commentary on advertising itself
- Underlying serious message about sustainability

---

## How to Test

### Step 1: Download the Ad

**Option A: Screen Recording (Recommended)**
1. Open video in browser: https://www.youtube.com/watch?v=j4IFNKYmLa8
2. Press `Cmd+Shift+5` (Mac) or `Win+G` (Windows)
3. Select area or full screen
4. Click Record
5. Play the video
6. Stop recording when done
7. Save as .mp4

**Option B: Browser Extension (if you trust it)**
- Use a video downloader extension
- Be cautious of security/privacy concerns

**Option C: VLC Media Player**
1. Open VLC
2. Media > Open Network Stream
3. Paste URL
4. Media > Convert/Save
5. Choose format and save

### Step 2: Analyze with RAI

1. **Start RAI:**
   ```bash
   cd /Users/julieschiller/responsible-advertising-index
   ./start.sh
   ```

2. **Go to Video Analysis tab**

3. **Upload the Oatly video**

4. **Add ad copy (if any text visible):**
   - Transcribe any text that appears on screen
   - Note any voiceover/dialogue

5. **Important: Add context in the ad copy field:**
   ```
   [Note: This ad uses satirical/ironic tone. Oatly is known for
   self-aware advertising that mocks traditional dairy marketing
   while promoting plant-based alternatives.]
   ```

6. **Click "Analyze Video"**

### Step 3: Evaluate Results

**What to Look For:**

#### ✅ Good Signs (RAI understands sarcasm)
- Mentions "satirical," "ironic," or "humorous" tone
- Recognizes self-aware marketing strategy
- Understands the underlying sustainability message
- Scores ethical communication positively for transparency
- Notes that humor serves a responsible purpose

#### ⚠️ Mixed Signs (Partial understanding)
- Identifies some irony but not consistently
- Flags some satirical elements as concerns
- Scores are moderate but findings show confusion
- Misses the meta-commentary aspect

#### ❌ Bad Signs (RAI misses sarcasm)
- Takes ironic statements literally
- Flags satirical exaggerations as misleading
- Low ethical scores due to misunderstanding tone
- Completely misses the intended message
- No mention of humor or satire

---

## Expected RAI Analysis

### Best Case Scenario

**Overall Score:** 75-85/100

**Climate Responsibility (80-90):**
- Strengths: Promotes plant-based alternative to dairy
- Strengths: Addresses environmental impact of dairy industry
- Note: Uses humor to make sustainability message more engaging

**Social Responsibility (70-80):**
- Strengths: Inclusive messaging
- Note: Self-aware approach avoids manipulation

**Cultural Sensitivity (75-85):**
- Strengths: Understands audience and cultural context
- Note: Satirical tone may not translate across all cultures

**Ethical Communication (75-85):**
- Strengths: Transparent about being advertising
- Strengths: Uses irony to critique greenwashing and conventional marketing
- Strengths: Honest about product benefits without exaggeration
- Note: Satirical tone serves to increase transparency, not deceive

**Key Findings:**
- "Ad employs satirical tone to critique traditional dairy advertising"
- "Self-aware, ironic approach increases transparency"
- "Humor is used to make serious sustainability message more accessible"
- "Meta-commentary on advertising itself demonstrates ethical awareness"

### Worst Case Scenario

**Overall Score:** 40-55/100

**Ethical Communication (30-45):**
- Concerns: Makes exaggerated claims (if taken literally)
- Concerns: Tone may be confusing or misleading
- Concerns: Unclear messaging

**Findings:**
- Takes ironic statements at face value
- Flags humor as potential manipulation
- Doesn't recognize satirical intent

---

## What We Learn

### If RAI Understands Sarcasm:
✅ Gemini 2.5 Flash has good tone detection
✅ Context clues are sufficient
✅ Current prompt works for complex communication
✅ RAI can handle sophisticated advertising

### If RAI Struggles with Sarcasm:
❌ Need to enhance prompts for tone detection
❌ May require explicit "tone" field in submissions
❌ Should add examples of irony/satire to training
❌ Consider adding confidence scores for tone detection

---

## Prompt Improvements (If Needed)

### Enhancement 1: Explicit Tone Detection

Add to analysis prompt:

```
STEP 1: TONE ANALYSIS
Before analyzing content, identify the tone:
- Is this ad serious, humorous, satirical, or ironic?
- Is there self-aware meta-commentary?
- Are any claims meant to be taken literally vs. figuratively?
- What is the INTENDED message vs. the surface-level words?

If sarcasm or irony is detected:
- Analyze the UNDERLYING message
- Note that tone is a deliberate communication strategy
- Assess whether the irony serves a responsible purpose
- Don't penalize irony that increases transparency or critiques greenwashing
```

### Enhancement 2: Context Field

Add to submission form and analysis:

```python
ad_context = st.text_area(
    "Additional Context (Optional)",
    help="Is this ad satirical? Self-aware? Responding to criticism? "
         "Any context that helps interpret the tone correctly.",
    height=80
)
```

### Enhancement 3: Confidence Scores

Add to output:

```json
{
  "tone_detection": {
    "detected_tone": "satirical",
    "confidence": 0.85,
    "reasoning": "Ad uses ironic language patterns, self-aware commentary,
                  and humor to critique conventional advertising"
  }
}
```

---

## Testing Checklist

- [ ] Download Oatly ad video
- [ ] Upload to RAI Video Analysis
- [ ] Add context note about satirical tone
- [ ] Run analysis
- [ ] Review overall score
- [ ] Check if "satirical" or "ironic" appears in findings
- [ ] Evaluate ethical communication score (should be positive)
- [ ] Note any literal misinterpretations
- [ ] Document what worked / what didn't
- [ ] Decide if prompt improvements are needed

---

## Results Template

**Date Tested:** _______________
**RAI Version:** _______________

**Overall Score:** ____/100

**Did RAI detect sarcasm?** ☐ Yes  ☐ Partially  ☐ No

**Evidence:**
- Mentions of tone: ________________________________
- Literal misinterpretations: ________________________________
- Correct interpretations: ________________________________

**Ethical Communication Score:** ____/100
**Was it appropriate given the satirical tone?** ☐ Yes  ☐ No

**Recommendations:**
☐ Current prompt is sufficient
☐ Minor improvements needed
☐ Major prompt overhaul needed
☐ Add explicit tone field to submissions
☐ Add confidence scoring for tone detection

**Notes:**
_______________________________________________________________
_______________________________________________________________

---

## Next Steps After Testing

1. **Document results** in this guide
2. **Share findings** with stakeholders
3. **Implement prompt improvements** if needed
4. **Test with other satirical ads** to validate
5. **Update methodology documentation** with tone detection approach

---

**Ready to Test?**

```bash
cd /Users/julieschiller/responsible-advertising-index
./start.sh
# Then upload the Oatly video via Video Analysis tab
```

Good luck! This will be a great test of RAI's sophistication.

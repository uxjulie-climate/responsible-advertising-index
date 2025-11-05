# Using Google Cloud Credits with Vertex AI

This guide shows you how to use your **Google Cloud startup credits** instead of the free Google AI API.

## 🎯 When to Use This

✅ **Use Vertex AI when:**
- You're ready for production
- You want to use your startup credits
- You need higher rate limits
- You want enterprise features

❌ **Stick with free API for:**
- Demos and testing
- Learning and development
- Quick prototypes

## 💰 Cost Comparison

| | Free Google AI API | Vertex AI (Your Credits) |
|---|---|---|
| **Cost** | FREE up to quota | ~$0.01-0.02 per ad |
| **Your Credits** | No | ✅ Yes |
| **Rate Limit** | 60/min | Much higher |
| **Setup** | 2 minutes | 15 minutes |

**Your startup credits will last a LONG time.** Even analyzing 10,000 ads would only cost ~$100-200.

## 🚀 Setup Steps

### Step 1: Enable Vertex AI in Google Cloud

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Select your project (or create one)
3. Go to **Vertex AI** → **Enable API**
4. Wait for it to enable (takes ~1 minute)

### Step 2: Check Gemini Availability

Gemini models are available in these regions:
- `us-central1` (Iowa)
- `us-east4` (Virginia)
- `europe-west1` (Belgium)
- `asia-northeast1` (Tokyo)

Pick the one closest to you!

### Step 3: Install Google Cloud SDK

```bash
# On Mac with Homebrew:
brew install --cask google-cloud-sdk

# Or download installer:
# https://cloud.google.com/sdk/docs/install
```

### Step 4: Authenticate

```bash
# Login to Google Cloud
gcloud auth login

# Set default project
gcloud config set project YOUR_PROJECT_ID

# Set up application credentials
gcloud auth application-default login
```

### Step 5: Install Python Libraries

```bash
pip3 install google-cloud-aiplatform
```

### Step 6: Update Your App

I'll provide an updated `app_vertex.py` file that uses Vertex AI instead of the free API.

## 📝 Code Changes for Vertex AI

Here's what changes in the code:

### Before (Free API):
```python
import google.generativeai as genai

genai.configure(api_key=api_key)
model = genai.GenerativeModel('gemini-1.5-pro')
```

### After (Vertex AI):
```python
import vertexai
from vertexai.generative_models import GenerativeModel

vertexai.init(project="your-project-id", location="us-central1")
model = GenerativeModel("gemini-1.5-pro")
```

## 🔧 Full Vertex AI Version

I'll create `app_vertex.py` for you with all the changes needed.

### Key Differences:

1. **No API key needed** - Uses Google Cloud authentication
2. **Project ID required** - Your GCP project
3. **Region selection** - Pick closest region
4. **Billing from credits** - Uses your startup credits automatically

## 📊 Monitoring Your Usage & Credits

### Check Your Credits:

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Click **Billing** → **Credits**
3. See remaining balance

### Monitor API Usage:

1. Go to **Vertex AI** → **Dashboard**
2. See request count and costs
3. Set up budget alerts

### Set Budget Alerts:

```bash
# Set an alert when you've used $50 of credits
gcloud billing budgets create \
  --billing-account=YOUR_BILLING_ACCOUNT \
  --display-name="RAI Demo Budget" \
  --budget-amount=50
```

## 🎯 Recommended Approach

### Phase 1: Demo (Now)
✅ Use the **free Google AI API**
- No setup needed
- Perfect for demos
- File: `app.py` (current version)

### Phase 2: Testing (Next Week)
✅ Switch to **Vertex AI**
- Uses your startup credits
- Higher limits
- File: `app_vertex.py` (I'll create this)

### Phase 3: Production (Next Month)
✅ Add features:
- Batch processing
- Database storage
- Higher concurrency

## 💡 Pro Tips

1. **Start with free API** - Perfect for your demo this week
2. **Switch to Vertex AI** - When you're ready to scale
3. **Set budget alerts** - So you don't accidentally use all credits
4. **Use us-central1** - Usually fastest and cheapest
5. **Cache results** - Don't re-analyze the same ad twice

## 🔐 Security Best Practices

### For Free API:
- ✅ Never commit API key to Git
- ✅ Use environment variables
- ✅ Rotate keys regularly

### For Vertex AI:
- ✅ Use service accounts
- ✅ Set IAM permissions carefully
- ✅ Enable audit logging
- ✅ Use VPC for production

## 📈 Cost Estimation

Based on Gemini 1.5 Pro pricing:

| Usage | Free API | Vertex AI (Your Credits) |
|-------|----------|-------------------------|
| 10 ads | FREE | ~$0.10-0.20 |
| 100 ads | FREE* | ~$1-2 |
| 1,000 ads | Rate limited | ~$10-20 |
| 10,000 ads | Not feasible | ~$100-200 |

*Free tier has quota limits

**With $10,000 in startup credits**, you could analyze 50,000+ ads!

## 🚀 Next Steps

### For Your Demo This Week:
1. ✅ Use current `app.py` with free API
2. ✅ Get free API key (2 minutes)
3. ✅ Test with 5-10 sample ads
4. ✅ Demo successfully!

### After Demo Success:
1. ⏭️ I'll create `app_vertex.py` for you
2. ⏭️ Set up Vertex AI (15 minutes)
3. ⏭️ Migrate to use your credits
4. ⏭️ Scale to thousands of ads

## 📞 Getting Help

**Vertex AI Issues:**
- Documentation: https://cloud.google.com/vertex-ai/docs
- Pricing: https://cloud.google.com/vertex-ai/pricing
- Support: Google Cloud Console → Support

**Startup Credits Issues:**
- Check: https://cloud.google.com/startup
- Contact: Your Google Cloud rep
- Community: Google Cloud Startup Slack

## ✅ Checklist for Vertex AI Setup

When you're ready to switch:

- [ ] Google Cloud project created
- [ ] Vertex AI API enabled
- [ ] Billing account with credits linked
- [ ] gcloud SDK installed
- [ ] Authenticated with gcloud
- [ ] Region selected (us-central1 recommended)
- [ ] Budget alerts configured
- [ ] Service account created (optional, for production)

---

## 🎉 Bottom Line

**For now:** Use the free API - it's perfect for your demo!

**Later:** Switch to Vertex AI to use your startup credits and scale up.

You have the best of both worlds! 🚀

---

**Want me to create the Vertex AI version now, or wait until after your demo?**

Most people start with the free API for demos, then upgrade to Vertex AI for production. Your choice!

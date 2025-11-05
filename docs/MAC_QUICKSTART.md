# Mac Quick Start Guide 🍎

## ✅ Complete Setup for Mac (5 Minutes)

### Step 1: Check Python Installation

Open Terminal and run:
```bash
python3 --version
```

You should see something like `Python 3.9.x` or higher.

**If Python is not installed:**
```bash
# Install Homebrew first (if you don't have it):
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Then install Python:
brew install python
```

### Step 2: Navigate to the Project Folder

```bash
# Replace with your actual path:
cd ~/Downloads/rai_demo_gemini
```

### Step 3: Install Required Packages

**Important:** On Mac, use `pip3` (not `pip`):

```bash
pip3 install -r requirements.txt
```

You should see it installing:
- ✓ streamlit
- ✓ google-generativeai
- ✓ pillow
- ✓ plotly

This takes 30-60 seconds.

### Step 4: Get Your Free Google AI API Key

1. Open browser: https://makersuite.google.com/app/apikey
2. Sign in with Google
3. Click "Create API Key"
4. Copy the key (looks like: `AIzaSy...`)

### Step 5: Run the App

```bash
streamlit run app.py
```

A browser window opens automatically at `http://localhost:8501`

### Step 6: Use the App

1. Paste your API key in the sidebar (left side)
2. Upload an ad image
3. Paste the ad text
4. Click "Analyze"
5. Wait 10-30 seconds
6. See your results!

---

## 🐛 Common Mac Issues & Fixes

### Issue: "zsh: command not found: pip"

**Fix:** Use `pip3` instead:
```bash
pip3 install -r requirements.txt
```

### Issue: "Permission denied" for setup.sh

**Fix:** Give it permission first:
```bash
chmod +x setup.sh
./setup.sh
```

### Issue: "Module not found: streamlit"

**Fix:** Reinstall packages:
```bash
pip3 install --upgrade -r requirements.txt
```

### Issue: Port 8501 already in use

**Fix:** Kill existing Streamlit process:
```bash
pkill -f streamlit
streamlit run app.py
```

### Issue: App won't open in browser

**Fix:** Manually open:
```
Open Safari/Chrome and go to: http://localhost:8501
```

---

## 🎯 Quick Commands Reference

```bash
# Check Python version
python3 --version

# Check pip version  
pip3 --version

# Install packages
pip3 install -r requirements.txt

# Run the app
streamlit run app.py

# Stop the app
Press Ctrl+C in Terminal

# Check if streamlit installed
streamlit --version

# Update all packages
pip3 install --upgrade -r requirements.txt
```

---

## 📱 Terminal Tips for Mac

**Open Terminal:**
- Press `Cmd + Space`
- Type "Terminal"
- Press Enter

**Navigate to folder:**
```bash
# See where you are:
pwd

# List files:
ls

# Go to Downloads:
cd ~/Downloads

# Go to Desktop:
cd ~/Desktop

# Go back one folder:
cd ..
```

**Copy/paste in Terminal:**
- Copy: `Cmd + C`
- Paste: `Cmd + V`

---

## ✅ Success Checklist

Before running the demo:

- [ ] Python 3.8+ installed (`python3 --version`)
- [ ] pip3 working (`pip3 --version`)
- [ ] All packages installed (no errors from pip3 install)
- [ ] Google AI API key obtained
- [ ] App runs without errors (`streamlit run app.py`)
- [ ] Can upload image and see it
- [ ] Analysis works (test with sample ad)
- [ ] Results display correctly

---

## 🎉 You're Ready!

Once all checkboxes are ✅, you're ready to demo!

**Pro tip:** Test with 2-3 sample ads from `SAMPLE_AD_COPY.md` before your real demo.

---

## 📞 Still Having Issues?

Common fixes:

**Everything fails:**
```bash
# Nuclear option - reinstall everything:
pip3 install --upgrade pip
pip3 install --force-reinstall -r requirements.txt
```

**Streamlit won't start:**
```bash
# Try running with full path:
python3 -m streamlit run app.py
```

**API key not working:**
- Make sure you copied the ENTIRE key
- Check there are no extra spaces
- Generate a new key if needed

---

**Need more help?** Check `README.md` for detailed documentation!

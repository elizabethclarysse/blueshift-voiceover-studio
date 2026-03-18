# Quick Setup with OpenAI API Key ⚡

## Step 1: Add Your API Key

### For Local Testing:
```bash
cd voice-replacement-tool

# Copy the example file
cp .env.example .env

# Edit .env and add your key
# Change this line:
OPENAI_API_KEY=your_openai_api_key_here

# To your actual key:
OPENAI_API_KEY=sk-proj-xxxxxxxxxxxxx
```

### For Railway Deployment:
1. Go to https://railway.app
2. Deploy your project
3. Click on your project → **Variables** tab
4. Add new variable:
   - **Name:** `OPENAI_API_KEY`
   - **Value:** `sk-proj-xxxxxxxxxxxxx` (your key)

### For Render Deployment:
1. Go to https://render.com
2. Deploy your project
3. Go to **Environment** tab
4. Add:
   - **Key:** `OPENAI_API_KEY`
   - **Value:** `sk-proj-xxxxxxxxxxxxx` (your key)

---

## Step 2: Deploy or Run

### Option A: Get Public URL (Fastest)
```bash
./deploy.sh
```

### Option B: Run Locally
```bash
./start.sh
# Then open: http://localhost:5002
```

---

## What You Get with OpenAI API Key

✅ **Transcription:** Whisper API (~$0.006/minute)
✅ **6 AI Voices:**
- Alloy (Neutral, balanced)
- Echo (Male, clear)
- Fable (British accent, expressive)
- Onyx (Deep male)
- Nova (Female, energetic)
- Shimmer (Female, soft)

---

## Cost Estimate

**Example 5-minute video:**
- Transcription: $0.03
- Voice synthesis: $0.02
- **Total: ~$0.05**

Very affordable! 🎉

---

## Test It Out

1. Upload a short video/audio file
2. Select "OpenAI API" for transcription
3. Choose a voice (try Nova or Onyx)
4. Click "Process Video"
5. Download your result!

---

## Need Help?

**API Key Issues:**
- Make sure key starts with `sk-`
- No spaces or quotes around the key
- Check you have credits at https://platform.openai.com/usage

**Deployment Issues:**
- See GET_PUBLIC_URL.md
- See DEPLOYMENT.md

You're all set! 🚀

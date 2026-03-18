# Quick Deploy to Public URL (5 Minutes)

## Fastest Method: Railway ⚡

### Step 1: Prepare Repository (2 min)

```bash
cd voice-replacement-tool

# Initialize git (if not already done)
git init
git add .
git commit -m "Initial deployment"
```

### Step 2: Deploy to Railway (3 min)

**Option A: Using Railway Website (Recommended)**

1. Go to **https://railway.app**
2. Click **"Start a New Project"**
3. Click **"Deploy from GitHub repo"**
4. If first time: Authorize Railway to access your GitHub
5. Click **"Deploy from local repo"** or push to GitHub first
6. Railway will automatically:
   - Detect Python app
   - Install FFmpeg (via nixpacks.toml)
   - Deploy your app

**Option B: Using Railway CLI (Alternative)**

```bash
# Install Railway CLI
npm install -g @railway/cli
# or: brew install railway

# Login
railway login

# Initialize and deploy
railway init
railway up
```

### Step 3: Add API Keys (1 min)

In Railway Dashboard:
1. Click on your project
2. Go to **"Variables"** tab
3. Click **"+ New Variable"**
4. Add:
   - `OPENAI_API_KEY` = `sk-your-key-here`
   - `ELEVENLABS_API_KEY` = `your-key` (optional)

### Step 4: Get Your Public URL

Railway automatically generates a URL like:
```
https://voice-replacement-tool-production-XXXX.up.railway.app
```

Find it in:
- Railway Dashboard → Settings → Domains
- Or click "Open App" button

**Done! Your app is live!** 🎉

---

## Alternative: Render (Also Easy)

### Step 1: Push to GitHub

```bash
cd voice-replacement-tool
git init
git add .
git commit -m "Initial deployment"

# Create a new repo on GitHub, then:
git remote add origin https://github.com/YOUR_USERNAME/voice-tool.git
git branch -M main
git push -u origin main
```

### Step 2: Deploy on Render

1. Go to **https://render.com**
2. Click **"New +"** → **"Web Service"**
3. Connect your GitHub repository
4. Render auto-detects settings from `render.yaml`
5. Click **"Create Web Service"**

### Step 3: Add Environment Variables

In Render Dashboard:
1. Go to your service
2. Click **"Environment"** tab
3. Add:
   - `OPENAI_API_KEY`
   - `ELEVENLABS_API_KEY` (optional)

### Step 4: Get Your URL

Render provides:
```
https://voice-replacement-tool.onrender.com
```

**Done!** 🎉

---

## Testing Your Deployment

1. Open your public URL
2. Upload a short video/audio file (start with <10 MB)
3. Select voice and options
4. Click "Process Video"
5. Download result

---

## Troubleshooting

**"Application failed to start"**
```bash
# Check logs
railway logs  # for Railway
# or check Render dashboard logs
```

**"FFmpeg not found"**
- Railway: Should work automatically via nixpacks.toml
- Render: Check that FFmpeg is in system packages

**"API key error"**
- Verify environment variables are set correctly
- No spaces or quotes around the key value
- Redeploy after adding variables

**"Out of memory"**
- Use OpenAI API for transcription instead of local Whisper
- Upgrade to paid tier if needed

---

## Cost Estimate

**Railway:**
- Free: ~500 hours/month
- Pro: $5/month (flat rate)

**Render:**
- Free: 750 hours/month (sleeps after 15 min inactivity)
- Starter: $7/month (always on)

**OpenAI API Usage:**
- Whisper transcription: ~$0.006 per minute
- TTS synthesis: ~$15 per 1M characters
- Example: 1 hour video = $0.36 + ~$0.50 = ~$0.86

---

## What's Next?

✅ Share your URL with users
✅ Monitor usage in Railway/Render dashboard
✅ Set up custom domain (optional)
✅ Add analytics (optional)
✅ Configure file cleanup for production

---

**Need help?** Check DEPLOYMENT.md for detailed guide.

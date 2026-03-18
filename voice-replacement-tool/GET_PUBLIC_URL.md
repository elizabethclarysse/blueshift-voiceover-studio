# Get a Public URL in 5 Minutes ⚡

## 🎯 Fastest Path: Railway (Recommended)

### Prerequisites
- OpenAI API key from https://platform.openai.com/api-keys

### Method 1: One-Command Deploy

```bash
cd voice-replacement-tool
./deploy.sh
```

The script will guide you through the deployment process!

---

### Method 2: Manual Railway Deploy

**Step 1: Go to Railway**
```
https://railway.app
```

**Step 2: Click "New Project"**
- Sign up/login with GitHub
- Click "Deploy from GitHub repo"
- Select or upload this folder

**Step 3: Add Your API Key**
- Click your project → "Variables"
- Add: `OPENAI_API_KEY` = `your-key-here`

**Step 4: Get Your URL**
- Settings → Generate Domain
- URL appears: `https://your-app.up.railway.app`

**Done!** Visit your URL and start using the tool!

---

## 🚀 Alternative: Render

**Step 1: Push to GitHub**
```bash
cd voice-replacement-tool
git init
git add .
git commit -m "Deploy voice tool"

# Create repo on GitHub, then:
git remote add origin https://github.com/YOUR_USERNAME/voice-tool.git
git push -u origin main
```

**Step 2: Deploy on Render**
1. Go to https://render.com
2. New Web Service → Connect GitHub repo
3. Render auto-configures from `render.yaml`

**Step 3: Add Environment Variables**
- Environment tab → Add `OPENAI_API_KEY`

**Step 4: Get URL**
- Your URL: `https://voice-tool.onrender.com`

---

## 🐳 Docker Deployment

For Digital Ocean, AWS, Google Cloud, etc:

```bash
# Build
docker build -t voice-tool .

# Run locally to test
docker run -p 5002:5002 \
  -e OPENAI_API_KEY=your-key \
  voice-tool

# Deploy to your cloud provider
# (See their Docker deployment docs)
```

---

## ✅ Verify Deployment

Once deployed, test your app:

1. **Health Check:**
   ```
   https://your-url.com/health
   ```
   Should return: `{"status": "healthy"}`

2. **Upload Test:**
   - Visit your URL
   - Upload a small video/audio file
   - Select voice options
   - Click "Process Video"
   - Download result

---

## 🔑 Getting Your OpenAI API Key

1. Go to https://platform.openai.com/
2. Sign up or login
3. Click your profile → "API keys"
4. Click "Create new secret key"
5. Copy the key (starts with `sk-`)
6. Add to your deployment's environment variables

**Costs:**
- Transcription: ~$0.006 per minute
- Voice synthesis: ~$15 per 1M characters
- Example 5-min video: ~$0.05 total

---

## 📊 Platform Comparison

| Platform | Deploy Time | Free Tier | Best For |
|----------|-------------|-----------|----------|
| **Railway** | 3 min | 500 hrs/mo | Fastest deploy ⚡ |
| **Render** | 5 min | 750 hrs/mo | Reliability |
| **Fly.io** | 10 min | Hobby tier | Performance |
| **Heroku** | 10 min | None | Legacy apps |

**Recommendation:** Start with Railway!

---

## 🆘 Common Issues

**"Application Error"**
- Check logs in platform dashboard
- Verify `OPENAI_API_KEY` is set
- Ensure FFmpeg installed (auto on Railway/Render)

**"Transcription failed"**
- Check API key is valid
- Verify you have OpenAI credits
- Try with smaller file first

**"Too slow"**
- Use OpenAI API for transcription (not local Whisper)
- Upgrade to paid tier for more resources
- Process smaller files

---

## 🎉 You're Ready!

Your app should now be live at a public URL. Share it with:
- Team members
- Clients
- Users

**Example URLs you might get:**
- Railway: `https://voice-tool-production-abc123.up.railway.app`
- Render: `https://voice-replacement-tool.onrender.com`
- Custom domain: `https://voicetool.yourdomain.com` (set up in platform settings)

---

## 📚 More Resources

- **QUICKSTART_DEPLOY.md** - Detailed 5-minute guide
- **DEPLOYMENT.md** - Comprehensive deployment guide
- **README.md** - Full app documentation

**Questions?** Check the deployment docs or platform support:
- Railway: https://docs.railway.app
- Render: https://render.com/docs

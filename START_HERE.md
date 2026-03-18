# 🎬 Voice Replacement Tool - Start Here!

## What This Does

Upload a video → Transcribe it → Replace audio with a different voice → Download result

**Simple. Fast. Powerful.**

---

## 🚀 Two Ways to Use This Tool

### Option 1: Get a Public URL (Recommended) ⭐

**Perfect for:** Sharing with others, production use, no local setup

**Time:** 5 minutes

**Follow this guide:**
```
📄 GET_PUBLIC_URL.md
```

**Quick steps:**
1. Go to https://railway.app
2. Deploy from this folder
3. Add your OpenAI API key
4. Get your public URL
5. Done!

---

### Option 2: Run Locally

**Perfect for:** Testing, development, offline use

**Time:** 10 minutes

**Steps:**

1. **Install FFmpeg:**
   ```bash
   brew install ffmpeg  # macOS
   ```

2. **Run startup script:**
   ```bash
   cd voice-replacement-tool
   ./start.sh
   ```

3. **Add API key:**
   - Edit `.env` file
   - Add: `OPENAI_API_KEY=your-key-here`

4. **Access:**
   ```
   http://localhost:5002
   ```

---

## 🔑 Get Your OpenAI API Key

You need this for either option:

1. Visit: https://platform.openai.com/api-keys
2. Sign up or login
3. Create new secret key
4. Copy it (starts with `sk-`)

**Cost:** ~$0.05 per 5-minute video

---

## 📖 Full Documentation

- **GET_PUBLIC_URL.md** - Deploy to public URL (5 min) ⚡
- **QUICKSTART_DEPLOY.md** - Detailed deployment guide
- **DEPLOYMENT.md** - Advanced deployment options
- **README.md** - Complete app documentation

---

## 🎯 Quick Test

Once running, test with:
1. Upload a short video/audio file
2. Select a voice (try "Nova" or "Onyx")
3. Click "Process Video"
4. Download and watch result

---

## ✨ Features

✅ Supports: MP4, AVI, MOV, MKV, MP3, WAV, M4A, FLAC
✅ 6 different AI voices
✅ Drag & drop upload
✅ Preserves video quality
✅ Fast transcription
✅ Clean, modern UI

---

## 🆘 Need Help?

**Quick answers:**
- App won't start? → Check FFmpeg is installed
- API error? → Verify OpenAI key is set correctly
- Processing fails? → Try smaller file first
- Want public URL? → See GET_PUBLIC_URL.md

**Platform support:**
- Railway: https://docs.railway.app
- Render: https://render.com/docs

---

## 🎉 Ready to Start?

Choose your path:

**For Public URL (Recommended):**
```bash
# Read this first:
open GET_PUBLIC_URL.md

# Then run:
./deploy.sh
```

**For Local Testing:**
```bash
./start.sh
```

**Happy voice replacing!** 🎤✨

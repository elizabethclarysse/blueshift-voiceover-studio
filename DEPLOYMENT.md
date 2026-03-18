# Deployment Guide - Voice Replacement Tool

This guide will help you deploy your voice replacement tool to a public URL.

## Recommended Platforms

### Option 1: Railway (Easiest - Recommended)

**Why Railway?**
- Free tier available
- Automatic HTTPS
- Built-in FFmpeg support
- One-click deployment
- Custom domain support

**Steps:**

1. **Prepare your repository:**
```bash
cd voice-replacement-tool
git init
git add .
git commit -m "Initial commit"
```

2. **Deploy to Railway:**
   - Go to [railway.app](https://railway.app)
   - Sign up with GitHub
   - Click "New Project" → "Deploy from GitHub repo"
   - Select your repository
   - Railway will auto-detect the configuration

3. **Add environment variables:**
   - In Railway dashboard, go to your project
   - Click "Variables" tab
   - Add:
     - `OPENAI_API_KEY` = your OpenAI key
     - `ELEVENLABS_API_KEY` = your ElevenLabs key (optional)

4. **Get your URL:**
   - Railway provides: `https://your-app.up.railway.app`
   - Or add a custom domain in Settings

**Estimated Cost:** Free for ~500 hours/month, then $5/month

---

### Option 2: Render

**Why Render?**
- Free tier includes 750 hours/month
- Easy deployment
- FFmpeg available
- Good for production

**Steps:**

1. **Push to GitHub:**
```bash
cd voice-replacement-tool
git init
git add .
git commit -m "Initial commit"
# Create repo on GitHub and push
git remote add origin https://github.com/yourusername/voice-tool.git
git push -u origin main
```

2. **Deploy on Render:**
   - Go to [render.com](https://render.com)
   - Click "New +" → "Web Service"
   - Connect your GitHub repository
   - Render will detect `render.yaml` automatically

3. **Configure:**
   - Name: `voice-replacement-tool`
   - Environment: `Python 3`
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `gunicorn --bind 0.0.0.0:$PORT --timeout 600 --workers 2 app:app`

4. **Add Environment Variables:**
   - `OPENAI_API_KEY`
   - `ELEVENLABS_API_KEY` (optional)

5. **Your URL:**
   - Render provides: `https://voice-replacement-tool.onrender.com`

**Estimated Cost:** Free tier (spins down after inactivity), or $7/month for always-on

---

### Option 3: Fly.io

**Why Fly.io?**
- Good free tier
- Fast deployment
- Global edge network

**Steps:**

1. **Install Fly CLI:**
```bash
brew install flyctl  # macOS
# or curl -L https://fly.io/install.sh | sh
```

2. **Login and launch:**
```bash
cd voice-replacement-tool
fly auth login
fly launch
```

3. **Set environment variables:**
```bash
fly secrets set OPENAI_API_KEY=your-key-here
fly secrets set ELEVENLABS_API_KEY=your-key-here
```

4. **Deploy:**
```bash
fly deploy
```

5. **Get URL:**
```bash
fly status
# Your app: https://your-app.fly.dev
```

**Estimated Cost:** Free for hobby projects

---

### Option 4: Heroku

**Steps:**

1. **Install Heroku CLI:**
```bash
brew tap heroku/brew && brew install heroku
```

2. **Login and create app:**
```bash
cd voice-replacement-tool
heroku login
heroku create your-voice-tool
```

3. **Add FFmpeg buildpack:**
```bash
heroku buildpacks:add --index 1 https://github.com/jonathanong/heroku-buildpack-ffmpeg-latest.git
heroku buildpacks:add --index 2 heroku/python
```

4. **Set environment variables:**
```bash
heroku config:set OPENAI_API_KEY=your-key-here
heroku config:set ELEVENLABS_API_KEY=your-key-here
```

5. **Deploy:**
```bash
git init
git add .
git commit -m "Initial commit"
git push heroku main
```

6. **Open your app:**
```bash
heroku open
# URL: https://your-voice-tool.herokuapp.com
```

**Estimated Cost:** $7/month (no free tier anymore)

---

## Production Considerations

### 1. File Storage

For production, consider using cloud storage:

**AWS S3 / Cloudflare R2:**
```python
# Add to requirements.txt:
# boto3>=1.28.0

# In app.py, replace file saving with S3 upload
import boto3

s3 = boto3.client('s3',
    aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
    aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY')
)

# Upload file
s3.upload_file(local_path, 'bucket-name', file_key)
```

### 2. File Cleanup

Add automatic cleanup for old files:

```python
# Add to app.py
import time
from pathlib import Path

def cleanup_old_files():
    """Remove files older than 1 hour"""
    for folder in ['uploads', 'outputs', 'temp']:
        for file in Path(folder).glob('*'):
            if time.time() - file.stat().st_mtime > 3600:
                file.unlink()

# Call periodically or use a cron job
```

### 3. Rate Limiting

Protect your API:

```bash
pip install flask-limiter
```

```python
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

limiter = Limiter(
    app=app,
    key_func=get_remote_address,
    default_limits=["10 per hour"]
)
```

### 4. Monitoring

Add health check endpoint:

```python
@app.route('/health')
def health():
    return {'status': 'ok', 'timestamp': time.time()}
```

### 5. Background Processing

For long videos, use background jobs:

```bash
pip install celery redis
```

---

## Quick Deployment Comparison

| Platform | Free Tier | Setup Time | FFmpeg | Custom Domain | Best For |
|----------|-----------|------------|--------|---------------|----------|
| **Railway** | 500 hrs/mo | 5 min | ✅ Built-in | ✅ Free | **Recommended** |
| **Render** | 750 hrs/mo | 10 min | ✅ Available | ✅ Free | Production |
| **Fly.io** | Hobby tier | 15 min | ⚠️ Manual | ✅ Free | Performance |
| **Heroku** | None | 10 min | ⚠️ Buildpack | ✅ Paid | Legacy apps |

---

## Troubleshooting Deployment

**"Application Error" or crashes:**
- Check logs: `railway logs` or `render logs` or `fly logs`
- Ensure all environment variables are set
- Verify FFmpeg is installed (check buildpack)

**"Out of Memory":**
- Whisper uses a lot of RAM. Use OpenAI API instead of local
- Upgrade to paid tier with more memory
- Reduce concurrent workers in Gunicorn

**"Timeout errors":**
- Increase timeout in Procfile/start command to 600s
- Use background jobs for large files
- Show user estimated processing time

**"FFmpeg not found":**
- Railway: Should work automatically
- Render: Add apt packages in render.yaml
- Heroku: Ensure buildpack is added
- Fly.io: Add to Dockerfile

---

## Security Checklist

- [ ] `.env` file is in `.gitignore`
- [ ] API keys are set as environment variables (not in code)
- [ ] File upload size limits are set (500MB default)
- [ ] Old files are automatically cleaned up
- [ ] Rate limiting is enabled for API endpoints
- [ ] HTTPS is enabled (automatic on most platforms)
- [ ] File validation checks file extensions
- [ ] No sensitive data in logs

---

## Next Steps After Deployment

1. **Test your deployment:**
   - Upload a small test video
   - Verify transcription works
   - Check download functionality

2. **Monitor costs:**
   - OpenAI API usage
   - Platform hosting costs
   - Storage costs

3. **Add analytics (optional):**
   - Google Analytics
   - Plausible
   - Custom logging

4. **Share your URL:**
   - Share with team/users
   - Add to documentation
   - Create demo video

---

## Need Help?

- Railway: [docs.railway.app](https://docs.railway.app)
- Render: [render.com/docs](https://render.com/docs)
- Fly.io: [fly.io/docs](https://fly.io/docs)

For issues with the app itself, check the main README.md

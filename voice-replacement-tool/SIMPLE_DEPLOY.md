# Simple Railway Deployment (No Git Required)

## Method 1: Railway CLI (Easiest)

### Step 1: Install Railway CLI
```bash
npm install -g @railway/cli
# or
brew install railway
```

### Step 2: Login
```bash
railway login
```

### Step 3: Deploy from this folder
```bash
cd voice-replacement-tool
railway init
railway up
```

### Step 4: Add your API key
```bash
railway variables set OPENAI_API_KEY=sk-your-key-here
```

### Step 5: Get your URL
```bash
railway open
```

**Done!** Your app is live.

---

## Method 2: Web Interface (No CLI needed)

### Step 1: Zip this folder
```bash
cd voice-replacement-tool
zip -r voice-tool.zip . -x "*.git*" -x "__pycache__/*" -x "venv/*"
```

### Step 2: Go to Railway
1. Visit https://railway.app
2. Sign up/login
3. Click **"New Project"**
4. Click **"Empty Project"**

### Step 3: Add Python service
1. Click **"+ New"**
2. Select **"Empty Service"**
3. Click on the service
4. Go to **Settings** tab
5. Under **Source**, click **"Connect Repo"** then **"Deploy from local directory"**

### Step 4: Upload files
Railway will guide you through uploading your project folder.

### Step 5: Add Environment Variable
1. Go to **Variables** tab
2. Click **"+ New Variable"**
3. Add:
   - Name: `OPENAI_API_KEY`
   - Value: `sk-your-actual-key`

### Step 6: Get your URL
1. Go to **Settings** tab
2. Scroll to **Networking**
3. Click **"Generate Domain"**
4. Copy your URL: `https://your-app.up.railway.app`

**Done!**

---

## Method 3: GitHub (If you have account)

### Step 1: Create GitHub repo
1. Go to https://github.com/new
2. Name it: `voice-replacement-tool`
3. Create (don't initialize with README)

### Step 2: Push code
```bash
cd voice-replacement-tool
git init
git add .
git commit -m "Deploy voice tool"
git remote add origin https://github.com/YOUR_USERNAME/voice-replacement-tool.git
git branch -M main
git push -u origin main
```

### Step 3: Deploy on Railway
1. Go to https://railway.app
2. Click **"New Project"**
3. Click **"Deploy from GitHub repo"**
4. Select your repo

### Step 4: Add API key
Variables tab → Add `OPENAI_API_KEY`

**Done!**

---

## Which Method Should You Use?

- **CLI** (Method 1): Fastest if you have npm/brew ⚡
- **Web** (Method 2): No tools needed, just browser
- **GitHub** (Method 3): Best for version control

---

## Troubleshooting

**Railway CLI not found:**
```bash
npm install -g @railway/cli
```

**"Authentication required":**
```bash
railway login
```

**App crashes:**
- Check logs: `railway logs`
- Verify OPENAI_API_KEY is set
- Make sure FFmpeg is installed (automatic with nixpacks.toml)

---

## After Deployment

Your URL will be something like:
```
https://voice-replacement-tool-production-abc123.up.railway.app
```

Test it by:
1. Opening the URL
2. Uploading a small video/audio file
3. Selecting voice options
4. Processing and downloading

✅ **You're live!**

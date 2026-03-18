#!/bin/bash

echo "🚀 Voice Replacement Tool - Quick Railway Deploy"
echo "================================================"
echo ""

# Check if Railway CLI is installed
if ! command -v railway &> /dev/null; then
    echo "❌ Railway CLI not found!"
    echo ""
    echo "Install it first:"
    echo "  npm install -g @railway/cli"
    echo "  # or"
    echo "  brew install railway"
    echo ""
    exit 1
fi

echo "✅ Railway CLI found!"
echo ""

# Check if user is logged in
railway whoami &> /dev/null
if [ $? -ne 0 ]; then
    echo "🔐 Please login to Railway..."
    railway login
    echo ""
fi

# Ask for OpenAI API key
echo "Enter your OpenAI API key (starts with sk-):"
read -s OPENAI_KEY
echo ""

if [ -z "$OPENAI_KEY" ]; then
    echo "❌ No API key provided!"
    exit 1
fi

# Check if already initialized
if [ ! -f "railway.json" ]; then
    echo "❌ railway.json not found. Are you in the right directory?"
    exit 1
fi

# Initialize Railway project if not already
if [ ! -f ".railway/config.json" ]; then
    echo "📋 Initializing Railway project..."
    railway init
    echo ""
fi

# Set environment variable
echo "🔑 Setting API key..."
railway variables set OPENAI_API_KEY="$OPENAI_KEY"
echo ""

# Deploy
echo "🚀 Deploying to Railway..."
railway up
echo ""

# Get the URL
echo "✅ Deployment complete!"
echo ""
echo "Your app is deploying now. Get your URL with:"
echo "  railway open"
echo ""
echo "Or check status:"
echo "  railway status"
echo ""
echo "View logs:"
echo "  railway logs"
echo ""
echo "🎉 Done! Your voice replacement tool will be live in ~2 minutes."

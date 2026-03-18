#!/bin/bash

echo "🚀 Voice Replacement Tool - Quick Deploy Script"
echo "================================================"
echo ""

# Check if Railway CLI is installed
if command -v railway &> /dev/null; then
    echo "✅ Railway CLI found!"

    read -p "Deploy to Railway now? (y/n): " deploy_railway

    if [ "$deploy_railway" = "y" ]; then
        echo ""
        echo "🚂 Deploying to Railway..."

        # Initialize git if needed
        if [ ! -d ".git" ]; then
            echo "📦 Initializing git repository..."
            git init
            git add .
            git commit -m "Initial deployment"
        fi

        # Login to Railway
        echo "🔐 Logging in to Railway..."
        railway login

        # Initialize project
        echo "📋 Initializing Railway project..."
        railway init

        # Deploy
        echo "🚀 Deploying..."
        railway up

        echo ""
        echo "✅ Deployment complete!"
        echo ""
        echo "⚠️  Don't forget to add your environment variables:"
        echo "   railway variables set OPENAI_API_KEY=your-key-here"
        echo ""
        echo "🌐 Open your app:"
        echo "   railway open"

        exit 0
    fi
fi

# If Railway CLI not found
echo "ℹ️  Railway CLI not found. Install it with:"
echo ""
echo "   npm install -g @railway/cli"
echo "   # or"
echo "   brew install railway"
echo ""
echo "Or deploy manually:"
echo "1. Go to https://railway.app"
echo "2. Click 'New Project' → 'Deploy from GitHub'"
echo "3. Connect this repository"
echo "4. Add environment variables in Railway dashboard"
echo ""

read -p "Would you like to initialize git for manual deployment? (y/n): " init_git

if [ "$init_git" = "y" ]; then
    if [ ! -d ".git" ]; then
        echo ""
        echo "📦 Initializing git repository..."
        git init
        git add .
        git commit -m "Initial deployment"
        echo ""
        echo "✅ Git initialized!"
        echo ""
        echo "Next steps:"
        echo "1. Create a new repository on GitHub"
        echo "2. Run: git remote add origin https://github.com/YOUR_USERNAME/voice-tool.git"
        echo "3. Run: git push -u origin main"
        echo "4. Deploy on Railway or Render using GitHub integration"
    else
        echo "ℹ️  Git repository already exists"
    fi
fi

echo ""
echo "📚 For detailed deployment instructions, see:"
echo "   - QUICKSTART_DEPLOY.md (5-minute guide)"
echo "   - DEPLOYMENT.md (comprehensive guide)"

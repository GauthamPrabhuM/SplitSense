# 🚀 Quick Deployment Guide

## Free Deployment Options

### Option 1: Railway (Recommended) ⭐

**FREE:** $5/month credit (plenty for small apps)

1. Push code to GitHub
2. Go to https://railway.app
3. Click "New Project" → "Deploy from GitHub repo"
4. Select your repository
5. Railway auto-detects Dockerfile and deploys!
6. Set environment variables in Railway dashboard
7. Done!

See `DEPLOY_RAILWAY.md` for detailed steps.

---

### Option 2: Render

**FREE:** Free tier (spins down after 15min inactivity)

1. Go to https://render.com
2. Click "New" → "Web Service"
3. Connect GitHub repo
4. Auto-detects Dockerfile
5. Set environment variables
6. Deploy!

**Note:** First request after inactivity takes ~30 seconds (cold start)

---

### Option 3: Koyeb

**FREE:** Free tier (always-on, no spin-down)

1. Go to https://koyeb.com
2. Click "Create App" → "GitHub"
3. Select your repo
4. Auto-detects Dockerfile
5. Set environment variables
6. Deploy!

---

## Required Environment Variables

Set these in your deployment platform:

```
SPLITWISE_CLIENT_ID=your_client_id
SPLITWISE_CLIENT_SECRET=your_client_secret
SPLITWISE_REDIRECT_URI=https://your-app-domain.com/auth/callback
ENVIRONMENT=production
CORS_ORIGINS=https://your-app-domain.com
FRONTEND_URL=https://your-app-domain.com
BASE_CURRENCY=USD
MASK_SENSITIVE_DATA=true
```

## Update Splitwise OAuth

1. Go to https://secure.splitwise.com/apps
2. Edit your OAuth app
3. Set Redirect URI to: `https://your-app-domain.com/auth/callback`
4. Save

## Recommendation

**Use Railway** - Simplest, most reliable, and truly free for small apps!


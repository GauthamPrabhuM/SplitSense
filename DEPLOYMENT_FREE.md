# Free Deployment Guide - Vercel + Render

## Overview

This guide deploys SplitSense using **100% free hosting**:
- **Frontend**: Vercel (Next.js) - Free tier
- **Backend**: Render (FastAPI) - Free tier

**Total Cost: $0/month**

## Free Tier Limits

### Vercel (Frontend)
- ✅ Unlimited deployments
- ✅ 100GB bandwidth/month
- ✅ Automatic HTTPS
- ✅ Global CDN
- ✅ Custom domains
- ⚠️ Serverless functions: 100GB-hours/month

### Render (Backend)
- ✅ 750 hours/month (enough for 24/7)
- ✅ 512MB RAM
- ✅ Automatic HTTPS
- ⚠️ Spins down after 15 min inactivity (wakes on request)
- ⚠️ No persistent storage (use environment variables)

## Step 1: Deploy Backend to Render

### 1.1 Create Render Account

1. Go to https://render.com
2. Sign up with GitHub
3. Connect your GitHub account

### 1.2 Create Web Service

1. Click **"New +"** → **"Web Service"**
2. Connect your repository
3. Configure:
   - **Name**: `splitsense-backend`
   - **Region**: Choose closest to you
   - **Branch**: `main`
   - **Root Directory**: `/` (root)
   - **Environment**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `uvicorn main:app --host 0.0.0.0 --port $PORT`

### 1.3 Set Environment Variables

In Render dashboard, add these **Environment Variables**:

```bash
# Required - OAuth
SPLITWISE_CLIENT_ID=your_client_id
SPLITWISE_CLIENT_SECRET=your_client_secret
SPLITWISE_REDIRECT_URI=https://splitsense-backend.onrender.com/auth/callback

# Application
ENVIRONMENT=production
CORS_ORIGINS=https://splitsense.vercel.app
FRONTEND_URL=https://splitsense.vercel.app
BASE_CURRENCY=USD
MASK_SENSITIVE_DATA=true
LOCAL_ONLY=false
USE_DB_POOLING=false

# Optional - Database (if you add PostgreSQL later)
# DATABASE_URL=postgresql://user:pass@host:5432/dbname
```

**Important**: Mark `SPLITWISE_CLIENT_SECRET` as **Secret** (click the lock icon)

### 1.4 Get Backend URL

After deployment, Render will give you a URL like:
```
https://splitsense-backend.onrender.com
```

**Note**: First request after inactivity may take 30-60 seconds (cold start)

### 1.5 Update Splitwise OAuth

1. Go to https://secure.splitwise.com/apps
2. Edit your OAuth app
3. Set **Redirect URI** to: `https://splitsense-backend.onrender.com/auth/callback`
4. Save

## Step 2: Deploy Frontend to Vercel

### 2.1 Create Vercel Account

1. Go to https://vercel.com
2. Sign up with GitHub
3. Connect your GitHub account

### 2.2 Import Project

1. Click **"Add New"** → **"Project"**
2. Select your repository
3. Configure:
   - **Framework Preset**: Next.js (auto-detected)
   - **Root Directory**: `frontend`
   - **Build Command**: `npm run build` (default)
   - **Output Directory**: `.next` (default)

### 2.3 Set Environment Variables

In Vercel dashboard → **Settings** → **Environment Variables**, add:

```bash
NEXT_PUBLIC_API_URL=https://splitsense-backend.onrender.com
```

### 2.4 Deploy

1. Click **"Deploy"**
2. Vercel will build and deploy automatically
3. You'll get a URL like: `https://splitsense.vercel.app`

### 2.5 Update Backend CORS

1. Go back to Render dashboard
2. Update `CORS_ORIGINS` environment variable:
   ```
   https://splitsense.vercel.app,https://splitsense.netlify.app
   ```
3. Update `FRONTEND_URL`:
   ```
   https://splitsense.vercel.app
   ```
4. Redeploy backend (or it will auto-redeploy)

## Step 3: Configure Frontend API Proxy

The `vercel.json` file is already configured to proxy API calls. If you need to update it:

1. Edit `vercel.json`
2. Update the `destination` URLs to your Render backend URL
3. Push to GitHub (Vercel auto-deploys)

## Step 4: Test Deployment

### 4.1 Test Backend

```bash
# Health check
curl https://splitsense-backend.onrender.com/api/health

# Should return:
{
  "status": "healthy",
  "version": "2.0.0",
  "oauth_available": true
}
```

### 4.2 Test Frontend

1. Visit your Vercel URL: `https://splitsense.vercel.app`
2. Click "Connect with Splitwise"
3. Should redirect and load data

## Step 5: Custom Domain (Optional)

### Vercel Custom Domain

1. Vercel dashboard → **Settings** → **Domains**
2. Add your domain
3. Follow DNS instructions
4. Free SSL automatically configured

### Render Custom Domain

1. Render dashboard → **Settings** → **Custom Domains**
2. Add your domain
3. Update `SPLITWISE_REDIRECT_URI` to use custom domain
4. Update `CORS_ORIGINS` and `FRONTEND_URL`

## Troubleshooting

### Backend Takes Long to Respond

**Issue**: First request after inactivity takes 30-60 seconds

**Solution**: 
- This is normal for Render free tier (spins down after 15 min)
- Consider using a monitoring service to ping your backend every 10 minutes
- Or upgrade to paid tier ($7/month) for always-on

### CORS Errors

**Issue**: Frontend can't connect to backend

**Solution**:
1. Check `CORS_ORIGINS` includes your Vercel URL
2. Check `FRONTEND_URL` is correct
3. Redeploy backend after changing env vars

### OAuth Not Working

**Issue**: OAuth redirect fails

**Solution**:
1. Verify `SPLITWISE_REDIRECT_URI` matches Render backend URL exactly
2. Check Splitwise app settings match
3. Check backend logs in Render dashboard

### Build Failures

**Backend (Render)**:
- Check build logs in Render dashboard
- Verify `requirements.txt` is correct
- Check Python version (should be 3.11)

**Frontend (Vercel)**:
- Check build logs in Vercel dashboard
- Verify `package.json` is correct
- Check Node version (should be 18+)

## Monitoring (Free Options)

### Uptime Monitoring

Use free services to keep Render backend warm:
- **UptimeRobot**: https://uptimerobot.com (50 monitors free)
- **Cronitor**: https://cronitor.io (free tier)
- **Pingdom**: https://pingdom.com (free trial)

Set up a monitor to ping:
```
https://splitsense-backend.onrender.com/api/health
```
Every 10 minutes to prevent spin-down

### Error Tracking

- **Sentry**: https://sentry.io (free tier: 5K events/month)
- **LogRocket**: https://logrocket.com (free trial)

## Cost Breakdown

| Service | Tier | Cost |
|---------|------|------|
| Vercel (Frontend) | Free | $0 |
| Render (Backend) | Free | $0 |
| **Total** | | **$0/month** |

## Limitations of Free Tier

### Render Free Tier
- ⚠️ Spins down after 15 min inactivity (cold start ~30-60s)
- ⚠️ 512MB RAM limit
- ⚠️ No persistent storage (use env vars or external DB)
- ⚠️ Limited to 750 hours/month (enough for 24/7)

### Vercel Free Tier
- ✅ No major limitations for this app
- ✅ Generous bandwidth (100GB/month)

## Upgrade Path (If Needed)

If you need better performance:

1. **Render Paid**: $7/month
   - Always-on (no spin-down)
   - 512MB RAM
   - Better performance

2. **Vercel Pro**: $20/month
   - More bandwidth
   - Team features
   - Better analytics

## Alternative: Netlify + Render

If you prefer Netlify over Vercel:

### Netlify Frontend Setup

1. Go to https://netlify.com
2. **Add site** → **Import from Git**
3. Configure:
   - **Base directory**: `frontend`
   - **Build command**: `npm run build`
   - **Publish directory**: `frontend/.next`
4. Add environment variable:
   ```
   NEXT_PUBLIC_API_URL=https://splitsense-backend.onrender.com
   ```

### Netlify Redirects

Create `frontend/netlify.toml`:
```toml
[[redirects]]
  from = "/api/*"
  to = "https://splitsense-backend.onrender.com/api/:splat"
  status = 200
  force = true

[[redirects]]
  from = "/auth/*"
  to = "https://splitsense-backend.onrender.com/auth/:splat"
  status = 200
  force = true
```

## Quick Start Checklist

- [ ] Create Render account
- [ ] Deploy backend to Render
- [ ] Set backend environment variables
- [ ] Get backend URL
- [ ] Update Splitwise OAuth redirect URI
- [ ] Create Vercel account
- [ ] Deploy frontend to Vercel
- [ ] Set frontend environment variable
- [ ] Update backend CORS with Vercel URL
- [ ] Test deployment
- [ ] Set up uptime monitoring (optional)

## Support

- Render Docs: https://render.com/docs
- Vercel Docs: https://vercel.com/docs
- Render Status: https://status.render.com
- Vercel Status: https://www.vercel-status.com


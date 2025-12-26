# Quick Fix: Deploy to Vercel Without Dashboard

## Problem
Can't edit Root Directory or other settings in Vercel dashboard.

## Solution: Use Vercel CLI (2 minutes)

### Step 1: Install Vercel CLI

```bash
npm install -g vercel
```

### Step 2: Deploy from Frontend Directory

```bash
cd frontend
vercel login
vercel --prod
```

### Step 3: Set Environment Variable

```bash
vercel env add NEXT_PUBLIC_API_URL production
# When prompted, enter: https://splitsense.onrender.com
```

**Done!** Your app is deployed.

## Or Use the Script

```bash
./deploy-vercel.sh
```

This script does everything automatically!

## Why This Works

- Vercel CLI doesn't need Root Directory setting
- It auto-detects Next.js from `frontend/` directory
- Uses `frontend/vercel.json` automatically
- No dashboard configuration needed

## After Deployment

1. Get your Vercel URL (shown after deploy)
2. Update Render backend:
   - `CORS_ORIGINS` = your Vercel URL
   - `FRONTEND_URL` = your Vercel URL
3. Redeploy backend

That's it! 🎉


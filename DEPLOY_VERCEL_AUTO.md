# Auto-Deploy to Vercel (No Dashboard Configuration Needed)

## Method 1: Deploy from Frontend Directory (Recommended)

Since you can't edit settings in the dashboard, we'll configure everything via files.

### Step 1: Connect Repository

1. Go to https://vercel.com
2. Click **"Add New"** → **"Project"**
3. Select your GitHub repository
4. **Don't configure anything yet** - just click **"Deploy"**

### Step 2: After First Deploy Fails

The first deploy will fail (expected). Now:

1. Go to your Vercel project dashboard
2. Click **Settings** → **General**
3. Scroll to **Root Directory**
4. Click **Edit** → Type: `frontend` → **Save**

**If you still can't edit it**, use Method 2 below.

## Method 2: Use Vercel CLI (No Dashboard Needed)

### Install Vercel CLI

```bash
npm install -g vercel
```

### Deploy from Frontend Directory

```bash
# Navigate to frontend directory
cd frontend

# Login to Vercel
vercel login

# Deploy (follow prompts)
vercel

# For production
vercel --prod
```

This will:
- Auto-detect Next.js
- Use `vercel.json` in frontend directory
- Deploy without needing dashboard settings

### Set Environment Variables via CLI

```bash
cd frontend
vercel env add NEXT_PUBLIC_API_URL
# Enter: https://splitsense-backend.onrender.com
# Select: Production, Preview, Development
```

## Method 3: GitHub Integration (Automatic)

If you connected via GitHub:

1. The `frontend/vercel.json` file will be used automatically
2. Set environment variables in Vercel dashboard:
   - Go to **Settings** → **Environment Variables**
   - Add: `NEXT_PUBLIC_API_URL` = `https://splitsense-backend.onrender.com`
3. Push to `main` branch - Vercel will auto-deploy

## Method 4: Manual Root Directory Fix

If dashboard won't let you edit Root Directory:

1. **Delete the project** in Vercel
2. **Re-import** the repository
3. **Before clicking Deploy**, look for **"Configure Project"** or **"Advanced"** options
4. Set Root Directory to `frontend` there
5. Then deploy

## Quick CLI Deploy (Easiest)

```bash
# One-time setup
cd frontend
npm install -g vercel
vercel login

# Deploy
vercel --prod

# Set env var
vercel env add NEXT_PUBLIC_API_URL production
# Paste: https://splitsense-backend.onrender.com
```

This bypasses all dashboard configuration!

## Files Created

- `frontend/vercel.json` - Vercel config in frontend directory
- `.vercelignore` - Tells Vercel to focus on frontend

## After Deployment

1. Get your Vercel URL (e.g., `https://splitsense.vercel.app`)
2. Update Render backend CORS:
   - `CORS_ORIGINS` = `https://splitsense.vercel.app`
   - `FRONTEND_URL` = `https://splitsense.vercel.app`
3. Redeploy backend

## Troubleshooting

### "No Next.js version detected"

**Solution**: Use Vercel CLI from `frontend/` directory (Method 2)

### "Build failed"

**Solution**: 
```bash
cd frontend
npm install
npm run build
# If this works locally, Vercel should work too
```

### Can't set Root Directory

**Solution**: Use Vercel CLI - it doesn't need Root Directory setting

## Recommended: Use Vercel CLI

The CLI method is the most reliable when dashboard settings are locked:

```bash
cd frontend
vercel login
vercel --prod
vercel env add NEXT_PUBLIC_API_URL production
```

Done! 🎉


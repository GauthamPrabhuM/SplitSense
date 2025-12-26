# Quick Free Deployment (5 Minutes)

## Option 1: Vercel + Render (Recommended)

### Backend (Render) - 2 minutes

1. Go to https://render.com → Sign up with GitHub
2. **New +** → **Web Service**
3. Connect repo → Configure:
   - **Name**: `splitsense-backend`
   - **Build**: `pip install -r requirements.txt`
   - **Start**: `uvicorn main:app --host 0.0.0.0 --port $PORT`
4. Add environment variables:
   ```
   SPLITWISE_CLIENT_ID=xxx
   SPLITWISE_CLIENT_SECRET=xxx
   SPLITWISE_REDIRECT_URI=https://splitsense-backend.onrender.com/auth/callback
   ENVIRONMENT=production
   CORS_ORIGINS=https://splitsense.vercel.app
   FRONTEND_URL=https://splitsense.vercel.app
   ```
5. Deploy → Copy URL (e.g., `https://splitsense-backend.onrender.com`)

### Frontend (Vercel) - 2 minutes

1. Go to https://vercel.com → Sign up with GitHub
2. **Add New** → **Project**
3. Import repo → Configure:
   - **Root Directory**: `frontend` ⚠️ **IMPORTANT: Must set this!**
   - **Framework**: Next.js (auto-detected)
   - **Build Command**: `npm run build` (auto)
   - **Output Directory**: `.next` (auto)
4. Add environment variable:
   ```
   NEXT_PUBLIC_API_URL=https://splitsense-backend.onrender.com
   ```
5. **Deploy** → Copy URL (e.g., `https://splitsense.vercel.app`)

**⚠️ If build fails with "No Next.js version detected":**
- Go to **Settings** → **General** → **Root Directory**
- Make sure it's set to `frontend` (not root `/`)
- Click **Save** and **Redeploy**

### Update Backend CORS - 1 minute

1. Go back to Render
2. Update `CORS_ORIGINS` and `FRONTEND_URL` with your Vercel URL
3. Redeploy

**Done!** Your app is live at your Vercel URL.

## Option 2: Netlify + Render

Same as above, but use Netlify instead of Vercel:

1. Go to https://netlify.com
2. **Add site** → **Import from Git**
3. **Root directory**: `frontend`
4. **Build command**: `npm run build`
5. **Publish directory**: `.next`
6. Add env var: `NEXT_PUBLIC_API_URL=https://splitsense-backend.onrender.com`

## Important Notes

⚠️ **Render Free Tier**: Spins down after 15 min inactivity. First request may take 30-60s.

💡 **Solution**: Use UptimeRobot (free) to ping your backend every 10 minutes:
- URL: `https://splitsense-backend.onrender.com/api/health`
- Interval: 10 minutes

## Cost: $0/month

Both services have generous free tiers that are perfect for this app!


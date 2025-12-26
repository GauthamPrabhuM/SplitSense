# Deploy to Railway (FREE - $5/month credit)

## Why Railway?

✅ **FREE** - $5/month credit (plenty for small apps)  
✅ **Super simple** - Just connect GitHub and deploy  
✅ **Automatic HTTPS** - SSL certificates handled automatically  
✅ **No configuration needed** - Detects Dockerfile automatically  
✅ **Full-stack ready** - Perfect for backend + frontend together  

## Quick Deploy (3 minutes)

### Step 1: Push to GitHub

Make sure your code is on GitHub:
```bash
git add .
git commit -m "Ready for deployment"
git push origin main
```

### Step 2: Deploy on Railway

1. Go to https://railway.app
2. Click **"Start a New Project"**
3. Select **"Deploy from GitHub repo"**
4. Choose your repository
5. Railway will automatically detect the Dockerfile and deploy!

That's it! Railway will:
- Build your Docker image
- Deploy it
- Give you a URL (like `https://your-app.up.railway.app`)

### Step 3: Set Environment Variables

In Railway dashboard:
1. Go to your project
2. Click on the service
3. Go to **"Variables"** tab
4. Add these:

```
SPLITWISE_CLIENT_ID=your_client_id
SPLITWISE_CLIENT_SECRET=your_client_secret
SPLITWISE_REDIRECT_URI=https://your-app.up.railway.app/auth/callback
ENVIRONMENT=production
CORS_ORIGINS=https://your-app.up.railway.app
FRONTEND_URL=https://your-app.up.railway.app
BASE_CURRENCY=USD
MASK_SENSITIVE_DATA=true
```

### Step 4: Update Splitwise OAuth

1. Go to https://secure.splitwise.com/apps
2. Edit your OAuth app
3. Set Redirect URI to: `https://your-app.up.railway.app/auth/callback`
4. Save

## Cost

**FREE TIER:**
- $5/month credit (FREE)
- Enough for small to medium apps
- Auto-sleeps when not in use (saves credits)
- Only pay if you exceed $5/month (unlikely for small apps)

## Updating Your App

Just push to GitHub:
```bash
git push origin main
```

Railway automatically deploys on every push to `main` branch!

## Custom Domain (Optional)

1. In Railway dashboard, go to **"Settings"**
2. Click **"Generate Domain"** to get a custom domain
3. Or add your own domain in **"Custom Domains"**

## That's It!

No complex setup, no CLI commands, just:
1. Push to GitHub
2. Connect on Railway
3. Set environment variables
4. Done!

**Truly free and simple!** 🎉


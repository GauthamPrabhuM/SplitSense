# Production Deployment Guide

## Overview

This guide walks you through deploying SplitSense to Railway with a complete CI/CD pipeline.

## Prerequisites

- GitHub account
- Railway account (sign up at https://railway.app)
- Splitwise OAuth app configured (see SETUP_OAUTH.md)

## Step 1: Set Up Railway

### 1.1 Create Railway Account

1. Go to https://railway.app
2. Sign up with GitHub
3. Create a new project: "SplitSense"

### 1.2 Add PostgreSQL Database

1. In Railway project, click **"+ New"**
2. Select **"Database"** → **"Add PostgreSQL"**
3. Railway will create a PostgreSQL instance
4. Note the `DATABASE_URL` from the database service variables

### 1.3 Create Backend Service

1. Click **"+ New"** → **"GitHub Repo"**
2. Select your repository
3. Railway will detect the `Dockerfile`
4. Configure:
   - **Root Directory**: `/` (root)
   - **Build Command**: (auto-detected from Dockerfile)
   - **Start Command**: `uvicorn main:app --host 0.0.0.0 --port $PORT --workers 2`

### 1.4 Create Frontend Service

1. Click **"+ New"** → **"GitHub Repo"** (same repo)
2. Configure:
   - **Root Directory**: `/frontend`
   - **Build Command**: `npm ci && npm run build`
   - **Start Command**: `npm start`
   - **Environment**: Node.js

## Step 2: Configure Environment Variables

### 2.1 Backend Environment Variables

In Railway backend service, add these variables:

```bash
# OAuth Configuration
SPLITWISE_CLIENT_ID=your_client_id
SPLITWISE_CLIENT_SECRET=your_client_secret
SPLITWISE_REDIRECT_URI=https://your-backend-url.railway.app/auth/callback

# Database
DATABASE_URL=${{Postgres.DATABASE_URL}}  # Reference from PostgreSQL service
USE_DB_POOLING=false  # Set to true for traditional servers

# Application
ENVIRONMENT=production
CORS_ORIGINS=https://your-frontend-url.railway.app,https://your-custom-domain.com
FRONTEND_URL=https://your-frontend-url.railway.app
BASE_CURRENCY=USD
MASK_SENSITIVE_DATA=true
LOCAL_ONLY=false

# Security
PORT=8000  # Railway sets this automatically
```

### 2.2 Frontend Environment Variables

In Railway frontend service, add:

```bash
NEXT_PUBLIC_API_URL=https://your-backend-url.railway.app
NODE_ENV=production
PORT=3000  # Railway sets this automatically
```

### 2.3 Update Splitwise OAuth Redirect URI

1. Go to https://secure.splitwise.com/apps
2. Edit your OAuth app
3. Set **Redirect URI** to: `https://your-backend-url.railway.app/auth/callback`
4. Save

## Step 3: Set Up GitHub Secrets

### 3.1 Get Railway Token

1. Go to Railway dashboard
2. Click your profile → **Settings** → **Tokens**
3. Create new token
4. Copy the token

### 3.2 Add GitHub Secrets

1. Go to your GitHub repository
2. **Settings** → **Secrets and variables** → **Actions**
3. Add these secrets:

```
RAILWAY_TOKEN=your_railway_token
RAILWAY_SERVICE_ID=your_backend_service_id  # Get from Railway service settings
PRODUCTION_URL=https://your-backend-url.railway.app
NEXT_PUBLIC_API_URL=https://your-backend-url.railway.app
```

**To get Service ID:**
- In Railway, go to your backend service
- Click **Settings** → **Service ID** (copy this)

## Step 4: Database Migrations

### 4.1 Initialize Alembic

```bash
# Install Alembic
pip install alembic

# Initialize migrations
alembic init alembic

# Create initial migration
alembic revision --autogenerate -m "Initial migration"

# Apply migration (locally for testing)
alembic upgrade head
```

### 4.2 Run Migrations on Railway

Add to Railway backend service:

**Build Command** (add after pip install):
```bash
pip install -r requirements.txt && alembic upgrade head
```

Or add a migration step in the Dockerfile.

## Step 5: Configure Custom Domains (Optional)

### 5.1 Backend Domain

1. In Railway backend service → **Settings** → **Networking**
2. Click **"Generate Domain"** or **"Add Custom Domain"**
3. Update `SPLITWISE_REDIRECT_URI` to use new domain
4. Update `CORS_ORIGINS` to include new domain

### 5.2 Frontend Domain

1. In Railway frontend service → **Settings** → **Networking**
2. Add custom domain
3. Update `FRONTEND_URL` in backend environment variables

## Step 6: Enable CI/CD

### 6.1 Verify GitHub Actions

The `.github/workflows/deploy.yml` file is already configured. It will:

1. Run tests on every push
2. Build Docker image
3. Deploy to Railway on `main` branch push

### 6.2 Test the Pipeline

1. Make a small change
2. Commit and push to `main`
3. Check GitHub Actions tab
4. Verify deployment in Railway

## Step 7: Production Readiness Checklist

### Security

- [x] HTTPS enabled (automatic on Railway)
- [x] CORS configured for production domains
- [x] Environment variables secured
- [x] Rate limiting enabled
- [x] Input validation (Pydantic)
- [x] OAuth 2.0 for authentication

### Monitoring

- [x] Health check endpoint (`/api/health`)
- [x] Railway built-in logging
- [ ] Optional: Add Sentry for error tracking

### Performance

- [x] Database connection pooling
- [x] Caching for analytics
- [x] Static asset optimization (Next.js)
- [x] Docker multi-stage build

### Reliability

- [x] Automatic restarts on failure
- [x] Health checks
- [x] Database backups (Railway managed)
- [x] Rollback capability

## Step 8: Monitoring & Logs

### View Logs

1. Railway dashboard → Your service → **Logs** tab
2. Real-time logs available
3. Search and filter logs

### Health Checks

```bash
# Check backend health
curl https://your-backend-url.railway.app/api/health

# Should return:
{
  "status": "healthy",
  "version": "2.0.0",
  "oauth_available": true
}
```

### Set Up Alerts (Optional)

1. Railway → **Settings** → **Notifications**
2. Configure email/Slack alerts for:
   - Deployment failures
   - Service crashes
   - High error rates

## Step 9: Rollback Procedure

### Manual Rollback

1. Railway dashboard → Your service
2. Click **"Deployments"** tab
3. Find previous successful deployment
4. Click **"Redeploy"**

### Automatic Rollback

GitHub Actions will:
1. Deploy new version
2. Run health check
3. If health check fails, notify (configure Slack webhook)

## Troubleshooting

### Deployment Fails

1. Check Railway logs
2. Check GitHub Actions logs
3. Verify environment variables
4. Check database connection

### OAuth Not Working

1. Verify `SPLITWISE_REDIRECT_URI` matches Splitwise app settings
2. Check CORS configuration
3. Verify OAuth credentials

### Database Connection Issues

1. Check `DATABASE_URL` is correct
2. Verify database is running in Railway
3. Check connection pooling settings

### Frontend Can't Connect to Backend

1. Verify `NEXT_PUBLIC_API_URL` is set correctly
2. Check CORS origins include frontend URL
3. Verify backend is running

## Cost Estimation

### Railway Free Tier

- **$5/month credit** (enough for small apps)
- **PostgreSQL**: Included
- **Bandwidth**: 100GB/month
- **Build minutes**: 500/month

### Estimated Monthly Cost

- **Small app** (< 1000 users): $0-10/month
- **Medium app** (1000-10000 users): $10-50/month
- **Large app** (> 10000 users): $50+/month

## Next Steps

1. **Set up monitoring**: Add Sentry or similar
2. **Add analytics**: Track usage with analytics service
3. **Scale database**: Upgrade PostgreSQL if needed
4. **Add CDN**: For static assets (Railway includes CDN)
5. **Backup strategy**: Railway handles backups, but verify

## Support

- Railway Docs: https://docs.railway.app
- GitHub Actions: https://docs.github.com/en/actions
- FastAPI Docs: https://fastapi.tiangolo.com


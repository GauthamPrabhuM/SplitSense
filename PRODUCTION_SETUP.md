# Production Setup Checklist

## Quick Start

1. **Railway Setup** (15 min)
   - Create Railway account
   - Add PostgreSQL database
   - Create backend service
   - Create frontend service

2. **Environment Variables** (10 min)
   - Configure OAuth credentials
   - Set database URL
   - Configure CORS origins

3. **GitHub Secrets** (5 min)
   - Add Railway token
   - Add service IDs

4. **Deploy** (5 min)
   - Push to main branch
   - GitHub Actions deploys automatically

**Total Time: ~35 minutes**

## Environment Variables Reference

### Backend (Railway)

```bash
# Required
SPLITWISE_CLIENT_ID=xxx
SPLITWISE_CLIENT_SECRET=xxx
SPLITWISE_REDIRECT_URI=https://your-backend.railway.app/auth/callback
DATABASE_URL=${{Postgres.DATABASE_URL}}
ENVIRONMENT=production
CORS_ORIGINS=https://your-frontend.railway.app
FRONTEND_URL=https://your-frontend.railway.app

# Optional
BASE_CURRENCY=USD
MASK_SENSITIVE_DATA=true
USE_DB_POOLING=false
```

### Frontend (Railway)

```bash
NEXT_PUBLIC_API_URL=https://your-backend.railway.app
NODE_ENV=production
```

## GitHub Secrets

```
RAILWAY_TOKEN=xxx
RAILWAY_SERVICE_ID=xxx
PRODUCTION_URL=https://your-backend.railway.app
```

## Testing Production

1. **Health Check**
   ```bash
   curl https://your-backend.railway.app/api/health
   ```

2. **OAuth Flow**
   - Visit frontend
   - Click "Connect with Splitwise"
   - Should redirect and load data

3. **API Endpoints**
   ```bash
   curl https://your-backend.railway.app/api/insights
   ```

## Monitoring

- **Railway Dashboard**: Real-time logs and metrics
- **Health Endpoint**: `/api/health` for uptime monitoring
- **GitHub Actions**: Deployment status

## Rollback

Railway → Service → Deployments → Redeploy previous version


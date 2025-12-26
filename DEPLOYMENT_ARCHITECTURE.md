# Deployment Architecture

## Overview

SplitSense is deployed as a full-stack application on **Railway**, providing a unified platform for frontend, backend, and database with automatic HTTPS and CI/CD integration.

## Architecture Diagram

```
┌─────────────────────────────────────────────────────────────┐
│                        GitHub Repository                     │
│                                                               │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐     │
│  │   Frontend   │  │   Backend    │  │   Database   │     │
│  │  (Next.js)  │  │  (FastAPI)  │  │ (PostgreSQL) │     │
│  └──────────────┘  └──────────────┘  └──────────────┘     │
└─────────────────────────────────────────────────────────────┘
                            │
                            │ Push to main
                            ▼
┌─────────────────────────────────────────────────────────────┐
│                    GitHub Actions CI/CD                      │
│                                                               │
│  1. Run Tests & Lint                                         │
│  2. Build Frontend (Next.js)                                │
│  3. Build Backend (Docker)                                  │
│  4. Deploy to Railway                                        │
└─────────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│                      Railway Platform                        │
│                                                               │
│  ┌─────────────────────────────────────────────────────┐   │
│  │              Frontend Service                        │   │
│  │  • Next.js Production Build                          │   │
│  │  • Static Assets (CDN)                               │   │
│  │  • HTTPS: https://splitsense.app                    │   │
│  └─────────────────────────────────────────────────────┘   │
│                            │                                 │
│                            │ API Calls                       │
│                            ▼                                 │
│  ┌─────────────────────────────────────────────────────┐   │
│  │              Backend Service                         │   │
│  │  • FastAPI Application                              │   │
│  │  • Docker Container                                  │   │
│  │  • HTTPS: https://api.splitsense.app                │   │
│  │  • Environment Variables (Secrets)                  │   │
│  └─────────────────────────────────────────────────────┘   │
│                            │                                 │
│                            │ Database Queries                │
│                            ▼                                 │
│  ┌─────────────────────────────────────────────────────┐   │
│  │         PostgreSQL Database                         │   │
│  │  • Managed PostgreSQL                                │   │
│  │  • Automatic Backups                                │   │
│  │  • Connection Pooling                               │   │
│  └─────────────────────────────────────────────────────┘   │
│                                                               │
│  ┌─────────────────────────────────────────────────────┐   │
│  │         External Services                           │   │
│  │  • Splitwise OAuth API                              │   │
│  │  • Monitoring & Logging                             │   │
│  └─────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────┘
                            │
                            ▼
                    ┌───────────────┐
                    │   End Users   │
                    │  (HTTPS/WSS)  │
                    └───────────────┘
```

## Technology Stack

### Infrastructure
- **Platform**: Railway
- **Frontend Hosting**: Railway (Next.js)
- **Backend Hosting**: Railway (Docker)
- **Database**: Railway PostgreSQL
- **CI/CD**: GitHub Actions
- **Monitoring**: Railway built-in + optional Sentry

### Why Railway?

**Advantages:**
1. **Monorepo Support**: Deploy frontend and backend from same repository
2. **Built-in Database**: PostgreSQL included, no separate setup
3. **Automatic HTTPS**: SSL certificates managed automatically
4. **GitHub Integration**: Direct deployment from GitHub
5. **Environment Variables**: Secure secret management
6. **Easy Rollback**: One-click rollback to previous deployments
7. **Free Tier**: Good for development and small production apps
8. **Simple Pricing**: Pay-as-you-go, no upfront costs

**Alternatives Considered:**
- **Vercel + Railway**: More complex, two platforms to manage
- **AWS/GCP/Azure**: Overkill, more complex, higher cost
- **Render**: Similar to Railway, but Railway has better monorepo support
- **Fly.io**: More complex setup, better for global edge deployment

## Data Flow

1. **User Request** → Frontend (Next.js)
2. **API Call** → Backend (FastAPI) via `/api/*` proxy
3. **Data Processing** → PostgreSQL (if persistence enabled)
4. **External API** → Splitwise OAuth/API
5. **Response** → Frontend → User

## Security Layers

1. **HTTPS**: Automatic SSL/TLS encryption
2. **CORS**: Configured for production domain
3. **Rate Limiting**: API rate limiting middleware
4. **Environment Variables**: Secrets stored securely
5. **OAuth 2.0**: Secure authentication flow
6. **Input Validation**: Pydantic models for all inputs

## Scalability

- **Horizontal Scaling**: Railway auto-scales based on traffic
- **Database**: PostgreSQL connection pooling
- **Caching**: In-memory caching for analytics (can add Redis later)
- **CDN**: Static assets served via Railway CDN

## Monitoring & Logging

- **Application Logs**: Railway built-in logging
- **Error Tracking**: Optional Sentry integration
- **Health Checks**: `/api/health` endpoint
- **Metrics**: Railway dashboard metrics

## Deployment Flow

1. **Developer** pushes to `main` branch
2. **GitHub Actions** triggers:
   - Run tests
   - Lint code
   - Build frontend
   - Build backend Docker image
3. **Railway** receives webhook:
   - Pulls latest code
   - Builds services
   - Runs database migrations
   - Deploys to production
4. **Health Check** verifies deployment
5. **Rollback** available if health check fails


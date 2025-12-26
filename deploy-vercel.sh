#!/bin/bash
# Automated Vercel deployment script
# This bypasses dashboard configuration issues

echo "🚀 Deploying to Vercel..."
echo ""

# Check if vercel CLI is installed
if ! command -v vercel &> /dev/null; then
    echo "📦 Installing Vercel CLI..."
    npm install -g vercel
fi

# Navigate to frontend directory
cd frontend || exit 1

echo "📁 Current directory: $(pwd)"
echo ""

# Check if logged in
if ! vercel whoami &> /dev/null; then
    echo "🔐 Please login to Vercel:"
    vercel login
fi

echo ""
echo "🌍 Setting environment variable..."
echo "Enter your Render backend URL (e.g., https://splitsense-backend.onrender.com):"
read -r BACKEND_URL

if [ -z "$BACKEND_URL" ]; then
    BACKEND_URL="https://splitsense-backend.onrender.com"
    echo "Using default: $BACKEND_URL"
fi

# Set environment variable
echo "Setting NEXT_PUBLIC_API_URL=$BACKEND_URL"
vercel env add NEXT_PUBLIC_API_URL production <<< "$BACKEND_URL" || echo "Env var might already exist"

echo ""
echo "🚀 Deploying to production..."
vercel --prod

echo ""
echo "✅ Deployment complete!"
echo ""
echo "📝 Next steps:"
echo "1. Copy your Vercel URL from above"
echo "2. Update Render backend CORS_ORIGINS with your Vercel URL"
echo "3. Update Render backend FRONTEND_URL with your Vercel URL"
echo "4. Redeploy backend on Render"


#!/bin/bash

# Setup script for SplitSense Dashboard Frontend

echo "🚀 Setting up SplitSense Dashboard..."

# Navigate to frontend directory
cd "$(dirname "$0")"

# Check for Node.js
if ! command -v node &> /dev/null; then
    echo "❌ Node.js is not installed. Please install Node.js 18+ first."
    exit 1
fi

NODE_VERSION=$(node -v | cut -d'v' -f2 | cut -d'.' -f1)
if [ "$NODE_VERSION" -lt 18 ]; then
    echo "❌ Node.js version 18+ is required. Current: $(node -v)"
    exit 1
fi

echo "✓ Node.js $(node -v) detected"

# Install dependencies
echo "📦 Installing dependencies..."
npm install

if [ $? -ne 0 ]; then
    echo "❌ Failed to install dependencies"
    exit 1
fi

echo "✓ Dependencies installed"

# Create .env.local if it doesn't exist
if [ ! -f ".env.local" ]; then
    echo "📝 Creating .env.local..."
    cat > .env.local << EOF
# Backend API URL (for production)
# NEXT_PUBLIC_API_URL=https://your-api-domain.com

# Analytics (optional)
# NEXT_PUBLIC_ANALYTICS_ID=
EOF
    echo "✓ Created .env.local"
fi

echo ""
echo "✅ Setup complete!"
echo ""
echo "To start the development server:"
echo "  cd frontend"
echo "  npm run dev"
echo ""
echo "The dashboard will be available at http://localhost:3000"
echo ""
echo "Make sure the FastAPI backend is running on http://localhost:8000"

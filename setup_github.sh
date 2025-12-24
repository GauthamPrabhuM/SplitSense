#!/bin/bash
# Script to set up and push to a new GitHub repository

REPO_NAME="${1:-splitwise-insights}"  # Default name if not provided
GITHUB_USER=$(git config user.name 2>/dev/null || echo "your-username")

echo "🚀 Setting up GitHub repository: $REPO_NAME"
echo ""

# Check if gh CLI is installed
if command -v gh &> /dev/null; then
    echo "✅ GitHub CLI detected"
    echo ""
    echo "Creating repository on GitHub..."
    gh repo create "$REPO_NAME" --public --source=. --remote=origin --push
    
    if [ $? -eq 0 ]; then
        echo ""
        echo "✅ Repository created and pushed successfully!"
        echo "🌐 View your repo at: https://github.com/$GITHUB_USER/$REPO_NAME"
    else
        echo "❌ Failed to create repository. Trying manual setup..."
        manual_setup
    fi
else
    echo "⚠️  GitHub CLI not found. Using manual setup..."
    manual_setup
fi

function manual_setup() {
    echo ""
    echo "📝 Manual setup instructions:"
    echo ""
    echo "1. Go to https://github.com/new"
    echo "2. Create a new repository named: $REPO_NAME"
    echo "3. DO NOT initialize with README, .gitignore, or license"
    echo "4. Then run these commands:"
    echo ""
    echo "   git remote add origin https://github.com/$GITHUB_USER/$REPO_NAME.git"
    echo "   git branch -M main"
    echo "   git push -u origin main"
    echo ""
    echo "Or if you prefer SSH:"
    echo "   git remote add origin git@github.com:$GITHUB_USER/$REPO_NAME.git"
    echo "   git branch -M main"
    echo "   git push -u origin main"
}


#!/bin/bash
# Setup script for Splitwise Analysis Tool

echo "Setting up Splitwise Analysis Tool..."

# Create virtual environment
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo "Installing dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

# Create data directory
mkdir -p data

echo "Setup complete!"
echo ""
echo "To activate the virtual environment, run:"
echo "  source venv/bin/activate"
echo ""
echo "To start the server, run:"
echo "  uvicorn main:app --reload"
echo ""
echo "Or set your API token and run:"
echo "  export SPLITWISE_API_TOKEN=your_token_here"
echo "  python example_usage.py"


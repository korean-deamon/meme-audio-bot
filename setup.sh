#!/bin/bash

# Exit on error
set -e

echo "🚀 Initializing Meme Audio Master..."

# Create virtual environment if it doesn't exist
if [ ! -d ".venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv .venv
fi

# Activate virtual environment
source .venv/bin/activate

# Install dependencies
echo "📥 Installing dependencies..."
pip install -r requirements.txt

echo "✅ Setup complete!"
echo "👉 To start the bot, run: source .venv/bin/activate && python main.py"

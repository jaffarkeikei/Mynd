#!/bin/bash

# Mynd Installation Script
echo "🧠 Installing Mynd - Universal AI Memory"
echo "============================================"

# Check Python version
python_version=$(python3 --version 2>&1 | grep -o '[0-9]\+\.[0-9]\+')
required_version="3.11"

if [ "$(printf '%s\n' "$required_version" "$python_version" | sort -V | head -n1)" != "$required_version" ]; then
    echo "❌ Python 3.11+ required. Found: $python_version"
    exit 1
fi

echo "✅ Python version check passed"

# Create virtual environment
echo "📦 Creating virtual environment..."
python3 -m venv venv
source venv/bin/activate

# Install dependencies
echo "📥 Installing dependencies..."
pip install --upgrade pip
pip install -e .

# Check for Ollama
echo "🤖 Checking for Ollama..."
if command -v ollama &> /dev/null; then
    echo "✅ Ollama found"
    
    # Check if required model exists
    if ollama list | grep -q "llama3.1:8b-instruct-q4_0"; then
        echo "✅ Required LLM model available"
    else
        echo "📥 Downloading required LLM model..."
        ollama pull llama3.1:8b-instruct-q4_0
    fi
else
    echo "⚠️  Ollama not found. Please install from https://ollama.ai"
    echo "   After installing Ollama, run: ollama pull llama3.1:8b-instruct-q4_0"
fi

# Initialize Mynd
echo "🎯 Initializing Mynd..."
python -m src.cli init

echo ""
echo "🚀 Installation complete!"
echo ""
echo "Next steps:"
echo "  1. Activate the environment: source venv/bin/activate"
echo "  2. Start Mynd: mynd start"
echo "  3. In another terminal, try: mynd demo"
echo "  4. Query your memory: mynd query 'authentication'"
echo ""
echo "🎉 Welcome to the future of AI memory!" 
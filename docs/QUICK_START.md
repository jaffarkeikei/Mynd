# Mynd Quick Start Guide

## 🚀 Running the Demo

The simplest way to see Mynd in action:

```bash
# Run the interactive demo
python scripts/demo.py
```

This demo will:
- ✅ Create sample memories (authentication decisions, database choices, etc.)
- ✅ Show how semantic search finds relevant context
- ✅ Test Claude integration if API key is set

## 🧪 Testing Components

### 1. Test Basic Functionality
```bash
# Check system status
mynd status

# Create demo data
mynd demo

# Query memories
mynd query "authentication decisions"
mynd query "database choice"
```

### 2. Test MCP Server
```bash
# Start the MCP server (in one terminal)
mynd start --port 8765

# Test the server (in another terminal)
python tests/test_mcp.py
```

### 3. Test AI Integration
```bash
# Set your API key
export ANTHROPIC_API_KEY='your-key-here'

# Run integration examples
python examples/real_ai_integration.py
python examples/real_ai_integration_gemini.py
```

## 📁 File Locations

- **Demo Script**: `scripts/demo.py` - Interactive demo
- **MCP Test**: `tests/test_mcp.py` - Tests server functionality
- **AI Examples**: `examples/` - Real AI integration demos

## 🔑 Setting Up API Keys

```bash
# Option 1: Export in terminal
export ANTHROPIC_API_KEY='sk-ant-api03-...'
export GOOGLE_API_KEY='AIzaSy...'

# Option 2: Create .env file
echo "ANTHROPIC_API_KEY=your-key" > .env
echo "GOOGLE_API_KEY=your-key" >> .env
```

## 🎯 Quick Test Sequence

1. **Install & Initialize**:
   ```bash
   ./install.sh
   source venv/bin/activate
   ```

2. **Run Demo**:
   ```bash
   python scripts/demo.py
   ```

3. **Start MCP Server** (optional):
   ```bash
   mynd start --port 8765
   ```

4. **Test Everything**:
   ```bash
   # Basic functionality
   mynd status
   
   # MCP server (if running)
   python tests/test_mcp.py
   
   # AI integration (if API key set)
   python examples/real_ai_integration.py
   ```

## 💡 Tips

- The demo works without any API keys or server
- MCP server is only needed for advanced integrations
- API keys enable real AI responses instead of simulated ones
- All data is stored locally in `~/.mynd/`

## 🆘 Troubleshooting

- **"Server not running"**: Start with `mynd start --port 8765`
- **"No API key"**: Set with `export ANTHROPIC_API_KEY='your-key'`
- **"Module not found"**: Activate venv with `source venv/bin/activate`
- **"Ollama not running"**: Start with `ollama serve` (for local LLM) 
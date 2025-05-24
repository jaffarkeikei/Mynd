# 📁 Mynd Project Structure

This document explains the organized structure of the Mynd project and how to navigate it effectively.

## 🏗️ Directory Layout

```
myndai/
├── 📚 docs/                    # Documentation hub
│   ├── README.md              # Documentation overview
│   ├── api/                   # API documentation
│   │   └── README.md          # Complete API reference
│   ├── guides/                # User and developer guides
│   │   ├── QUICKSTART.md      # Quick start guide
│   │   ├── ARCHITECTURE.md    # System architecture
│   │   ├── COMPONENTS.md      # Component details
│   │   └── *.md              # Additional guides
│   └── images/               # Diagrams and screenshots
│
├── 🎮 demos/                   # Interactive demonstrations
│   ├── practical_memory_test.py    # Real data storage & recall
│   ├── cross_session_demo.py       # Cross-session memory
│   ├── memory_test_example.py      # Basic memory workflow
│   └── random_ai_test.py           # Random scenario testing
│
├── 🔧 examples/                # Real AI integrations
│   ├── real_ai_integration.py      # Claude API integration
│   ├── real_ai_integration_gemini.py # Gemini API integration
│   └── demo_real_ai.py             # Simplified demo
│
├── ⚙️ scripts/                 # Setup and utility scripts
│   ├── quick_setup.py         # One-command project setup
│   ├── run_demos.py           # Demo launcher with menu
│   ├── setup_api_keys.py      # Interactive API key setup
│   ├── test_my_keys.py        # API connectivity testing
│   └── env_example.txt        # Environment template
│
├── 🧪 tests/                   # Test suites
│   ├── real_world_demo.py     # Real-world testing
│   ├── real_world_test.py     # Comprehensive tests
│   └── demo_test.py           # Basic functionality tests
│
├── 🧠 src/                     # Core implementation
│   ├── main.py                # Main orchestrator
│   ├── mcp_server.py          # FastAPI MCP server
│   ├── vector_storage.py      # ChromaDB integration
│   └── semantic_extractor.py  # Content processing
│
├── 📄 Root Files
│   ├── README.md              # Project overview
│   ├── .gitignore             # Git ignore rules
│   ├── requirements.txt       # Python dependencies
│   ├── pyproject.toml         # Project configuration
│   └── test_server.py         # Development server
```

## 🚀 Quick Start Commands

### **Setup & Installation**
```bash
# Complete project setup
python scripts/quick_setup.py

# Setup API keys interactively
python scripts/setup_api_keys.py

# Start the MCP server
python test_server.py
```

### **Running Demos**
```bash
# List all available demos
python scripts/run_demos.py --list

# Run specific demo
python scripts/run_demos.py --demo memory-test

# Interactive demo menu
python scripts/run_demos.py --interactive

# Check prerequisites
python scripts/run_demos.py --check
```

### **Testing & Validation**
```bash
# Test API keys
python scripts/test_my_keys.py

# Run comprehensive tests
python tests/real_world_test.py

# Basic functionality test
python tests/demo_test.py
```

## 📚 Documentation Navigation

### **For New Users**
1. **[README.md](README.md)** - Start here for project overview
2. **[docs/guides/QUICKSTART.md](docs/guides/QUICKSTART.md)** - 5-minute setup guide
3. **[scripts/quick_setup.py](scripts/quick_setup.py)** - Automated setup

### **For Developers**
1. **[docs/guides/ARCHITECTURE.md](docs/guides/ARCHITECTURE.md)** - System design
2. **[docs/api/README.md](docs/api/README.md)** - API reference
3. **[docs/guides/COMPONENTS.md](docs/guides/COMPONENTS.md)** - Component details

### **For Integration**
1. **[examples/real_ai_integration.py](examples/real_ai_integration.py)** - Claude integration
2. **[examples/real_ai_integration_gemini.py](examples/real_ai_integration_gemini.py)** - Gemini integration
3. **[docs/api/README.md](docs/api/README.md)** - API documentation

## 🎮 Demo Categories

### **Memory Demonstrations**
- **`memory-test`** - Store data and test immediate recall
- **`cross-session`** - Memory across different sessions
- **`basic-memory`** - Basic storage and retrieval workflow

### **AI Integration Demos**
- **`claude-integration`** - Real Claude API with context
- **`gemini-integration`** - Real Gemini API with context
- **`api-test`** - Quick API connectivity test

### **Advanced Testing**
- **`random-test`** - Random scenario generation
- **Real-world tests** - Comprehensive system validation

## 🔧 Script Functions

### **Setup Scripts**
- **`quick_setup.py`** - Complete project initialization
- **`setup_api_keys.py`** - Interactive API key configuration
- **`test_my_keys.py`** - Validate API connectivity

### **Demo Management**
- **`run_demos.py`** - Unified demo launcher with:
  - List all available demos
  - Run specific demos by ID
  - Interactive selection menu
  - Prerequisite checking
  - Error handling and reporting

## 📁 File Organization Principles

### **Separation of Concerns**
- **`src/`** - Core implementation only
- **`demos/`** - User-facing demonstrations
- **`examples/`** - Integration examples
- **`scripts/`** - Utility and setup tools
- **`tests/`** - Testing and validation
- **`docs/`** - All documentation

### **Naming Conventions**
- **Scripts**: `verb_noun.py` (e.g., `setup_api_keys.py`)
- **Demos**: `descriptive_demo.py` (e.g., `memory_test_demo.py`)
- **Examples**: `real_ai_integration_provider.py`
- **Docs**: `UPPERCASE.md` for guides, `lowercase.md` for references

### **GitHub Ready**
- **`.gitignore`** - Comprehensive exclusions
- **`README.md`** - Professional project overview
- **`requirements.txt`** - All dependencies listed
- **`pyproject.toml`** - Modern Python project config

## 🎯 Usage Workflows

### **First-Time Setup**
```bash
git clone <repository>
cd myndai
python scripts/quick_setup.py
python scripts/setup_api_keys.py
python test_server.py
```

### **Running Demonstrations**
```bash
python scripts/run_demos.py --list
python scripts/run_demos.py --demo api-test
python scripts/run_demos.py --interactive
```

### **Development Workflow**
```bash
python test_server.py                    # Start server
python scripts/run_demos.py --check      # Verify setup
python examples/real_ai_integration.py   # Test integration
python tests/real_world_test.py          # Run tests
```

### **Documentation Workflow**
```bash
# Read overview
cat README.md

# Check quick start
cat docs/guides/QUICKSTART.md

# API reference
cat docs/api/README.md

# Architecture details
cat docs/guides/ARCHITECTURE.md
```

## 🔍 Finding Specific Information

| Need | Location |
|------|----------|
| **Project overview** | `README.md` |
| **Quick setup** | `scripts/quick_setup.py` |
| **API documentation** | `docs/api/README.md` |
| **System architecture** | `docs/guides/ARCHITECTURE.md` |
| **Demo examples** | `demos/` directory |
| **Integration examples** | `examples/` directory |
| **Troubleshooting** | `scripts/run_demos.py --check` |

## 🚀 Ready for GitHub

This structure is optimized for:
- ✅ **Professional presentation**
- ✅ **Easy navigation**
- ✅ **Clear documentation**
- ✅ **Automated setup**
- ✅ **Comprehensive testing**
- ✅ **Developer-friendly**

The project is now ready for GitHub upload with a clean, organized structure that makes it easy for users to understand, set up, and use Mynd. 
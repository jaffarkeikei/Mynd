#!/usr/bin/env python3
"""
Mynd Quick Setup
Get the project ready for GitHub and testing
"""
import sys
import subprocess
from pathlib import Path

def check_python_version():
    """Check if Python version is compatible"""
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print("❌ Python 3.8+ required")
        print(f"   Current version: {version.major}.{version.minor}.{version.micro}")
        return False
    print(f"✅ Python {version.major}.{version.minor}.{version.micro}")
    return True

def check_dependencies():
    """Check and install required dependencies"""
    print("🔍 Checking dependencies...")
    
    required_packages = [
        "fastapi",
        "uvicorn", 
        "chromadb",
        "anthropic",
        "google-generativeai",
        "python-dotenv",
        "requests"
    ]
    
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package.replace('-', '_'))
            print(f"✅ {package}")
        except ImportError:
            print(f"❌ {package}")
            missing_packages.append(package)
    
    if missing_packages:
        print(f"\n📦 Installing missing packages: {', '.join(missing_packages)}")
        try:
            subprocess.run([
                sys.executable, "-m", "pip", "install",
                "--break-system-packages"  # For macOS
            ] + missing_packages, check=True)
            print("✅ All dependencies installed")
        except subprocess.CalledProcessError:
            print("❌ Failed to install dependencies")
            print("💡 Try manually: pip install -r requirements.txt")
            return False
    
    return True

def setup_environment():
    """Set up environment files"""
    print("🔧 Setting up environment...")
    
    project_root = Path(__file__).parent.parent
    env_file = project_root / ".env"
    env_example = project_root / "scripts" / "env_example.txt"
    
    if not env_file.exists() and env_example.exists():
        print("📝 Creating .env file from template...")
        try:
            with open(env_example, 'r', encoding='utf-8') as f:
                content = f.read()
            
            with open(env_file, 'w', encoding='utf-8') as f:
                f.write(content)
            
            print("✅ .env file created")
            print("💡 Edit .env with your API keys: nano .env")
        except (OSError, IOError) as e:
            print(f"❌ Error creating .env file: {e}")
            return False
    elif env_file.exists():
        print("✅ .env file already exists")
    else:
        print("⚠️  env_example.txt not found")
        
    return True

def check_project_structure():
    """Verify project structure is correct"""
    print("📁 Checking project structure...")
    
    project_root = Path(__file__).parent.parent
    required_dirs = ["src", "demos", "examples", "scripts", "tests", "docs"]
    
    for dir_name in required_dirs:
        dir_path = project_root / dir_name
        if dir_path.exists():
            print(f"✅ {dir_name}/")
        else:
            print(f"❌ {dir_name}/ missing")
            try:
                dir_path.mkdir(exist_ok=True)
                print(f"   Created {dir_name}/")
            except OSError as e:
                print(f"   Failed to create {dir_name}/: {e}")
                return False
    
    return True

def test_basic_functionality():
    """Test basic system functionality"""
    print("🧪 Testing basic functionality...")
    
    try:
        # Test if test_server.py exists and is runnable
        project_root = Path(__file__).parent.parent
        test_server = project_root / "test_server.py"
        
        if test_server.exists():
            print("✅ test_server.py found")
        else:
            print("❌ test_server.py missing")
            return False
        
        # Test if we can import main modules
        sys.path.insert(0, str(project_root))
        
        try:
            import src.main  # Import to check availability without conflicting names
            del src.main  # Remove reference to avoid linter warning
            print("✅ Core modules importable")
        except ImportError as e:
            print(f"⚠️  Import warning: {e}")
        
        return True
        
    except (OSError, ImportError) as e:
        print(f"❌ Basic functionality test failed: {e}")
        return False

def display_next_steps():
    """Display next steps for the user"""
    print("\n🎉 Setup complete! Next steps:")
    print("=" * 40)
    print("1. Add your API keys:")
    print("   python scripts/setup_api_keys.py")
    print()
    print("2. Start the MCP server:")
    print("   python test_server.py")
    print()
    print("3. Run a demo:")
    print("   python scripts/run_demos.py --demo api-test")
    print()
    print("4. Explore all demos:")
    print("   python scripts/run_demos.py --list")
    print()
    print("5. Ready for GitHub:")
    print("   git init")
    print("   git add .")
    print("   git commit -m 'Initial Mynd implementation'")
    print()
    print("📚 Documentation: docs/guides/")
    print("🔧 Examples: examples/")
    print("🎮 Demos: demos/")

def run_setup():
    print("🧠 Mynd Quick Setup")
    print("=" * 30)
    
    success = True
    
    # Check Python version
    if not check_python_version():
        success = False
    
    # Check dependencies
    if success and not check_dependencies():
        success = False
    
    # Setup environment
    if success and not setup_environment():
        success = False
    
    # Check project structure
    if success and not check_project_structure():
        success = False
    
    # Test basic functionality
    if success and not test_basic_functionality():
        success = False
    
    if success:
        display_next_steps()
        print("\n✅ Setup successful!")
    else:
        print("\n❌ Setup had issues. Please check the errors above.")
        sys.exit(1)

if __name__ == "__main__":
    run_setup() 
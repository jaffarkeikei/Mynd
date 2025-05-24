#!/usr/bin/env python3
"""
Mynd Demo Launcher
Run various demonstrations of the AI memory system
"""
import sys
import subprocess
import argparse
from pathlib import Path

# Add project root to Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

class DemoLauncher:
    """Launcher for Mynd demonstrations"""
    
    def __init__(self):
        self.project_root = project_root
        self.demos_dir = self.project_root / "demos"
        self.examples_dir = self.project_root / "examples"
        self.scripts_dir = self.project_root / "scripts"
        
        self.available_demos = {
            "memory-test": {
                "file": "practical_memory_test.py",
                "description": "Store new data and test AI recall immediately",
                "directory": "demos"
            },
            "cross-session": {
                "file": "cross_session_demo.py", 
                "description": "Show how AI memory works across different sessions",
                "directory": "demos"
            },
            "random-test": {
                "file": "random_ai_test.py",
                "description": "Test with completely random AI scenarios",
                "directory": "demos"
            },
            "basic-memory": {
                "file": "memory_test_example.py",
                "description": "Basic memory storage and retrieval workflow",
                "directory": "demos"
            },
            "claude-integration": {
                "file": "real_ai_integration.py",
                "description": "Real Claude API integration with project context",
                "directory": "examples"
            },
            "gemini-integration": {
                "file": "real_ai_integration_gemini.py", 
                "description": "Real Gemini API integration with project context",
                "directory": "examples"
            },
            "api-test": {
                "file": "test_my_keys.py",
                "description": "Test API keys and run quick integration demo",
                "directory": "scripts"
            }
        }

    def list_demos(self):
        """List all available demonstrations"""
        print("🧠 Available Mynd Demonstrations")
        print("=" * 50)
        
        for demo_id, demo_info in self.available_demos.items():
            print(f"📍 {demo_id}")
            print(f"   {demo_info['description']}")
            print(f"   Location: {demo_info['directory']}/{demo_info['file']}")
            print()

    def check_prerequisites(self):
        """Check if system is ready for demos"""
        print("🔍 Checking prerequisites...")
        
        # Check if MCP server is running
        try:
            import requests
            response = requests.get("http://localhost:8080", timeout=2)
            if response.status_code == 200:
                print("✅ MCP server is running")
            else:
                print("⚠️  MCP server responding but not ready")
                return False
        except (ImportError, requests.RequestException, requests.Timeout):
            print("❌ MCP server not running")
            print("💡 Start with: python test_server.py")
            return False
        
        # Check for .env file
        env_file = self.project_root / ".env"
        if env_file.exists():
            print("✅ Environment file found")
        else:
            print("⚠️  No .env file found")
            print("💡 Run: python scripts/setup_api_keys.py")
        
        # Check dependencies
        try:
            __import__('anthropic')
            print("✅ Anthropic library available")
        except ImportError:
            print("⚠️  Anthropic library not installed")
        
        try:
            __import__('google.generativeai')
            print("✅ Google AI library available")
        except ImportError:
            print("⚠️  Google AI library not installed")
        
        return True

    def run_demo(self, demo_id: str):
        """Run a specific demonstration"""
        if demo_id not in self.available_demos:
            print(f"❌ Demo '{demo_id}' not found")
            self.list_demos()
            return False
        
        demo_info = self.available_demos[demo_id]
        demo_file = getattr(self, f"{demo_info['directory']}_dir") / demo_info["file"]
        
        if not demo_file.exists():
            print(f"❌ Demo file not found: {demo_file}")
            return False
        
        print(f"🚀 Starting demo: {demo_id}")
        print(f"📝 Description: {demo_info['description']}")
        print("-" * 50)
        
        try:
            # Run the demo
            result = subprocess.run(
                [sys.executable, str(demo_file)],
                cwd=str(self.project_root),
                check=False
            )
            
            if result.returncode == 0:
                print(f"\n✅ Demo '{demo_id}' completed successfully!")
            else:
                print(f"\n❌ Demo '{demo_id}' exited with code {result.returncode}")
            
            return result.returncode == 0
            
        except KeyboardInterrupt:
            print(f"\n⏹️  Demo '{demo_id}' interrupted by user")
            return False
        except (OSError, subprocess.SubprocessError) as e:
            print(f"\n❌ Error running demo '{demo_id}': {e}")
            return False

    def run_interactive_mode(self):
        """Run in interactive mode to choose demos"""
        print("🧠 Mynd Interactive Demo Launcher")
        print("=" * 40)
        
        while True:
            print("\nAvailable options:")
            print("1. List all demos")
            print("2. Check prerequisites") 
            print("3. Run a demo")
            print("4. Exit")
            
            choice = input("\nChoose an option (1-4): ").strip()
            
            if choice == "1":
                self.list_demos()
            elif choice == "2":
                self.check_prerequisites()
            elif choice == "3":
                self.list_demos()
                demo_id = input("Enter demo ID to run: ").strip()
                if demo_id:
                    self.run_demo(demo_id)
            elif choice == "4":
                print("👋 Goodbye!")
                break
            else:
                print("❌ Invalid choice. Please select 1-4.")

def main():
    parser = argparse.ArgumentParser(
        description="Mynd Demo Launcher",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python scripts/run_demos.py --list
  python scripts/run_demos.py --demo memory-test
  python scripts/run_demos.py --check
  python scripts/run_demos.py --interactive
        """
    )
    
    parser.add_argument(
        "--demo", 
        help="Run a specific demo by ID"
    )
    parser.add_argument(
        "--list", 
        action="store_true",
        help="List all available demos"
    )
    parser.add_argument(
        "--check", 
        action="store_true",
        help="Check prerequisites for running demos"
    )
    parser.add_argument(
        "--interactive", 
        action="store_true",
        help="Run in interactive mode"
    )
    
    args = parser.parse_args()
    launcher = DemoLauncher()
    
    if args.list:
        launcher.list_demos()
    elif args.check:
        launcher.check_prerequisites()
    elif args.demo:
        if not launcher.check_prerequisites():
            print("\n⚠️  Prerequisites not met. Please fix issues above.")
            sys.exit(1)
        success = launcher.run_demo(args.demo)
        sys.exit(0 if success else 1)
    elif args.interactive:
        launcher.run_interactive_mode()
    else:
        # Default: show help and available demos
        parser.print_help()
        print("\n")
        launcher.list_demos()

if __name__ == "__main__":
    main() 
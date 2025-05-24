#!/usr/bin/env python3
"""
Mynd Demo Launcher - Comprehensive Test & Demo Suite
Win the hackathon with impressive demonstrations!
"""
import sys
import subprocess
import argparse
from pathlib import Path
import time
from typing import List, Tuple

# Add project root to Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

class DemoLauncher:
    """Enhanced launcher for Mynd demonstrations and tests"""
    
    def __init__(self):
        self.project_root = project_root
        self.demos_dir = self.project_root / "demos"
        self.examples_dir = self.project_root / "examples"
        self.scripts_dir = self.project_root / "scripts"
        self.tests_dir = self.project_root / "tests"
        
        # Organized demo categories for hackathon
        self.demo_categories = {
            "🧠 Core Memory Demos": {
                "memory-test": {
                    "file": "practical_memory_test.py",
                    "description": "Store new data and test AI recall immediately",
                    "directory": "demos",
                    "time": "2 min",
                    "impact": "Shows instant memory retention"
                },
                "cross-session": {
                    "file": "cross_session_demo.py", 
                    "description": "Show how AI memory works across different sessions",
                    "directory": "demos",
                    "time": "3 min",
                    "impact": "Demonstrates persistent memory"
                },
                "basic-memory": {
                    "file": "memory_test_example.py",
                    "description": "Basic memory storage and retrieval workflow",
                    "directory": "demos",
                    "time": "2 min",
                    "impact": "Foundation demo"
                }
            },
            "🌐 Web Interface": {
                "web-app": {
                    "file": "web_app.py",
                    "description": "Beautiful ChatGPT-like web interface with memory toggle (BEST FOR JUDGES!)",
                    "directory": "src",
                    "time": "5 min",
                    "impact": "Visual wow factor - side-by-side comparison!"
                }
            },
            "🤖 AI Integration Tests": {
                "claude-integration": {
                    "file": "real_ai_integration.py",
                    "description": "Real Claude API integration with project context",
                    "directory": "examples",
                    "time": "3 min",
                    "impact": "Shows real AI enhancement"
                },
                "gemini-integration": {
                    "file": "real_ai_integration_gemini.py", 
                    "description": "Real Gemini API integration with project context",
                    "directory": "examples",
                    "time": "3 min",
                    "impact": "Multi-AI compatibility"
                },
                "api-test": {
                    "file": "test_my_keys.py",
                    "description": "Test API keys and run quick integration demo",
                    "directory": "scripts",
                    "time": "1 min",
                    "impact": "Quick validation"
                }
            },
            "🚀 Comprehensive Tests": {
                "real-world-demo": {
                    "file": "real_world_demo.py",
                    "description": "Complete real-world usage scenarios (BEST FOR HACKATHON)",
                    "directory": "tests",
                    "time": "5 min",
                    "impact": "Shows all features in action"
                },
                "real-world-test": {
                    "file": "real_world_test.py",
                    "description": "Comprehensive system test with performance metrics",
                    "directory": "tests",
                    "time": "4 min",
                    "impact": "Proves system robustness"
                },
                "demo-test": {
                    "file": "demo_test.py",
                    "description": "Complete API endpoint and functionality test",
                    "directory": "tests",
                    "time": "2 min",
                    "impact": "Technical validation"
                },
                "mcp-test": {
                    "file": "test_mcp.py",
                    "description": "Test Model Context Protocol server",
                    "directory": "tests",
                    "time": "2 min",
                    "impact": "MCP compliance check"
                },
                "claude-test": {
                    "file": "test_claude_integration.py",
                    "description": "Detailed Claude + Mynd integration test",
                    "directory": "tests",
                    "time": "3 min",
                    "impact": "AI enhancement validation"
                }
            },
            "🎲 Advanced Demos": {
                "random-test": {
                    "file": "random_ai_test.py",
                    "description": "Test with completely random AI scenarios",
                    "directory": "demos",
                    "time": "3 min",
                    "impact": "Shows adaptability"
                }
            }
        }
        
        # Flatten for backward compatibility
        self.available_demos = {}
        for demos in self.demo_categories.values():
            self.available_demos.update(demos)

    def list_demos(self, category_filter: str = None):
        """List all available demonstrations with categories"""
        print("🧠 Mynd Demo & Test Suite - Win the Hackathon!")
        print("=" * 70)
        
        for category, demos in self.demo_categories.items():
            if category_filter and category_filter.lower() not in category.lower():
                continue
                
            print(f"\n{category}")
            print("-" * len(category))
            
            for demo_id, demo_info in demos.items():
                print(f"\n📍 {demo_id}")
                print(f"   {demo_info['description']}")
                print(f"   ⏱️  Duration: {demo_info['time']} | 🎯 Impact: {demo_info['impact']}")
                print(f"   📂 Location: {demo_info['directory']}/{demo_info['file']}")

    def check_prerequisites(self) -> Tuple[bool, List[str]]:
        """Enhanced prerequisite checking with detailed feedback"""
        print("🔍 Checking prerequisites...")
        issues = []
        warnings = []
        
        # Check Python version
        python_version = sys.version_info
        if python_version.major == 3 and python_version.minor >= 9:
            print("✅ Python version OK")
        else:
            issues.append(f"Python 3.9+ required (found {python_version.major}.{python_version.minor})")
        
        # Check if MCP server could be running
        try:
            import requests
            # Try multiple common ports
            server_found = False
            for port in [8080, 8765, 3000]:
                try:
                    response = requests.get(f"http://localhost:{port}", timeout=1)
                    if response.status_code == 200:
                        print(f"✅ Server found on port {port}")
                        server_found = True
                        break
                except Exception:
                    continue
            
            if not server_found:
                warnings.append("MCP server not running (start with: python -m src.mcp_server)")
        except ImportError:
            issues.append("requests library not installed")
        
        # Check for .env file
        env_file = self.project_root / ".env"
        if env_file.exists():
            print("✅ Environment file found")
        else:
            warnings.append("No .env file (run: python scripts/setup_api_keys.py)")
        
        # Check critical dependencies
        try:
            __import__('anthropic')
            print("✅ Anthropic library available")
        except ImportError:
            warnings.append("Anthropic library not installed (for Claude demos)")
        
        try:
            __import__('google.generativeai')
            print("✅ Google AI library available")
        except ImportError:
            warnings.append("Google AI library not installed (for Gemini demos)")
        
        try:
            __import__('chromadb')
            print("✅ ChromaDB available")
        except ImportError:
            issues.append("ChromaDB not installed (core dependency)")
        
        # Check Ollama for local LLM
        try:
            result = subprocess.run(['ollama', 'list'], capture_output=True, text=True, check=False)
            if result.returncode == 0:
                print("✅ Ollama installed")
            else:
                warnings.append("Ollama not running (needed for semantic extraction)")
        except (OSError, subprocess.SubprocessError):
            warnings.append("Ollama not found (install from ollama.ai)")
        
        # Summary
        if issues:
            print(f"\n❌ {len(issues)} critical issues found:")
            for issue in issues:
                print(f"   • {issue}")
        
        if warnings:
            print(f"\n⚠️  {len(warnings)} warnings:")
            for warning in warnings:
                print(f"   • {warning}")
        
        return len(issues) == 0, warnings

    def run_demo(self, demo_id: str) -> bool:
        """Enhanced demo runner with timing and better output"""
        if demo_id not in self.available_demos:
            print(f"❌ Demo '{demo_id}' not found")
            self.list_demos()
            return False
        
        demo_info = self.available_demos[demo_id]
        demo_file = getattr(self, f"{demo_info['directory']}_dir") / demo_info["file"]
        
        if not demo_file.exists():
            print(f"❌ Demo file not found: {demo_file}")
            return False
        
        print(f"\n{'='*70}")
        print(f"🚀 Starting: {demo_id}")
        print(f"📝 {demo_info['description']}")
        print(f"⏱️  Expected duration: {demo_info['time']}")
        print(f"🎯 Impact: {demo_info['impact']}")
        print(f"{'='*70}\n")
        
        start_time = time.time()
        
        try:
            # Run the demo
            result = subprocess.run(
                [sys.executable, str(demo_file)],
                cwd=str(self.project_root),
                check=False
            )
            
            elapsed_time = time.time() - start_time
            
            if result.returncode == 0:
                print(f"\n{'='*70}")
                print(f"✅ Demo '{demo_id}' completed successfully!")
                print(f"⏱️  Actual duration: {elapsed_time:.1f} seconds")
                print(f"{'='*70}")
            else:
                print(f"\n❌ Demo '{demo_id}' exited with code {result.returncode}")
            
            return result.returncode == 0
            
        except KeyboardInterrupt:
            print(f"\n⏹️  Demo '{demo_id}' interrupted by user")
            return False
        except (OSError, subprocess.SubprocessError) as e:
            print(f"\n❌ Error running demo '{demo_id}': {e}")
            return False

    def run_hackathon_sequence(self):
        """Run the best sequence of demos for hackathon judges"""
        print("🏆 HACKATHON DEMO SEQUENCE")
        print("=" * 70)
        print("Running the most impressive demos in optimal order...\n")
        
        # Optimal demo sequence for judges - NOW WITH WEB APP!
        demo_sequence = [
            ("api-test", "Quick validation that everything works"),
            ("web-app", "🌟 VISUAL WOW - ChatGPT-like interface with memory toggle!"),
            ("real-world-demo", "Complete real-world scenarios"),
            ("claude-integration", "Live AI enhancement demo")
        ]
        
        print("📋 Demo sequence:")
        for i, (demo_id, reason) in enumerate(demo_sequence, 1):
            print(f"   {i}. {demo_id}: {reason}")
        
        input("\n🎬 Press Enter to start the hackathon demo sequence...")
        
        results = []
        for demo_id, reason in demo_sequence:
            print(f"\n{'='*70}")
            print(f"🎯 Demo {len(results)+1}/{len(demo_sequence)}: {reason}")
            print(f"{'='*70}")
            
            if demo_id == "web-app":
                print("\n🌐 Starting web interface...")
                print("📍 Open http://localhost:8000 in your browser")
                print("🎪 Show the judges:")
                print("   1. Toggle memory ON/OFF to see the difference")
                print("   2. Try 'Side-by-Side Comparison' mode")
                print("   3. Load demo data and ask about authentication")
                print("\n⏸️  Press Enter when ready to continue...")
                input()
                success = True
            else:
                success = self.run_demo(demo_id)
            
            results.append((demo_id, success))
            
            if success and len(results) < len(demo_sequence):
                input("\n➡️  Press Enter for next demo...")
        
        # Summary
        print("\n🏁 HACKATHON DEMO COMPLETE")
        print("=" * 70)
        successful = sum(1 for _, success in results if success)
        print(f"✅ {successful}/{len(results)} demos completed successfully")
        
        if successful == len(results):
            print("\n🎉 Perfect run! Ready to win the hackathon!")
        else:
            print("\n⚠️  Some demos had issues. Run with --check to diagnose.")

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
        description="Mynd Demo Launcher - Comprehensive Test Suite",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python scripts/run_demos.py --list                    # List all demos
  python scripts/run_demos.py --demo real-world-demo    # Run best demo
  python scripts/run_demos.py --hackathon              # Run hackathon sequence
  python scripts/run_demos.py --category "AI Integration"  # List category
  python scripts/run_demos.py --check                   # Check prerequisites
  python scripts/run_demos.py --interactive            # Interactive mode
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
        "--category",
        help="Filter demos by category"
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
    parser.add_argument(
        "--hackathon",
        action="store_true",
        help="Run the optimal hackathon demo sequence"
    )
    
    args = parser.parse_args()
    launcher = DemoLauncher()
    
    if args.list:
        launcher.list_demos(args.category)
    elif args.check:
        ready, warnings = launcher.check_prerequisites()
        if ready:
            print("\n✅ System ready for demos!")
        else:
            print("\n❌ Please fix critical issues before running demos.")
    elif args.hackathon:
        ready, _ = launcher.check_prerequisites()
        if not ready:
            print("\n⚠️  Prerequisites not met. Please fix issues above.")
            sys.exit(1)
        launcher.run_hackathon_sequence()
    elif args.demo:
        ready, _ = launcher.check_prerequisites()
        if not ready and args.demo not in ['api-test', 'demo-test']:
            print("\n⚠️  Prerequisites not met. Some demos may fail.")
        success = launcher.run_demo(args.demo)
        sys.exit(0 if success else 1)
    elif args.interactive:
        launcher.run_interactive_mode()
    else:
        # Default: show help and highlight best demos
        parser.print_help()
        print("\n")
        print("🏆 RECOMMENDED FOR HACKATHON:")
        print("   python scripts/run_demos.py --hackathon")
        print("\n🚀 BEST INDIVIDUAL DEMOS:")
        print("   python scripts/run_demos.py --demo real-world-demo")
        print("   python scripts/run_demos.py --demo memory-test")
        print("   python scripts/run_demos.py --demo claude-integration")

if __name__ == "__main__":
    main() 
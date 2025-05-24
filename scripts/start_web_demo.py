#!/usr/bin/env python3
"""
Quick start script for Mynd Web Demo
Starts both MCP server and web interface for hackathon presentation
"""
import subprocess
import time
import webbrowser
import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

def main():
    print("🚀 Starting Mynd Web Demo for Hackathon")
    print("=" * 50)
    
    # Start MCP server in background
    print("📡 Starting MCP server...")
    mcp_process = subprocess.Popen(
        [sys.executable, "-m", "src.mcp_server"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    
    # Give MCP server time to start
    time.sleep(2)
    
    # Start web app
    print("🌐 Starting web interface...")
    print("📍 Opening http://localhost:8000 in your browser...")
    
    # Open browser after a short delay
    time.sleep(1)
    webbrowser.open("http://localhost:8000")
    
    print("\n✅ Demo ready!")
    print("\n📋 Quick Demo Script:")
    print("1. Click 'Load Demo Context' button")
    print("2. Ask: 'What was our authentication decision?'")
    print("3. Toggle Memory OFF and ask again")
    print("4. Try 'Side-by-Side Comparison' mode")
    print("5. Show real-time stats on the left")
    print("\n🛑 Press Ctrl+C to stop all services")
    
    try:
        # Run web app (this blocks)
        subprocess.run([sys.executable, "src/web_app.py"])
    except KeyboardInterrupt:
        print("\n\n👋 Shutting down demo...")
        mcp_process.terminate()
        print("✅ Demo stopped")

if __name__ == "__main__":
    main() 
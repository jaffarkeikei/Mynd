#!/usr/bin/env python3
"""
Test script to verify Mynd web app is working
"""
import subprocess
import time
import requests
import sys

def test_web_app():
    print("🧪 Testing Mynd Web App Setup")
    print("=" * 50)
    
    # Test 1: Check if FastAPI is installed
    print("\n1️⃣ Checking dependencies...")
    try:
        import fastapi
        import uvicorn
        import pydantic
        print("✅ FastAPI dependencies installed")
    except ImportError as e:
        print(f"❌ Missing dependency: {e}")
        print("   Run: pip install fastapi uvicorn pydantic")
        return False
    
    # Test 2: Try to import the web app
    print("\n2️⃣ Testing web app import...")
    try:
        sys.path.insert(0, '..')
        from src.web_app import app
        print("✅ Web app module loads successfully")
    except Exception as e:
        print(f"❌ Failed to import web app: {e}")
        return False
    
    # Test 3: Start the web server
    print("\n3️⃣ Starting web server...")
    print("   This will start the server on http://localhost:8000")
    print("   Press Ctrl+C to stop\n")
    
    try:
        # Run the web app
        subprocess.run([sys.executable, "src/web_app.py"])
    except KeyboardInterrupt:
        print("\n✅ Server stopped by user")
    except Exception as e:
        print(f"❌ Error running server: {e}")
        return False
    
    return True

if __name__ == "__main__":
    print("🚀 Mynd Web App Test")
    print("This will verify your web interface is working\n")
    
    if test_web_app():
        print("\n✅ Web app test completed!")
    else:
        print("\n❌ Web app test failed - check errors above") 
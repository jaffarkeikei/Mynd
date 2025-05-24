#!/usr/bin/env python3
"""
Simple test script to verify Claude integration with Mynd
Tests both the local Mynd functionality and Claude API access
"""

import os
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from src.main import Mynd
from src.models import SemanticEvent

# Test Claude API
try:
    import anthropic
    claude_available = bool(os.getenv('ANTHROPIC_API_KEY'))
except ImportError:
    claude_available = False
    anthropic = None

def test_mynd_local():
    """Test local Mynd functionality"""
    print("🧠 Testing Mynd Local Functionality")
    print("=" * 60)
    
    # Initialize Mynd
    mynd = Mynd()
    print("✅ Mynd initialized successfully")
    
    # Get stats
    stats = mynd.db.get_stats()
    print(f"📊 Database stats: {stats['total_events']} events captured")
    
    # Query for authentication context
    print("\n🔍 Testing semantic search...")
    context = mynd.get_context_for_query("authentication architecture", max_tokens=500)
    
    if context:
        print("✅ Found relevant context:")
        print("-" * 40)
        print(context[:300] + "..." if len(context) > 300 else context)
        print("-" * 40)
    else:
        print("⚠️  No context found for query")
    
    return True

def test_claude_api():
    """Test Claude API access"""
    print("\n🤖 Testing Claude API Integration")
    print("=" * 60)
    
    if not claude_available:
        print("❌ Claude not available:")
        if not anthropic:
            print("   - anthropic library not installed")
        if not os.getenv('ANTHROPIC_API_KEY'):
            print("   - ANTHROPIC_API_KEY not set")
        return False
    
    try:
        # Initialize Claude client
        client = anthropic.Anthropic(api_key=os.getenv('ANTHROPIC_API_KEY'))
        print("✅ Claude client initialized")
        
        # Test simple API call
        print("📡 Testing API connection...")
        response = client.messages.create(
            model="claude-3-haiku-20240307",
            max_tokens=100,
            messages=[
                {"role": "user", "content": "Say 'Hello from Mynd!' if you can hear me."}
            ]
        )
        
        print(f"✅ Claude response: {response.content[0].text}")
        return True
        
    except Exception as e:
        print(f"❌ Claude API error: {e}")
        return False

def test_mynd_with_claude():
    """Test Claude with Mynd context"""
    print("\n🎯 Testing Claude + Mynd Integration")
    print("=" * 60)
    
    if not claude_available:
        print("⚠️  Skipping integration test (Claude not available)")
        return False
    
    try:
        # Get context from Mynd
        mynd = Mynd()
        context = mynd.get_context_for_query("authentication architecture", max_tokens=500)
        
        if not context:
            print("⚠️  No context found in Mynd")
            return False
        
        # Send to Claude with context
        client = anthropic.Anthropic(api_key=os.getenv('ANTHROPIC_API_KEY'))
        
        prompt = f"""Based on the following project context from my memory system:

{context}

What authentication approach did we decide on and why?"""
        
        print("📡 Asking Claude with Mynd context...")
        response = client.messages.create(
            model="claude-3-haiku-20240307",
            max_tokens=300,
            messages=[
                {"role": "user", "content": prompt}
            ]
        )
        
        print("\n✅ Claude's context-aware response:")
        print("-" * 40)
        print(response.content[0].text)
        print("-" * 40)
        
        return True
        
    except Exception as e:
        print(f"❌ Integration error: {e}")
        return False

def main():
    """Run all tests"""
    print("🚀 Mynd + Claude Integration Test")
    print("=" * 60)
    print(f"📍 Working directory: {os.getcwd()}")
    print(f"🔑 ANTHROPIC_API_KEY: {'✅ Set' if os.getenv('ANTHROPIC_API_KEY') else '❌ Not set'}")
    print(f"📦 anthropic library: {'✅ Installed' if anthropic else '❌ Not installed'}")
    print()
    
    # Run tests
    results = []
    
    # Test 1: Local Mynd
    try:
        results.append(("Mynd Local", test_mynd_local()))
    except Exception as e:
        print(f"❌ Mynd local test failed: {e}")
        results.append(("Mynd Local", False))
    
    # Test 2: Claude API
    try:
        results.append(("Claude API", test_claude_api()))
    except Exception as e:
        print(f"❌ Claude API test failed: {e}")
        results.append(("Claude API", False))
    
    # Test 3: Integration
    try:
        results.append(("Integration", test_mynd_with_claude()))
    except Exception as e:
        print(f"❌ Integration test failed: {e}")
        results.append(("Integration", False))
    
    # Summary
    print("\n📊 Test Summary")
    print("=" * 60)
    for test_name, passed in results:
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"{test_name:.<40} {status}")
    
    all_passed = all(result[1] for result in results)
    print("\n" + ("🎉 All tests passed!" if all_passed else "⚠️  Some tests failed"))
    
    return all_passed

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 
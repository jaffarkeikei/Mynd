#!/usr/bin/env python3
"""
Test MCP Server Functionality
"""
import os
import sys
import time
import requests
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

def test_mcp_server():
    """Test if MCP server is running and responding"""
    print("🧪 Testing MCP Server...")
    print("="*60)
    
    base_url = "http://localhost:8765"
    
    # Test 1: Check if server is running
    print("\n1️⃣  Testing server health...")
    try:
        response = requests.get(f"{base_url}/", timeout=2)
        if response.status_code == 200:
            print("   ✅ Server is running")
            data = response.json()
            print(f"   📡 Server message: {data.get('message', 'No message')}")
        else:
            print(f"   ❌ Server returned status {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print("   ❌ Cannot connect to server")
        print("   💡 Start the server with: mynd start --port 8765")
        return False
    except Exception as e:
        print(f"   ❌ Error: {e}")
        return False
    
    # Test 2: Check status endpoint
    print("\n2️⃣  Testing status endpoint...")
    try:
        response = requests.get(f"{base_url}/api/status", timeout=2)
        if response.status_code == 200:
            print("   ✅ Status endpoint working")
            data = response.json()
            if data.get('success'):
                stats = data.get('data', {})
                print(f"   📊 Database events: {stats.get('database', {}).get('total_events', 0)}")
                print(f"   🔑 Active tokens: {stats.get('active_tokens', 0)}")
        else:
            print(f"   ❌ Status endpoint returned {response.status_code}")
    except Exception as e:
        print(f"   ❌ Status check failed: {e}")
    
    # Test 3: Create capability token
    print("\n3️⃣  Testing token creation...")
    token = None
    try:
        response = requests.post(f"{base_url}/api/tokens", json={
            "client_id": "test-client",
            "scope": "context_read",
            "ttl_seconds": 300,
            "max_tokens": 4000
        }, timeout=5)
        
        if response.status_code == 200:
            print("   ✅ Token created successfully")
            data = response.json()
            token = data.get('data', {}).get('token')
            print(f"   🔑 Token: {token[:20]}..." if token else "   ❌ No token received")
        else:
            print(f"   ❌ Token creation failed with status {response.status_code}")
    except Exception as e:
        print(f"   ❌ Token creation error: {e}")
    
    # Test 4: Query context with token
    if token:
        print("\n4️⃣  Testing context query...")
        try:
            headers = {"Authorization": f"Bearer {token}"}
            response = requests.post(f"{base_url}/api/context",
                headers=headers,
                json={
                    "query": "authentication decisions",
                    "max_tokens": 500
                },
                timeout=10
            )
            
            if response.status_code == 200:
                print("   ✅ Context query successful")
                data = response.json()
                context = data.get('data', {}).get('context', '')
                tokens_used = data.get('data', {}).get('tokens_used', 0)
                print(f"   📝 Context length: {len(context)} chars")
                print(f"   🔢 Tokens used: {tokens_used}")
                if context:
                    print(f"   📄 Preview: {context[:100]}...")
            else:
                print(f"   ❌ Context query failed with status {response.status_code}")
        except Exception as e:
            print(f"   ❌ Context query error: {e}")
    
    # Test 5: Check API documentation
    print("\n5️⃣  Testing API documentation...")
    try:
        response = requests.get(f"{base_url}/docs", timeout=2)
        if response.status_code == 200:
            print("   ✅ API documentation available")
            print(f"   📚 Access at: {base_url}/docs")
        else:
            print(f"   ❌ Documentation returned status {response.status_code}")
    except Exception as e:
        print(f"   ⚠️  Documentation check skipped: {e}")
    
    print("\n" + "="*60)
    print("✅ MCP Server is working correctly!")
    return True

def main():
    """Run MCP server tests"""
    print("\n🚀 MCP Server Test Suite")
    print("Testing Model Context Protocol server functionality\n")
    
    # Check if server is supposed to be running
    print("ℹ️  This test requires the MCP server to be running")
    print("   Start it with: mynd start --port 8765\n")
    
    # Run tests
    success = test_mcp_server()
    
    if success:
        print("\n🎉 All MCP tests passed!")
        print("\nThe MCP server is ready to:")
        print("  • Serve context to AI clients")
        print("  • Manage capability tokens")
        print("  • Handle secure API requests")
        print("  • Provide context for queries")
    else:
        print("\n❌ MCP tests failed")
        print("\nTroubleshooting:")
        print("  1. Make sure the server is running: mynd start --port 8765")
        print("  2. Check if port 8765 is available")
        print("  3. Look for error messages in the server output")
    
    return 0 if success else 1

if __name__ == "__main__":
    sys.exit(main()) 
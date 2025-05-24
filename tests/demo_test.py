#!/usr/bin/env python3
"""
Comprehensive demo test for Mynd
Tests all functionality including CLI, MCP server, and API endpoints
"""
import requests
import json
import time
import subprocess
import sys

def test_api_endpoint(url, method="GET", headers=None, data=None):
    """Test an API endpoint and return the response"""
    try:
        if method == "GET":
            response = requests.get(url, headers=headers, timeout=5)
        elif method == "POST":
            response = requests.post(url, headers=headers, json=data, timeout=5)
        elif method == "DELETE":
            response = requests.delete(url, headers=headers, timeout=5)
        
        return response.status_code, response.json() if response.content else {}
    except Exception as e:
        return None, str(e)

def main():
    print("🧠 Mynd Comprehensive Demo Test")
    print("=" * 50)
    
    # Test 1: Check if MCP server is running
    print("\n1. Testing MCP Server Status...")
    status_code, response = test_api_endpoint("http://localhost:8080/")
    if status_code == 200:
        print("✅ MCP Server is running")
        print(f"   Response: {response}")
    else:
        print("❌ MCP Server is not running")
        print("   Please start the server first: python test_server.py")
        return
    
    # Test 2: Get server statistics
    print("\n2. Testing Server Statistics...")
    status_code, response = test_api_endpoint("http://localhost:8080/api/status")
    if status_code == 200:
        print("✅ Server statistics retrieved")
        data = response.get('data', {})
        print(f"   Total events: {data.get('database', {}).get('total_events', 0)}")
        print(f"   Vector store: {data.get('vector_store', {}).get('total_vectors', 0)} vectors")
        print(f"   Active tokens: {data.get('active_tokens', 0)}")
    else:
        print(f"❌ Failed to get statistics: {response}")
    
    # Test 3: Create capability token
    print("\n3. Testing Token Creation...")
    token_data = {
        "client_id": "demo-client",
        "scope": "context_read",
        "ttl_seconds": 3600,
        "max_tokens": 4000
    }
    status_code, response = test_api_endpoint(
        "http://localhost:8080/api/tokens",
        method="POST",
        data=token_data
    )
    
    if status_code == 200:
        print("✅ Capability token created")
        token = response.get('data', {}).get('token')
        print(f"   Token: {token[:20]}...")
        print(f"   Expires: {response.get('data', {}).get('expires_at')}")
    else:
        print(f"❌ Failed to create token: {response}")
        return
    
    # Test 4: Query context with token
    print("\n4. Testing Context Retrieval...")
    headers = {"Authorization": f"Bearer {token}"}
    query_data = {
        "query": "JWT authentication architecture",
        "max_tokens": 2000
    }
    status_code, response = test_api_endpoint(
        "http://localhost:8080/api/context",
        method="POST",
        headers=headers,
        data=query_data
    )
    
    if status_code == 200:
        print("✅ Context retrieved successfully")
        data = response.get('data', {})
        print(f"   Tokens used: {data.get('tokens_used', 0)}")
        context = data.get('context', '')
        print(f"   Context preview: {context[:200]}...")
    else:
        print(f"❌ Failed to retrieve context: {response}")
    
    # Test 5: Test CLI functionality
    print("\n5. Testing CLI Functionality...")
    try:
        # Test CLI status
        result = subprocess.run(
            [sys.executable, "-m", "src.cli", "status"],
            capture_output=True,
            text=True,
            timeout=10
        )
        if result.returncode == 0:
            print("✅ CLI status command works")
        else:
            print(f"❌ CLI status failed: {result.stderr}")
        
        # Test CLI query
        result = subprocess.run(
            [sys.executable, "-m", "src.cli", "query", "authentication"],
            capture_output=True,
            text=True,
            timeout=10
        )
        if result.returncode == 0:
            print("✅ CLI query command works")
        else:
            print(f"❌ CLI query failed: {result.stderr}")
            
    except Exception as e:
        print(f"❌ CLI test failed: {e}")
    
    # Test 6: Test search endpoint
    print("\n6. Testing Search Endpoint...")
    status_code, response = test_api_endpoint(
        "http://localhost:8080/api/search/mobile%20authentication",
        headers=headers
    )
    
    if status_code == 200:
        print("✅ Search endpoint works")
        data = response.get('data', {})
        print(f"   Found context with {data.get('tokens_used', 0)} tokens")
    else:
        print(f"❌ Search endpoint failed: {response}")
    
    print("\n🎉 Demo Test Complete!")
    print("\n📚 Available Endpoints:")
    print("   • http://localhost:8080/ - Root endpoint")
    print("   • http://localhost:8080/api/status - Server status")
    print("   • http://localhost:8080/api/tokens - Create tokens")
    print("   • http://localhost:8080/api/context - Get context")
    print("   • http://localhost:8080/api/search/{query} - Search context")
    print("   • http://localhost:8080/docs - API documentation")
    
    print("\n🔧 CLI Commands:")
    print("   • python -m src.cli status - Show status")
    print("   • python -m src.cli query 'text' - Query context")
    print("   • python -m src.cli demo - Create demo data")
    print("   • python -m src.cli start - Start full system")

if __name__ == "__main__":
    main() 
#!/usr/bin/env python3
"""
Test the Mynd memory storage and retrieval system
"""
import requests
import time

BASE_URL = "http://localhost:8000"

def test_memory_system():
    print("🧪 Testing Mynd Memory System")
    print("=" * 50)
    
    # Test 1: Store some information
    print("\n1️⃣ Storing new information...")
    test_messages = [
        "My favorite programming language is Python because of its simplicity and vast ecosystem.",
        "I'm working on a project called DataViz Pro that visualizes complex datasets using D3.js.",
        "The project deadline is December 15th, 2024 and we need to deliver three main features.",
        "Our tech stack includes React, Node.js, PostgreSQL, and Redis for caching."
    ]
    
    for msg in test_messages:
        response = requests.post(f"{BASE_URL}/api/chat", json={
            "message": msg,
            "use_memory": True
        })
        print(f"  Stored: {msg[:50]}...")
        time.sleep(0.5)
    
    # Test 2: Retrieve information
    print("\n2️⃣ Testing memory retrieval...")
    queries = [
        "What's my favorite programming language?",
        "What project am I working on?",
        "When is the project deadline?",
        "What database are we using?"
    ]
    
    for query in queries:
        print(f"\n  Query: {query}")
        
        # With memory
        response = requests.post(f"{BASE_URL}/api/chat", json={
            "message": query,
            "use_memory": True
        })
        data = response.json()
        print(f"  With Memory: {data['response'][:100]}...")
        
        # Without memory
        response = requests.post(f"{BASE_URL}/api/chat", json={
            "message": query,
            "use_memory": False
        })
        data = response.json()
        print(f"  Without Memory: {data['response'][:100]}...")
    
    # Test 3: Load demo data
    print("\n3️⃣ Loading demo data...")
    response = requests.post(f"{BASE_URL}/api/load-demo")
    data = response.json()
    print(f"  Demo data loaded: {data}")
    
    # Test 4: Check stats
    print("\n4️⃣ Checking system stats...")
    response = requests.get(f"{BASE_URL}/api/stats")
    stats = response.json()
    print(f"  Total Events: {stats['total_events']}")
    
    print("\n✅ Memory system test complete!")

if __name__ == "__main__":
    test_memory_system() 
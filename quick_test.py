#!/usr/bin/env python3
import requests

def test_memory():
    # Test 1: Memory OFF
    print('🔍 Testing Memory OFF:')
    response = requests.post('http://localhost:8001/api/chat', json={'message': 'My name is John', 'use_memory': False})
    print('Response:', response.json()['response'][:100])

    # Test 2: Memory ON - Store info
    print('\n🧠 Testing Memory ON - Storing info:')
    response = requests.post('http://localhost:8001/api/chat', json={'message': 'My favorite color is blue', 'use_memory': True})
    print('Response:', response.json()['response'][:100])

    # Test 3: Memory ON - Retrieve info
    print('\n🔍 Testing Memory ON - Should retrieve:')
    response = requests.post('http://localhost:8001/api/chat', json={'message': 'What is my favorite color?', 'use_memory': True})
    result = response.json()
    print('Response:', result['response'][:100])
    print('Memory Context:', result.get('memory_context', []))

if __name__ == "__main__":
    test_memory() 
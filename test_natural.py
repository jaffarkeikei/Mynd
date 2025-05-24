#!/usr/bin/env python3
import requests

def test_natural_conversation():
    print('🧪 Testing Natural Conversation System')
    print('=' * 50)
    
    # Test 1: Memory OFF
    print('\n🔍 Memory OFF:')
    response = requests.post('http://localhost:8001/api/chat', json={'message': 'I love chocolate', 'use_memory': False})
    print('Response:', response.json()['response'])

    # Test 2: Memory ON - Store info  
    print('\n🧠 Memory ON - Statement:')
    response = requests.post('http://localhost:8001/api/chat', json={'message': 'I love chocolate ice cream', 'use_memory': True})
    print('Response:', response.json()['response'])

    # Test 3: Memory ON - Question
    print('\n❓ Memory ON - Question:')
    response = requests.post('http://localhost:8001/api/chat', json={'message': 'What do I love?', 'use_memory': True})
    result = response.json()
    print('Response:', result['response'])
    print('Memory Context shown:', result.get('memory_context', []))

if __name__ == "__main__":
    test_natural_conversation() 
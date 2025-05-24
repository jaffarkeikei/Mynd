#!/usr/bin/env python3
import requests
import time

def test_confidence_system():
    print('🎯 Testing Confidence-Based Memory System')
    print('=' * 50)
    
    def test_message(msg, memory_on, description):
        mode = "Memory ON" if memory_on else "Memory OFF"
        print(f'\n{description}')
        print(f'{mode} - "{msg}":')
        response = requests.post('http://localhost:8001/api/chat', json={'message': msg, 'use_memory': memory_on})
        result = response.json()
        print(f'AI: {result["response"]}')
        time.sleep(0.5)
    
    # Test 1: Greetings (should get AI response - low confidence)
    test_message('hi', True, '👋 Test 1: Greeting (should get AI response)')
    test_message('hello', False, '👋 Test 1b: Greeting memory OFF')
    
    # Test 2: Store specific information
    test_message('My favorite programming language is Python because it is simple and powerful', True, '📝 Test 2: Store specific info')
    
    # Test 3: Ask about stored info (should get high confidence retrieval)
    test_message('What is my favorite programming language?', True, '❓ Test 3: Ask about stored info (should retrieve)')
    test_message('What programming language do I prefer?', True, '❓ Test 3b: Similar question (should retrieve)')
    
    # Test 4: Ask unrelated question (should get AI response - low confidence)
    test_message('What is the weather today?', True, '🌤️ Test 4: Unrelated question (should get AI response)')
    
    # Test 5: Memory OFF
    test_message('What is my favorite programming language?', False, '🚫 Test 5: Memory OFF (should get AI response)')

if __name__ == "__main__":
    test_confidence_system() 
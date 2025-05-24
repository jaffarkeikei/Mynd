#!/usr/bin/env python3
"""
Quick Demo: Real AI Integration with Mynd
Shows how to enhance Claude or Gemini with project memory
"""
import os
import requests
import time

def check_mynd_server():
    """Check if Mynd server is running"""
    try:
        response = requests.get("http://localhost:8080/", timeout=2)
        return response.status_code == 200
    except:
        return False

def get_context_from_mynd(query: str) -> str:
    """Simple function to get context from Mynd"""
    try:
        # Authenticate
        auth_response = requests.post("http://localhost:8080/api/tokens", json={
            "client_id": "demo-client",
            "scope": "context_read",
            "ttl_seconds": 3600,
            "max_tokens": 5000
        }, timeout=5)
        
        if auth_response.status_code != 200:
            return ""
        
        token = auth_response.json()['data']['token']
        
        # Get context
        context_response = requests.post("http://localhost:8080/api/context", 
            headers={"Authorization": f"Bearer {token}"},
            json={"query": query, "max_tokens": 2000},
            timeout=10
        )
        
        if context_response.status_code == 200:
            return context_response.json()['data']['context']
        return ""
    except:
        return ""

def demo_claude_integration():
    """Demo Claude integration (requires ANTHROPIC_API_KEY)"""
    print("\n🤖 Claude + Mynd Demo")
    print("="*50)
    
    try:
        import anthropic
        
        api_key = os.getenv('ANTHROPIC_API_KEY')
        if not api_key:
            print("❌ Set ANTHROPIC_API_KEY environment variable")
            return
        
        client = anthropic.Anthropic(api_key=api_key)
        
        # Test question
        question = "How should we handle caching in our application?"
        print(f"Question: {question}")
        
        # Get context from Mynd
        print("\n🧠 Getting project context...")
        context = get_context_from_mynd(question)
        
        if context:
            print(f"✅ Found {len(context)} chars of context")
            
            # Ask Claude with context
            prompt = f"""You're helping a development team. Here's their project context:

{context}

Question: {question}

Based on the specific project context, provide targeted advice."""

            print("\n🤖 Claude's contextual response:")
            response = client.messages.create(
                model="claude-3-haiku-20240307",
                max_tokens=1000,
                messages=[{"role": "user", "content": prompt}]
            )
            
            print(response.content[0].text[:300] + "...")
            print("\n✅ Claude provided project-specific guidance!")
        else:
            print("❌ No context available")
            
    except ImportError:
        print("❌ Install: pip install anthropic")
    except Exception as e:
        print(f"❌ Error: {e}")

def demo_gemini_integration():
    """Demo Gemini integration (requires GOOGLE_API_KEY)"""
    print("\n🤖 Gemini + Mynd Demo")
    print("="*50)
    
    try:
        import google.generativeai as genai
        
        api_key = os.getenv('GOOGLE_API_KEY')
        if not api_key:
            print("❌ Set GOOGLE_API_KEY environment variable")
            return
        
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-pro')
        
        # Test question
        question = "What security measures should we implement?"
        print(f"Question: {question}")
        
        # Get context from Mynd
        print("\n🧠 Getting project context...")
        context = get_context_from_mynd(question)
        
        if context:
            print(f"✅ Found {len(context)} chars of context")
            
            # Ask Gemini with context
            prompt = f"""You're helping a development team. Here's their project context:

{context}

Question: {question}

Based on the specific project context, provide targeted advice."""

            print("\n🤖 Gemini's contextual response:")
            response = model.generate_content(prompt)
            
            print(response.text[:300] + "...")
            print("\n✅ Gemini provided project-specific guidance!")
        else:
            print("❌ No context available")
            
    except ImportError:
        print("❌ Install: pip install google-generativeai")
    except Exception as e:
        print(f"❌ Error: {e}")

def quick_setup_guide():
    """Show quick setup instructions"""
    print("\n📋 Quick Setup Guide")
    print("="*50)
    print("1. Start Mynd server:")
    print("   python test_server.py")
    print("\n2. Set up AI API keys:")
    print("   export ANTHROPIC_API_KEY='your-claude-key'")
    print("   export GOOGLE_API_KEY='your-gemini-key'")
    print("\n3. Install AI libraries:")
    print("   pip install anthropic google-generativeai")
    print("\n4. Run this demo:")
    print("   python demo_real_ai.py")

def main():
    print("🚀 Mynd + Real AI Integration Demo")
    print("="*60)
    print("Demonstrating how project memory enhances AI responses")
    
    # Check prerequisites
    if not check_mynd_server():
        print("\n❌ Mynd server not running")
        print("💡 Start with: python test_server.py")
        quick_setup_guide()
        return
    
    print("\n✅ Mynd server is running")
    
    # Test available integrations
    claude_available = bool(os.getenv('ANTHROPIC_API_KEY'))
    gemini_available = bool(os.getenv('GOOGLE_API_KEY'))
    
    if claude_available:
        demo_claude_integration()
    
    if gemini_available:
        demo_gemini_integration()
    
    if not claude_available and not gemini_available:
        print("\n💡 No AI API keys found")
        print("Set ANTHROPIC_API_KEY or GOOGLE_API_KEY to see real integration")
        
        # Show simulated example
        print("\n🎭 Simulated Example:")
        print("Question: How should we handle database scaling?")
        print("\n🧠 Mynd Context: Your project uses PostgreSQL with...")
        print("🤖 AI Response: Based on your PostgreSQL setup and partitioning strategy...")
        print("\n✅ AI becomes project-aware instead of giving generic advice!")
    
    print(f"\n🎉 Demo Complete!")
    print("💡 Real AI integration transforms generic assistants into project experts!")
    
    if not claude_available or not gemini_available:
        quick_setup_guide()

if __name__ == "__main__":
    main() 
#!/usr/bin/env python3
"""
Mynd Quick Demo - See AI Memory in Action!
"""
import os
import sys
from pathlib import Path

# Add parent directory to path so we can import src
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.main import Mynd

def print_banner():
    """Print a nice banner"""
    print("\n" + "="*60)
    print("🧠 Mynd - Universal AI Memory Demo")
    print("="*60)
    print("Give every AI perfect memory of YOUR context!\n")

def create_demo_data():
    """Create some interesting demo data"""
    print("📝 Creating demo memories...")
    
    mynd = Mynd()
    
    # Create varied demo events
    demo_events = [
        # Authentication decision
        {
            "type": "browser",
            "content": "Researched JWT vs session authentication. Decided on JWT because mobile app needs stateless auth. Considered security implications but chose simplicity.",
            "source": "https://auth0.com/blog/jwt-authentication"
        },
        # Architecture document
        {
            "type": "document", 
            "content": "Architecture Decision: JWT Authentication\nProblem: Need auth for web and mobile\nSolution: JWT with refresh tokens\nReasoning: Stateless, scalable, mobile-friendly",
            "source": "auth-decisions.md"
        },
        # Code implementation
        {
            "type": "code",
            "content": "# JWT implementation with PyJWT\n# Added refresh tokens for security\n# 15min access token, 7day refresh token\n# Tokens cached in memory for speed",
            "source": "auth_service.py"
        },
        # Team meeting notes
        {
            "type": "meeting",
            "content": "Team decided on PostgreSQL over MongoDB. Reasons: ACID compliance, better for relational data, team expertise. Will use JSON columns for flexibility.",
            "source": "team-meeting-2024-03-15.md"
        },
        # Code review
        {
            "type": "code_review",
            "content": "PR #234: Switched from REST to GraphQL for mobile API. Benefits: Reduced overfetching, better performance on slow connections, single endpoint.",
            "source": "github.com/myapp/pr/234"
        }
    ]
    
    # Store events
    for event_data in demo_events:
        event = mynd.extractor.create_semantic_event(
            source_type=event_data["type"],
            source_path=event_data["source"],
            content=event_data["content"],
            metadata={"demo": True}
        )
        mynd.db.store_event(event)
        mynd.vector_store.store_event(event)
        print(f"  ✅ Stored: {event_data['type']} - {event_data['source'][:30]}...")
    
    print(f"\n✨ Created {len(demo_events)} demo memories!")
    return mynd

def demo_queries(mynd):
    """Run some interesting queries"""
    print("\n🔍 Testing AI Memory Queries...")
    print("-"*60)
    
    queries = [
        "What authentication method did we choose and why?",
        "What database did the team decide to use?",
        "Tell me about our API architecture decisions"
    ]
    
    for i, query in enumerate(queries, 1):
        print(f"\n📌 Query {i}: {query}")
        print("-"*40)
        
        context = mynd.get_context_for_query(query, max_tokens=300)
        if context:
            # Show first few lines of context
            lines = context.split('\n')[:5]
            for line in lines:
                if line.strip():
                    print(f"  → {line[:80]}...")
        else:
            print("  ❌ No relevant context found")

def test_with_ai(mynd):
    """Test with real AI if available"""
    print("\n🤖 AI Integration Test")
    print("-"*60)
    
    # Check if Claude is available
    try:
        import anthropic
        api_key = os.getenv('ANTHROPIC_API_KEY')
        if api_key:
            print("✅ Claude API available!")
            
            # Get context and ask Claude
            context = mynd.get_context_for_query("authentication decisions", max_tokens=500)
            
            client = anthropic.Anthropic(api_key=api_key)
            response = client.messages.create(
                model="claude-3-haiku-20240307",
                max_tokens=200,
                messages=[{
                    "role": "user",
                    "content": f"Based on this project context:\n{context}\n\nWhat authentication approach was chosen?"
                }]
            )
            
            print("\n🤖 Claude's response (with YOUR project memory):")
            print("-"*40)
            print(response.content[0].text)
            
        else:
            print("⚠️  Set ANTHROPIC_API_KEY to test with Claude")
            print("   export ANTHROPIC_API_KEY='your-key-here'")
    except ImportError:
        print("⚠️  Install anthropic to test with Claude: pip install anthropic")
    except Exception as e:
        print(f"⚠️  Claude test skipped: {e}")

def main():
    """Run the demo"""
    print_banner()
    
    # Check if data exists
    mynd = Mynd()
    stats = mynd.db.get_stats()
    
    if stats['total_events'] > 0:
        print(f"ℹ️  Found existing data: {stats['total_events']} memories")
        response = input("Create fresh demo data? (y/n): ").lower()
        if response == 'y':
            mynd = create_demo_data()
    else:
        mynd = create_demo_data()
    
    # Run queries
    demo_queries(mynd)
    
    # Test with AI
    test_with_ai(mynd)
    
    print("\n🎉 Demo Complete!")
    print("\nNext steps:")
    print("  1. Try your own queries: mynd query 'your question'")
    print("  2. Add real data: mynd capture your-file.txt")
    print("  3. Start MCP server: mynd start --port 8765")
    print("  4. Integrate with AI: Set API keys and run examples/")
    print("\n💡 Mynd gives every AI perfect memory of YOUR context!")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 Demo interrupted")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1) 
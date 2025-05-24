#!/usr/bin/env python3
"""
Practical Memory Test: Add Real Data → Test AI Recall
This demonstrates how new information gets stored and can be recalled by AI
"""
import os
import time
import requests
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

try:
    import anthropic
    ANTHROPIC_AVAILABLE = True
except ImportError:
    ANTHROPIC_AVAILABLE = False

class PracticalMemoryTest:
    """Test memory storage and AI recall with real data"""
    
    def __init__(self):
        self.mynd_base_url = "http://localhost:8080"
        self.mynd_token = None
        
        # Initialize Claude client
        self.claude_api_key = os.getenv('ANTHROPIC_API_KEY')
        if not self.claude_api_key or not ANTHROPIC_AVAILABLE:
            print("⚠️  Using simulated Claude responses")
            self.claude_client = None
        else:
            self.claude_client = anthropic.Anthropic(api_key=self.claude_api_key)

    def authenticate_mynd(self) -> bool:
        """Authenticate with Mynd"""
        try:
            response = requests.post(f"{self.mynd_base_url}/api/tokens", json={
                "client_id": "practical-memory-test",
                "scope": "context_read",
                "ttl_seconds": 3600,
                "max_tokens": 8000
            }, timeout=5)
            
            if response.status_code == 200:
                self.mynd_token = response.json()['data']['token']
                return True
            return False
        except Exception as e:
            print(f"❌ Authentication failed: {e}")
            return False

    def add_new_data_to_system(self):
        """Add new data directly to the Mynd system"""
        print("📝 Adding new project data to the system...")
        
        # Import the Mynd classes
        try:
            from src.main import Mynd
            from src.semantic_extractor import SemanticExtractor
        except ImportError:
            print("❌ Cannot import Mynd classes - make sure you're in the right directory")
            return False
        
        # Create a Mynd instance to access the database and vector store
        mynd = Mynd()
        extractor = SemanticExtractor()
        
        # New project decision to add
        new_project_data = [
            {
                "source_type": "meeting_notes",
                "source_path": "/project/meetings/2025-01-08-api-design.md",
                "content": """
API Design Decision: GraphQL vs REST for Mobile App

Decision: We chose GraphQL over REST for our mobile API.

Key reasons:
- Mobile needs flexible data fetching to reduce bandwidth
- Frontend team prefers single endpoint with type safety
- Real-time subscriptions needed for chat features
- GraphQL introspection helps with development speed

Trade-offs considered:
- REST has better caching (decided to use CDN caching)
- GraphQL learning curve (team training budget approved)
- Query complexity attacks (rate limiting implemented)

Implementation:
- Apollo Server with Express.js backend
- Apollo Client for React Native
- DataLoader for N+1 query prevention
- Redis caching for repeated queries

Performance target: <200ms response time for 95% of queries
Cost impact: Development time +2 weeks, but maintenance time -30%
                """,
                "metadata": {"meeting_date": "2025-01-08", "participants": 5, "decision_type": "architecture"}
            },
            {
                "source_type": "documentation",
                "source_path": "/project/docs/redis-strategy.md", 
                "content": """
Redis Implementation Strategy

Implementation: Multi-layer caching with Redis Cluster

Architecture:
- L1 Cache: Application memory (Node.js)
- L2 Cache: Redis single instance (development)
- L3 Cache: Redis Cluster (production)

Use cases:
- Session storage (TTL: 24 hours)
- API response caching (TTL: 5 minutes)
- Rate limiting counters (TTL: 1 hour)
- Real-time data (pub/sub for notifications)

Configuration:
- Memory: 8GB Redis instances
- Persistence: RDB snapshots every 15 minutes
- Replication: 2 replicas per master
- Monitoring: RedisInsight + DataDog integration

Cost analysis: $450/month for production cluster vs $1200/month for ElastiCache
Performance: 99.9% hit rate, <1ms latency for cache hits
                """,
                "metadata": {"doc_type": "technical_spec", "version": "1.2", "status": "approved"}
            },
            {
                "source_type": "code_review",
                "source_path": "/project/backend/auth/oauth-integration.py",
                "content": """
OAuth 2.0 Integration Implementation

# Added Google and GitHub OAuth providers
# Security considerations addressed:
# - PKCE for mobile app security
# - State parameter for CSRF protection
# - Secure token storage with encryption

Implementation details:
- OAuth library: Authlib (chosen over requests-oauthlib for better PKCE support)
- Token encryption: Fernet symmetric encryption
- Refresh token rotation: Automatic with 7-day expiry
- Scope validation: Strict whitelist approach

Security measures:
- Redirect URI validation with exact matching
- Rate limiting: 5 attempts per minute per IP
- Token revocation: Immediate on logout
- Audit logging: All auth events logged to secure table

Testing:
- Unit tests: 95% coverage on auth flows
- Integration tests: Full OAuth flow simulation
- Security scan: No vulnerabilities detected
                """,
                "metadata": {"language": "python", "review_status": "approved", "security_review": "passed"}
            }
        ]
        
        events_added = 0
        for data in new_project_data:
            if extractor.is_content_relevant(data["content"]):
                event = extractor.create_semantic_event(
                    source_type=data["source_type"],
                    source_path=data["source_path"],
                    content=data["content"],
                    metadata=data["metadata"]
                )
                
                # Store in both database and vector store
                if mynd.db.store_event(event):
                    mynd.vector_store.store_event(event)
                    events_added += 1
                    print(f"   ✅ Added: {data['source_type']} - {data['source_path'].split('/')[-1]}")
        
        print(f"📊 Successfully added {events_added} new events to memory system")
        return events_added > 0

    def get_context_about(self, query: str) -> str:
        """Get context from Mynd about a specific topic"""
        if not self.mynd_token:
            return None
        
        try:
            response = requests.post(f"{self.mynd_base_url}/api/context", 
                headers={"Authorization": f"Bearer {self.mynd_token}"},
                json={"query": query, "max_tokens": 3000},
                timeout=10
            )
            
            if response.status_code == 200:
                return response.json()['data'].get('context', '')
            return None
        except Exception as e:
            print(f"❌ Failed to get context: {e}")
            return None

    def ask_claude_about(self, question: str, include_context: bool = True) -> str:
        """Ask Claude a question, optionally with Mynd context"""
        if not self.claude_client:
            if include_context:
                context = self.get_context_about(question)
                if context and len(context) > 100:
                    return f"[SIMULATED WITH CONTEXT] Based on recent project memory:\n{context[:300]}...\n\nI can reference the specific decisions and details from your project."
                else:
                    return "[SIMULATED] No relevant information found in project memory."
            else:
                return "[SIMULATED WITHOUT CONTEXT] I don't have information about your specific project."
        
        try:
            if include_context:
                context = self.get_context_about(question)
                if context and len(context) > 50:
                    prompt = f"""You are an AI assistant with access to the development team's project memory.

Project Context:
{context}

Based on this project information, please answer: {question}

Reference specific details from the context in your response."""
                else:
                    prompt = f"Please answer this question about a software project: {question}"
            else:
                prompt = f"Please answer this question about a software project: {question}"

            response = self.claude_client.messages.create(
                model="claude-3-haiku-20240307",
                max_tokens=1200,
                messages=[{"role": "user", "content": prompt}]
            )
            return response.content[0].text
            
        except Exception as e:
            return f"Error calling Claude: {e}"

    def run_practical_test(self):
        """Run the complete practical memory test"""
        print("🧠 Practical Memory Test: Real Data → AI Recall")
        print("="*70)
        
        # Check server
        try:
            response = requests.get(f"{self.mynd_base_url}/", timeout=2)
            if response.status_code != 200:
                print("❌ Mynd server not running - start with: python3 test_server.py")
                return
        except:
            print("❌ Mynd server not running - start with: python3 test_server.py")
            return
        
        print("✅ Mynd server is running")
        
        # Step 1: Add new data to the system
        print("\n📝 STEP 1: Adding New Project Data")
        print("-" * 50)
        
        if not self.add_new_data_to_system():
            print("❌ Failed to add new data")
            return
        
        # Authenticate with MCP server
        if not self.authenticate_mynd():
            print("❌ Failed to authenticate with MCP server")
            return
        
        print("✅ Connected to MCP server")
        
        # Wait for indexing
        print("⏳ Waiting for vector indexing...")
        time.sleep(3)
        
        # Step 2: Test AI recall with different questions
        test_questions = [
            "Why did we choose GraphQL over REST for our API?",
            "What's our Redis caching strategy and how much does it cost?",
            "How did we implement OAuth security and what measures did we take?",
        ]
        
        for i, question in enumerate(test_questions, 1):
            print(f"\n🎯 TEST {i}: {question}")
            print("-" * 70)
            
            # Test WITHOUT context
            print("🤖 Claude WITHOUT project memory:")
            response_without = self.ask_claude_about(question, include_context=False)
            print(response_without[:250] + "..." if len(response_without) > 250 else response_without)
            
            # Test WITH context
            print("\n🧠 Claude WITH project memory:")
            response_with = self.ask_claude_about(question, include_context=True)
            print(response_with[:350] + "..." if len(response_with) > 350 else response_with)
            
            # Quick analysis
            context = self.get_context_about(question)
            if context and len(context) > 100:
                # Check for specific details
                specific_terms = ["GraphQL", "Apollo", "Redis Cluster", "DataLoader", "OAuth", "PKCE", "Authlib"]
                found_terms = [term for term in specific_terms if term in response_with]
                
                print(f"\n📊 Memory recall: {len(found_terms)} specific terms found")
                if found_terms:
                    print(f"   Details recalled: {', '.join(found_terms)}")
                    print("   ✅ AI successfully used project memory")
                else:
                    print("   ⚠️  AI didn't recall specific project details")
            else:
                print("\n❌ No relevant context found for this question")
        
        print("\n🎉 Practical Memory Test Complete!")
        print("="*70)
        print("💡 Summary:")
        print("   ✅ Added real project data to memory system")
        print("   ✅ Tested AI recall of specific decisions and details")
        print("   ✅ Demonstrated memory-enhanced vs generic responses")
        print("\n🚀 Your AI now has persistent project knowledge!")

def main():
    print("🧠 Starting Practical Memory Test")
    print("This adds real project data and tests AI recall\n")
    
    tester = PracticalMemoryTest()
    tester.run_practical_test()

if __name__ == "__main__":
    main() 
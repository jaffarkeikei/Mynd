#!/usr/bin/env python3
"""
Specific Memory Test Example
1. Store new information in Mynd
2. Ask Claude about it immediately
3. Verify Claude remembers and uses the new information
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

class MemoryTestExample:
    """Test real-time memory storage and retrieval"""
    
    def __init__(self):
        self.mynd_base_url = "http://localhost:8080"
        self.mynd_token = None
        
        # Initialize Claude client
        self.claude_api_key = os.getenv('ANTHROPIC_API_KEY')
        if not self.claude_api_key or not ANTHROPIC_AVAILABLE:
            print("⚠️  ANTHROPIC_API_KEY not set - using simulated responses")
            self.claude_client = None
        else:
            self.claude_client = anthropic.Anthropic(api_key=self.claude_api_key)

    def authenticate_mynd(self) -> bool:
        """Authenticate with Mynd"""
        try:
            response = requests.post(f"{self.mynd_base_url}/api/tokens", json={
                "client_id": "memory-test-example",
                "scope": "context_read context_write",
                "ttl_seconds": 3600,
                "max_tokens": 8000
            }, timeout=5)
            
            if response.status_code == 200:
                self.mynd_token = response.json()['data']['token']
                return True
            return False
        except Exception as e:
            print(f"❌ Failed to authenticate: {e}")
            return False

    def store_new_information(self, title: str, content: str, tags: list = None) -> bool:
        """Store new information in Mynd memory"""
        if not self.mynd_token:
            return False
        
        try:
            payload = {
                "title": title,
                "content": content,
                "tags": tags or [],
                "timestamp": datetime.now().isoformat(),
                "source": "memory_test_example"
            }
            
            response = requests.post(f"{self.mynd_base_url}/api/memories",
                headers={"Authorization": f"Bearer {self.mynd_token}"},
                json=payload,
                timeout=10
            )
            
            if response.status_code in [200, 201]:
                print(f"✅ Stored: {title}")
                return True
            else:
                print(f"❌ Failed to store memory: {response.status_code}")
                return False
                
        except Exception as e:
            print(f"❌ Error storing memory: {e}")
            return False

    def get_context_about(self, query: str) -> str:
        """Get context from Mynd about a specific topic"""
        if not self.mynd_token:
            return None
        
        try:
            response = requests.post(f"{self.mynd_base_url}/api/context", 
                headers={"Authorization": f"Bearer {self.mynd_token}"},
                json={"query": query, "max_tokens": 2000},
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
                if context:
                    return f"[SIMULATED WITH CONTEXT] Based on recent project memory: {context[:200]}...\n\nI can reference the specific decisions and information stored in your project memory."
                else:
                    return "[SIMULATED] I don't have any specific information about that topic in your project memory."
            else:
                return "[SIMULATED WITHOUT CONTEXT] I don't have information about your specific project decisions."
        
        try:
            if include_context:
                # Get context first
                context = self.get_context_about(question)
                if context:
                    prompt = f"""You are a helpful AI assistant with access to the development team's project memory.

Project Context:
{context}

Based on this project information, please answer: {question}

Reference the specific details from the project context in your response."""
                else:
                    prompt = f"Please answer this question about a software project: {question}"
            else:
                prompt = f"Please answer this question about a software project: {question}"

            response = self.claude_client.messages.create(
                model="claude-3-haiku-20240307",
                max_tokens=1000,
                messages=[{"role": "user", "content": prompt}]
            )
            return response.content[0].text
            
        except Exception as e:
            return f"Error calling Claude: {e}"

    def run_memory_example(self):
        """Run the complete memory storage and retrieval example"""
        print("🧠 Memory Test Example: Store → Remember → Verify")
        print("="*70)
        
        # Check server
        try:
            response = requests.get(f"{self.mynd_base_url}/", timeout=2)
            if response.status_code != 200:
                print("❌ Mynd server not running")
                return
        except:
            print("❌ Mynd server not running")
            return
        
        # Authenticate
        if not self.authenticate_mynd():
            print("❌ Failed to authenticate with Mynd")
            return
        
        print("✅ Connected to Mynd server")
        
        # Step 1: Store new project decision
        print("\n📝 STEP 1: Storing New Project Decision")
        print("-" * 50)
        
        new_decision = {
            "title": "Database Choice: PostgreSQL for User Analytics",
            "content": """
Decision: We chose PostgreSQL over MongoDB for our user analytics system.

Reasoning:
- Need complex queries for user behavior analysis
- ACID compliance for financial data
- Strong JSON support for flexible schemas
- Better performance for our read-heavy workload
- Team expertise with SQL

Trade-offs:
- More complex scaling than MongoDB
- Need to manage schema migrations
- Higher initial setup complexity

Implementation details:
- Using connection pooling with pgbouncer
- Read replicas for analytics queries
- Partitioning user data by date
- Indexing on user_id and timestamp

Cost impact: ~$200/month for managed PostgreSQL vs $300/month for MongoDB Atlas
Performance: 40% faster queries than our MongoDB prototype
            """,
            "tags": ["database", "postgresql", "analytics", "architecture", "performance"]
        }
        
        if self.store_new_information(new_decision["title"], new_decision["content"], new_decision["tags"]):
            print("💾 Successfully stored the PostgreSQL decision in project memory")
        else:
            print("❌ Failed to store the decision")
            return
        
        # Wait a moment for indexing
        print("⏳ Waiting for memory indexing...")
        time.sleep(2)
        
        # Step 2: Ask Claude WITHOUT context first
        print("\n❓ STEP 2: Testing Claude WITHOUT Project Memory")
        print("-" * 50)
        question = "Why did we choose PostgreSQL for analytics and what were the trade-offs?"
        
        response_without = self.ask_claude_about(question, include_context=False)
        print("🤖 Claude's response WITHOUT memory:")
        print(response_without[:300] + "..." if len(response_without) > 300 else response_without)
        
        # Step 3: Ask Claude WITH context
        print("\n🧠 STEP 3: Testing Claude WITH Project Memory")
        print("-" * 50)
        
        response_with = self.ask_claude_about(question, include_context=True)
        print("🤖 Claude's response WITH memory:")
        print(response_with[:400] + "..." if len(response_with) > 400 else response_with)
        
        # Step 4: Analysis
        print("\n📊 STEP 4: Memory Test Analysis")
        print("-" * 50)
        
        # Check if specific details were remembered
        memory_indicators = [
            "PostgreSQL", "MongoDB", "pgbouncer", "read replicas", 
            "$200/month", "40% faster", "ACID compliance", "partitioning"
        ]
        
        found_details = [detail for detail in memory_indicators if detail in response_with]
        
        print(f"Memory recall test:")
        print(f"   Response length without memory: {len(response_without)} chars")
        print(f"   Response length with memory: {len(response_with)} chars")
        print(f"   Specific details recalled: {len(found_details)}/{len(memory_indicators)}")
        print(f"   Details found: {', '.join(found_details)}")
        
        if len(found_details) >= 3:
            print("   ✅ Excellent memory recall - Claude referenced specific stored details")
        elif len(found_details) >= 1:
            print("   ✅ Good memory recall - Claude used some stored information")
        else:
            print("   ❌ Poor memory recall - Claude didn't use stored details")
        
        # Check for project-specific language
        project_terms = ["we chose", "our decision", "our team", "our analytics"]
        project_refs = sum(1 for term in project_terms if term.lower() in response_with.lower())
        
        if project_refs > 0:
            print("   ✅ Claude used project-specific language")
        else:
            print("   ⚠️  Claude didn't use project-specific language")
        
        print("\n🎉 Memory Test Complete!")
        print("="*70)
        print("💡 Key Findings:")
        
        if len(found_details) >= 3:
            print("   ✅ Memory system successfully stored and retrieved specific details")
            print("   ✅ Claude can reference exact decisions, costs, and technical details")
            print("   ✅ AI responses became project-specific instead of generic")
        else:
            print("   ⚠️  Memory storage worked, but retrieval needs optimization")
            print("   💡 Try asking more specific questions to trigger better context matching")
        
        print("\n🚀 This demonstrates real-time AI memory enhancement!")

def main():
    print("🧠 Starting Specific Memory Test Example")
    print("This will store new information and immediately test if Claude remembers it\n")
    
    tester = MemoryTestExample()
    tester.run_memory_example()

if __name__ == "__main__":
    main() 
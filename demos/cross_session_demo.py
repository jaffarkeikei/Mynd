#!/usr/bin/env python3
"""
Cross-Session Memory Demo
Shows how AI remembers context across different sessions/tabs/time
"""
import os
import time
import requests
from dotenv import load_dotenv

load_dotenv()

try:
    import anthropic
    ANTHROPIC_AVAILABLE = True
except ImportError:
    ANTHROPIC_AVAILABLE = False

class CrossSessionDemo:
    """Demonstrate how AI memory works across different sessions"""
    
    def __init__(self):
        self.mynd_base_url = "http://localhost:8080"
        self.mynd_token = None
        
        self.claude_api_key = os.getenv('ANTHROPIC_API_KEY')
        if not self.claude_api_key or not ANTHROPIC_AVAILABLE:
            print("⚠️  Using simulated responses")
            self.claude_client = None
        else:
            self.claude_client = anthropic.Anthropic(api_key=self.claude_api_key)

    def authenticate(self):
        """Authenticate with Mynd"""
        try:
            response = requests.post(f"{self.mynd_base_url}/api/tokens", json={
                "client_id": "cross-session-demo",
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

    def simulate_different_question_types(self):
        """Show how the system handles different types of questions about the same underlying topic"""
        
        print("🔍 DEMONSTRATION: How AI Memory Works Across Sessions")
        print("="*80)
        print("Scenario: You worked on database decisions last week.")
        print("Today, in a new tab/session, you ask follow-up questions.\n")
        
        # Different ways someone might ask about the same underlying information
        question_variations = [
            {
                "context": "Week 1 - You researched databases",
                "question": "What database should we use for user analytics?",
                "explanation": "Direct question about database choice"
            },
            {
                "context": "Week 2 - New tab, different angle", 
                "question": "How much will our data storage cost per month?",
                "explanation": "Cost question - but relates to previous database research"
            },
            {
                "context": "Week 3 - Following up on performance",
                "question": "Why are our queries slow and how can we optimize them?",
                "explanation": "Performance question - connects to database implementation details"
            },
            {
                "context": "Week 4 - Team discussion about scaling",
                "question": "What infrastructure changes do we need for 10x more users?",
                "explanation": "Scaling question - relates to database architecture decisions"
            }
        ]
        
        for i, scenario in enumerate(question_variations, 1):
            print(f"📅 {scenario['context']}")
            print(f"❓ Question: {scenario['question']}")
            print(f"💭 Type: {scenario['explanation']}")
            print("-" * 60)
            
            # Show what context gets retrieved
            context = self.get_relevant_context(scenario['question'])
            if context:
                print("🧠 Context Retrieved from Memory:")
                print(f"   {context[:200]}...")
                
                # Show what keywords/concepts were matched
                self.analyze_semantic_matching(scenario['question'], context)
            else:
                print("❌ No relevant context found")
            
            # Get AI response
            ai_response = self.ask_ai_with_memory(scenario['question'])
            print(f"\n🤖 AI Response:")
            print(f"   {ai_response[:300]}...")
            
            print("\n" + "="*80 + "\n")

    def get_relevant_context(self, question: str) -> str:
        """Get context for a question (simulates the semantic search)"""
        if not self.mynd_token:
            return None
        
        try:
            response = requests.post(f"{self.mynd_base_url}/api/context", 
                headers={"Authorization": f"Bearer {self.mynd_token}"},
                json={"query": question, "max_tokens": 2000},
                timeout=10
            )
            
            if response.status_code == 200:
                return response.json()['data'].get('context', '')
            return None
        except Exception as e:
            print(f"❌ Failed to get context: {e}")
            return None

    def analyze_semantic_matching(self, question: str, context: str):
        """Show how semantic matching works (not just keywords)"""
        print("🔍 Semantic Analysis:")
        
        # Extract key concepts from question
        question_concepts = self.extract_concepts(question.lower())
        context_concepts = self.extract_concepts(context.lower())
        
        # Find semantic connections
        direct_matches = set(question_concepts) & set(context_concepts)
        semantic_connections = self.find_semantic_connections(question_concepts, context_concepts)
        
        print(f"   Question concepts: {', '.join(question_concepts[:5])}")
        print(f"   Context concepts: {', '.join(context_concepts[:5])}")
        print(f"   Direct matches: {', '.join(direct_matches) if direct_matches else 'None'}")
        print(f"   Semantic connections: {', '.join(semantic_connections)}")

    def extract_concepts(self, text: str) -> list:
        """Extract key concepts from text"""
        # Simple concept extraction (in real system this uses embeddings)
        tech_concepts = [
            'database', 'postgresql', 'mongodb', 'performance', 'cost', 'scaling',
            'queries', 'analytics', 'storage', 'infrastructure', 'optimization',
            'users', 'data', 'architecture', 'implementation', 'memory'
        ]
        
        found_concepts = [concept for concept in tech_concepts if concept in text]
        return found_concepts

    def find_semantic_connections(self, question_concepts: list, context_concepts: list) -> list:
        """Find semantic relationships (simplified version)"""
        # This simulates how vector embeddings find related concepts
        semantic_map = {
            'cost': ['infrastructure', 'scaling', 'performance'],
            'slow': ['performance', 'optimization', 'queries'],
            'scaling': ['infrastructure', 'users', 'architecture'],
            'storage': ['database', 'data', 'infrastructure'],
            'optimize': ['performance', 'queries', 'architecture']
        }
        
        connections = []
        for q_concept in question_concepts:
            for related in semantic_map.get(q_concept, []):
                if related in context_concepts:
                    connections.append(f"{q_concept}→{related}")
        
        return connections

    def ask_ai_with_memory(self, question: str) -> str:
        """Ask AI with memory context"""
        context = self.get_relevant_context(question)
        
        if not self.claude_client:
            if context and len(context) > 50:
                return f"Based on your project memory, I can reference specific details about {question.split()[0].lower()} decisions and provide project-specific guidance."
            else:
                return "I don't have specific information about your project for this question."
        
        try:
            if context and len(context) > 50:
                prompt = f"""You are an AI assistant with access to project memory.

Project Context: {context}

Question: {question}

Reference specific details from the context in your response."""
            else:
                prompt = f"Answer this software project question: {question}"

            response = self.claude_client.messages.create(
                model="claude-3-haiku-20240307",
                max_tokens=800,
                messages=[{"role": "user", "content": prompt}]
            )
            return response.content[0].text
            
        except Exception as e:
            return f"Error calling AI: {e}"

    def run_demo(self):
        """Run the complete cross-session demo"""
        print("🧠 Cross-Session AI Memory Demo")
        print("Understanding how AI remembers across different contexts\n")
        
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
        if not self.authenticate():
            print("❌ Failed to authenticate")
            return
        
        print("✅ Connected to Mynd memory system\n")
        
        # Run the demonstration
        self.simulate_different_question_types()
        
        print("🎯 KEY INSIGHTS:")
        print("="*50)
        print("✅ Questions don't need exact keywords")
        print("✅ System finds semantic relationships")
        print("✅ Memory persists across sessions/tabs/time")
        print("✅ AI responses become project-specific")
        print("✅ Follow-up questions work automatically")
        
        print("\n💡 How This Works:")
        print("1. 📝 Information stored with semantic embeddings")
        print("2. 🔍 Questions analyzed for meaning (not just keywords)")
        print("3. 🧠 Vector search finds relevant context")
        print("4. 🤖 AI responds with project-specific knowledge")
        print("5. 🔄 Works across any session/tab/time period")

def main():
    print("🧠 Starting Cross-Session Memory Demo")
    print("This shows how AI memory works across different contexts\n")
    
    demo = CrossSessionDemo()
    demo.run_demo()

if __name__ == "__main__":
    main() 
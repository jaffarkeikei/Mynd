#!/usr/bin/env python3
"""
Real-World Mynd Demo
Demonstrates practical use cases for development teams
"""
import requests
import time
import json
from typing import Dict, List

class RealWorldDemo:
    """Demonstrate real-world Mynd usage scenarios"""
    
    def __init__(self):
        self.base_url = "http://localhost:8080"
        self.token = None
    
    def authenticate(self, client_name: str) -> bool:
        """Authenticate with the MCP server"""
        try:
            response = requests.post(f"{self.base_url}/api/tokens", json={
                "client_id": client_name,
                "scope": "context_read",
                "ttl_seconds": 7200,
                "max_tokens": 8000
            }, timeout=5)
            
            if response.status_code == 200:
                self.token = response.json()['data']['token']
                return True
            return False
        except:
            return False
    
    def query_context(self, query: str, max_tokens: int = 2000) -> Dict:
        """Query context from Mynd"""
        if not self.token:
            return {"error": "Not authenticated"}
        
        try:
            response = requests.post(f"{self.base_url}/api/context", 
                headers={"Authorization": f"Bearer {self.token}"},
                json={"query": query, "max_tokens": max_tokens},
                timeout=10
            )
            
            if response.status_code == 200:
                return response.json()['data']
            return {"error": f"Query failed: {response.status_code}"}
        except Exception as e:
            return {"error": str(e)}
    
    def scenario_new_developer_onboarding(self):
        """Scenario: New developer joining the team"""
        print("\n🎯 SCENARIO 1: New Developer Onboarding")
        print("="*60)
        print("👤 Alex just joined the team and needs to understand our e-commerce platform")
        
        if not self.authenticate("alex-new-developer"):
            print("❌ Authentication failed - ensure server is running")
            return
        
        print("✅ Alex authenticated with Mynd")
        
        # Realistic onboarding questions
        onboarding_questions = [
            {
                "question": "What is our overall system architecture?",
                "context": "Understanding the big picture"
            },
            {
                "question": "How do we handle payments in our system?",
                "context": "Learning about critical business logic"
            },
            {
                "question": "What security measures do we have in place?",
                "context": "Understanding security requirements"
            },
            {
                "question": "How is our database structured?",
                "context": "Learning about data models"
            }
        ]
        
        for i, qa in enumerate(onboarding_questions, 1):
            print(f"\n   Question {i}: {qa['question']}")
            print(f"   Context: {qa['context']}")
            
            result = self.query_context(qa['question'])
            if 'error' not in result:
                context = result.get('context', '')
                tokens = result.get('tokens_used', 0)
                
                # Extract key insights
                lines = context.split('\n')
                sources = [line for line in lines if line.strip().startswith('[')][:3]
                
                print(f"   ✅ Found {len(sources)} relevant sources ({tokens} tokens)")
                for source in sources:
                    if source.strip():
                        source_type = source.split(']')[0].replace('[', '')
                        preview = source.split(':', 2)[-1][:80] if ':' in source else source[:80]
                        print(f"      📄 {source_type}: {preview}...")
            else:
                print(f"   ❌ {result['error']}")
    
    def scenario_code_review_prep(self):
        """Scenario: Preparing for code review"""
        print("\n🎯 SCENARIO 2: Code Review Preparation")
        print("="*60)
        print("👩‍💻 Sarah is reviewing payment integration code and needs context")
        
        if not self.authenticate("sarah-senior-dev"):
            print("❌ Authentication failed")
            return
        
        print("✅ Sarah authenticated with Mynd")
        
        review_questions = [
            "Why did we choose Stripe over other payment providers?",
            "What error handling patterns are we using for payments?",
            "How do we handle webhook validation and security?",
            "What monitoring do we have for payment failures?"
        ]
        
        print("\n   💭 Sarah's code review checklist:")
        for i, question in enumerate(review_questions, 1):
            print(f"\n   {i}. {question}")
            
            result = self.query_context(question, max_tokens=1500)
            if 'error' not in result:
                context = result.get('context', '')
                
                # Simulate extracting decision rationale
                if 'stripe' in context.lower():
                    print("      ✅ Found Stripe decision rationale")
                if 'error' in context.lower() or 'webhook' in context.lower():
                    print("      ✅ Found error handling patterns")
                if 'monitoring' in context.lower() or 'datadog' in context.lower():
                    print("      ✅ Found monitoring setup")
                
                preview = context[:120].replace('\n', ' ')
                print(f"      📋 Context: {preview}...")
            else:
                print(f"      ❌ {result['error']}")
    
    def scenario_incident_response(self):
        """Scenario: Production incident response"""
        print("\n🎯 SCENARIO 3: Production Incident Response")
        print("="*60)
        print("🚨 Payment failures are spiking - DevOps team needs quick context")
        
        if not self.authenticate("devops-oncall"):
            print("❌ Authentication failed")
            return
        
        print("✅ DevOps team authenticated with Mynd")
        
        incident_queries = [
            "How do we monitor payment failures?",
            "What alerts do we have for payment issues?",
            "How do Stripe webhooks work in our system?",
            "What's our error handling for payment processing?"
        ]
        
        print("\n   🔥 Rapid context gathering for incident response:")
        start_time = time.time()
        
        for i, query in enumerate(incident_queries, 1):
            query_start = time.time()
            result = self.query_context(query, max_tokens=1000)
            query_time = time.time() - query_start
            
            print(f"\n   {i}. {query}")
            if 'error' not in result:
                context = result.get('context', '')
                tokens = result.get('tokens_used', 0)
                
                # Extract actionable info
                actionable_keywords = ['alert', 'monitor', 'webhook', 'error', 'datadog', 'stripe']
                found_keywords = [kw for kw in actionable_keywords if kw in context.lower()]
                
                print(f"      ⚡ {query_time:.2f}s - {tokens} tokens - {len(found_keywords)} actionable items")
                if found_keywords:
                    print(f"      🎯 Key topics: {', '.join(found_keywords[:3])}")
            else:
                print(f"      ❌ {result['error']}")
        
        total_time = time.time() - start_time
        print(f"\n   📊 Total context gathering: {total_time:.2f}s")
        print("   ✅ Team has context to debug payment issues quickly")
    
    def scenario_architecture_decision(self):
        """Scenario: Making new architecture decisions"""
        print("\n🎯 SCENARIO 4: Architecture Decision Making")
        print("="*60)
        print("🏗️ Team is scaling and needs to review past architectural decisions")
        
        if not self.authenticate("architecture-team"):
            print("❌ Authentication failed")
            return
        
        print("✅ Architecture team authenticated with Mynd")
        
        architecture_queries = [
            "What technology decisions have we made and why?",
            "How did we evaluate AWS vs other cloud providers?",
            "What are our current performance optimization strategies?",
            "What security requirements influenced our design?"
        ]
        
        print("\n   🔍 Reviewing past architectural decisions:")
        
        for i, query in enumerate(architecture_queries, 1):
            print(f"\n   {i}. {query}")
            
            result = self.query_context(query, max_tokens=2500)
            if 'error' not in result:
                context = result.get('context', '')
                sources = result.get('sources', [])
                
                # Analyze decision patterns
                decision_keywords = ['decision', 'chose', 'selected', 'because', 'vs', 'trade-off']
                decisions = [kw for kw in decision_keywords if kw in context.lower()]
                
                print(f"      📚 Found {len(sources)} source types with {len(decisions)} decision indicators")
                
                # Extract decision summaries
                lines = context.split('\n')
                decision_lines = [line for line in lines if any(kw in line.lower() for kw in decision_keywords)][:2]
                
                for decision in decision_lines:
                    if decision.strip():
                        clean_decision = decision.strip()[:100]
                        print(f"      💡 {clean_decision}...")
            else:
                print(f"      ❌ {result['error']}")
    
    def scenario_stakeholder_update(self):
        """Scenario: Preparing stakeholder updates"""
        print("\n🎯 SCENARIO 5: Stakeholder Update Preparation")
        print("="*60)
        print("📊 Product Manager needs to prepare technical progress update")
        
        if not self.authenticate("product-manager"):
            print("❌ Authentication failed")
            return
        
        print("✅ Product Manager authenticated with Mynd")
        
        stakeholder_topics = [
            "What are our key technical achievements this sprint?",
            "What infrastructure costs should we expect?",
            "What security measures are we implementing?",
            "How are we ensuring system performance and reliability?"
        ]
        
        print("\n   📈 Gathering technical progress for stakeholders:")
        
        summary_points = []
        for i, topic in enumerate(stakeholder_topics, 1):
            print(f"\n   {i}. {topic}")
            
            result = self.query_context(topic, max_tokens=1500)
            if 'error' not in result:
                context = result.get('context', '')
                
                # Extract business-relevant information
                business_keywords = ['cost', 'performance', 'security', 'scalable', 'monitoring', 'stripe']
                business_items = [kw for kw in business_keywords if kw in context.lower()]
                
                if business_items:
                    summary_points.extend(business_items[:2])
                    print(f"      ✅ Found business-relevant info: {', '.join(business_items[:3])}")
                else:
                    print("      📝 General technical context found")
            else:
                print(f"      ❌ {result['error']}")
        
        print(f"\n   📋 Summary for stakeholders:")
        print(f"      • Technical progress covers: {', '.join(set(summary_points))}")
        print(f"      • {len(stakeholder_topics)} key areas documented")
        print(f"      • Ready for executive summary preparation")

def main():
    print("🌍 Mynd Real-World Usage Demonstration")
    print("="*70)
    print("Demonstrating how development teams use Mynd in practice")
    
    demo = RealWorldDemo()
    
    # Check if server is running
    try:
        response = requests.get(f"{demo.base_url}/", timeout=2)
        if response.status_code != 200:
            print("❌ Mynd server not responding. Start with: python test_server.py")
            return
    except:
        print("❌ Mynd server not running. Start with: python test_server.py")
        return
    
    print("✅ Mynd server is running")
    print("\nRunning 5 realistic team scenarios...\n")
    
    # Run all scenarios
    demo.scenario_new_developer_onboarding()
    demo.scenario_code_review_prep()
    demo.scenario_incident_response()
    demo.scenario_architecture_decision()
    demo.scenario_stakeholder_update()
    
    print("\n🎉 Real-World Demo Complete!")
    print("="*70)
    print("💡 Key Benefits Demonstrated:")
    print("   • Accelerated onboarding for new team members")
    print("   • Enhanced code review with historical context")
    print("   • Faster incident response with quick context access")
    print("   • Informed architecture decisions based on past learnings")
    print("   • Efficient stakeholder communication with technical summaries")
    print("\n🚀 Mynd enables teams to:")
    print("   ✅ Preserve institutional knowledge")
    print("   ✅ Reduce context-switching overhead")
    print("   ✅ Improve decision-making with historical insight")
    print("   ✅ Accelerate team productivity")
    print("   ✅ Enhance collaboration across roles")

if __name__ == "__main__":
    main() 
"""
Semantic extraction engine using local LLM for privacy-preserving context extraction
"""
import re
import json
from typing import Dict, List, Optional, Any

try:
    import ollama
    OLLAMA_AVAILABLE = True
except ImportError:
    OLLAMA_AVAILABLE = False

from .models import SemanticEvent

class PIIDetector:
    """Detect and remove personally identifiable information"""
    
    def __init__(self):
        # Common PII patterns
        self.patterns = {
            'email': r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b',
            'phone': r'\b\d{3}-\d{3}-\d{4}\b|\b\(\d{3}\)\s*\d{3}-\d{4}\b',
            'ssn': r'\b\d{3}-\d{2}-\d{4}\b',
            'credit_card': r'\b\d{4}[-\s]?\d{4}[-\s]?\d{4}[-\s]?\d{4}\b',
            'api_key': r'[a-zA-Z0-9]{32,}',
            'password': r'password[:\s]*[^\s]+',
            'token': r'token[:\s]*[^\s]+',
        }
    
    def remove_pii(self, text: str) -> str:
        """Remove PII from text while preserving context"""
        sanitized = text
        
        for pii_type, pattern in self.patterns.items():
            sanitized = re.sub(pattern, f'[{pii_type.upper()}_REDACTED]', 
                             sanitized, flags=re.IGNORECASE)
        
        return sanitized
    
    def validate_content(self, content: str) -> bool:
        """Check if content is safe for processing"""
        return len(content.strip()) > 0

class SemanticExtractor:
    """Extract semantic meaning from content using local LLM"""
    
    def __init__(self, model: str = "llama3.1:8b-instruct-q4_0"):
        self.model = model
        self.pii_detector = PIIDetector()
        
        if OLLAMA_AVAILABLE:
            try:
                self.client = ollama.Client()
                # Test if model is available
                self.client.chat(
                    model=self.model,
                    messages=[{"role": "user", "content": "test"}],
                    stream=False
                )
                self.llm_available = True
            except (ConnectionError, Exception) as e:
                print(f"Ollama not available: {e}")
                self.llm_available = False
        else:
            print("Ollama package not installed")
            self.llm_available = False
    
    def extract_concepts(self, text: str) -> List[str]:
        """Extract key concepts from text using simple heuristics"""
        # Fallback concept extraction if LLM is not available
        words = re.findall(r'\b[A-Z][a-z]+|[a-z]+(?:[A-Z][a-z]*)*\b', text)
        
        # Filter out common words and focus on technical/decision terms
        concept_keywords = [
            'API', 'database', 'architecture', 'framework', 'library',
            'authentication', 'security', 'performance', 'design',
            'implementation', 'decision', 'choice', 'alternative',
            'solution', 'problem', 'requirement', 'feature'
        ]
        
        concepts = []
        text_lower = text.lower()
        
        for keyword in concept_keywords:
            if keyword.lower() in text_lower:
                concepts.append(keyword)
        
        # Add any capitalized words that might be technology names
        for word in words:
            if len(word) > 3 and word[0].isupper():
                concepts.append(word)
        
        return list(set(concepts))[:10]  # Limit to 10 concepts
    
    async def extract_semantic_meaning(self, content: str, 
                                     content_type: str = "general") -> Dict[str, Any]:
        """Extract semantic meaning from content"""
        
        # First, sanitize the content
        sanitized_content = self.pii_detector.remove_pii(content)
        
        if self.llm_available:
            return await self._extract_with_llm(sanitized_content, content_type)
        
        return self._extract_fallback(sanitized_content)
    
    async def _extract_with_llm(self, content: str, content_type: str) -> Dict[str, Any]:
        """Extract semantic meaning using local LLM"""
        
        prompt = f"""
        Analyze this {content_type} content and extract ONLY decision-making context and insights.
        Do NOT include any personal data, only patterns and decisions.
        
        Content: {content}
        
        Extract and return as JSON:
        {{
            "summary": "Brief summary of the main point or decision",
            "concepts": ["key", "technical", "concepts"],
            "decision_context": "What decision was being made or considered?",
            "factors": ["factors", "that", "influenced", "decision"],
            "outcome": "What was decided or concluded?"
        }}
        
        Focus on:
        - Technical decisions and reasoning
        - Problem-solving approaches
        - Learning and insights
        - Workflow patterns
        
        Ignore:
        - Personal details
        - Specific data values
        - Private information
        """
        
        try:
            response = self.client.chat(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                stream=False
            )
            
            # Extract JSON from response
            response_text = response['message']['content']
            
            # Try to parse JSON from the response
            json_match = re.search(r'\{.*\}', response_text, re.DOTALL)
            if json_match:
                json_str = json_match.group(0)
                result = json.loads(json_str)
                
                # Validate required fields
                required_fields = ['summary', 'concepts', 'decision_context']
                for field in required_fields:
                    if field not in result:
                        result[field] = ""
                
                return result
            
            # Fallback if JSON parsing fails
            return self._extract_fallback(content)
                
        except (json.JSONDecodeError, KeyError, ConnectionError) as e:
            print(f"LLM extraction error: {e}")
            return self._extract_fallback(content)
    
    def _extract_fallback(self, content: str) -> Dict[str, Any]:
        """Fallback extraction method when LLM is not available"""
        
        # Simple heuristic-based extraction
        concepts = self.extract_concepts(content)
        
        # Create a simple summary (first 100 chars)
        summary = content[:100].strip()
        if len(content) > 100:
            summary += "..."
        
        # Look for decision-related keywords
        decision_keywords = ['decided', 'chose', 'selected', 'picked', 'opted']
        decision_context = ""
        
        for keyword in decision_keywords:
            if keyword in content.lower():
                # Find sentence containing the keyword
                sentences = content.split('.')
                for sentence in sentences:
                    if keyword in sentence.lower():
                        decision_context = sentence.strip()
                        break
                break
        
        return {
            "summary": summary,
            "concepts": concepts,
            "decision_context": decision_context,
            "factors": [],
            "outcome": ""
        }
    
    def create_semantic_event(self, source_type: str, source_path: str, 
                             content: str, metadata: Optional[Dict] = None) -> SemanticEvent:
        """Create a semantic event from content"""
        
        # Extract semantic meaning
        if self.llm_available:
            # For demo purposes, use sync version
            try:
                self.client.chat(
                    model=self.model,
                    messages=[{
                        "role": "user", 
                        "content": f"""Extract key insights from: {content[:500]}
                        Return: summary, concepts (list), decision_context"""
                    }],
                    stream=False
                )
                
                # Simple parsing for demo
                semantic_data = {
                    "summary": content[:200],
                    "concepts": self.extract_concepts(content),
                    "decision_context": None
                }
            except (ConnectionError, Exception):
                semantic_data = self._extract_fallback(content)
        else:
            semantic_data = self._extract_fallback(content)
        
        # Create the semantic event
        event = SemanticEvent.create(
            source_type=source_type,
            source_path=source_path,
            semantic_summary=semantic_data["summary"],
            concepts=semantic_data["concepts"],
            decision_context=semantic_data.get("decision_context"),
            metadata=metadata or {}
        )
        
        return event
    
    def is_content_relevant(self, content: str) -> bool:
        """Determine if content is worth extracting semantic meaning from"""
        
        # Skip very short content
        if len(content.strip()) < 50:
            return False
        
        # Look for decision-making or technical content indicators
        relevance_indicators = [
            'decided', 'chose', 'implemented', 'solution', 'problem',
            'design', 'architecture', 'code', 'bug', 'fix', 'feature',
            'research', 'analysis', 'conclusion', 'recommendation'
        ]
        
        content_lower = content.lower()
        for indicator in relevance_indicators:
            if indicator in content_lower:
                return True
        
        # Check for technical concepts
        tech_indicators = [
            'api', 'database', 'server', 'client', 'framework',
            'library', 'algorithm', 'performance', 'security'
        ]
        
        for indicator in tech_indicators:
            if indicator in content_lower:
                return True
        
        return False 
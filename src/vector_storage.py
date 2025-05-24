"""
Vector storage using ChromaDB for semantic search
"""
from typing import List, Dict, Optional
from pathlib import Path

try:
    import chromadb
    from chromadb.config import Settings
    CHROMADB_AVAILABLE = True
except ImportError:
    CHROMADB_AVAILABLE = False

from .models import SemanticEvent, ContextQuery

class VectorStorage:
    """ChromaDB-based vector storage for semantic search"""
    
    def __init__(self, data_dir: str):
        self.data_dir = data_dir
        Path(data_dir).mkdir(parents=True, exist_ok=True)
        
        if CHROMADB_AVAILABLE:
            try:
                self.client = chromadb.PersistentClient(
                    path=data_dir,
                    settings=Settings(
                        anonymized_telemetry=False,
                        allow_reset=False
                    )
                )
                
                # Get or create collection for semantic events
                self.collection = self.client.get_or_create_collection(
                    name="semantic_events",
                    metadata={"description": "Mynd semantic events"}
                )
                
                self.available = True
                print(f"✅ ChromaDB initialized at {data_dir}")
                
            except Exception as e:
                print(f"ChromaDB initialization error: {e}")
                self.available = False
        else:
            print("ChromaDB not available - vector search disabled")
            self.available = False
    
    def store_event(self, event: SemanticEvent) -> bool:
        """Store a semantic event in the vector database"""
        if not self.available:
            return False
        
        try:
            # Combine summary and concepts for embedding
            content_for_embedding = f"{event.semantic_summary} {' '.join(event.concepts)}"
            if event.decision_context:
                content_for_embedding += f" {event.decision_context}"
            
            # Prepare metadata
            metadata = {
                "source_type": event.source_type,
                "source_path": event.source_path,
                "timestamp": event.timestamp.isoformat(),
                "concepts": ",".join(event.concepts),
            }
            
            # Add custom metadata
            for key, value in event.metadata.items():
                if isinstance(value, (str, int, float, bool)):
                    metadata[f"meta_{key}"] = str(value)
            
            # Store in ChromaDB
            self.collection.add(
                documents=[content_for_embedding],
                metadatas=[metadata],
                ids=[event.id]
            )
            
            return True
            
        except Exception as e:
            print(f"Error storing event in vector database: {e}")
            return False
    
    def search_similar(self, query: str, limit: int = 10, 
                      source_type: Optional[str] = None) -> List[Dict]:
        """Search for similar semantic events"""
        if not self.available:
            return []
        
        try:
            where_filter = {}
            if source_type:
                where_filter["source_type"] = source_type
            
            results = self.collection.query(
                query_texts=[query],
                n_results=limit,
                where=where_filter if where_filter else None
            )
            
            # Format results
            formatted_results = []
            if results['documents'] and results['documents'][0]:
                for i, doc in enumerate(results['documents'][0]):
                    result = {
                        'id': results['ids'][0][i],
                        'content': doc,
                        'metadata': results['metadatas'][0][i],
                        'distance': results['distances'][0][i] if results.get('distances') else 0
                    }
                    formatted_results.append(result)
            
            return formatted_results
            
        except Exception as e:
            print(f"Error searching vector database: {e}")
            return []
    
    def get_context_for_query(self, query: str, max_tokens: int = 4000) -> str:
        """Get relevant context for a query, optimized for token limits"""
        if not self.available:
            return "Vector search not available - install ChromaDB"
        
        # Search for relevant events
        similar_events = self.search_similar(query, limit=20)
        
        if not similar_events:
            return "No relevant context found in your memory."
        
        # Build context response with token management
        context_parts = []
        total_tokens = 0
        
        context_parts.append(f"Relevant context for '{query}':\n")
        
        for i, event in enumerate(similar_events):
            metadata = event['metadata']
            content = event['content']
            
            # Estimate tokens (rough approximation: 1 token ≈ 4 chars)
            event_tokens = len(content) // 4
            
            if total_tokens + event_tokens > max_tokens - 200:  # Leave buffer
                break
            
            # Format the context entry
            source_info = f"[{metadata.get('source_type', 'unknown')}]"
            timestamp = metadata.get('timestamp', 'unknown')[:10]  # Just date
            
            context_entry = f"\n{i+1}. {source_info} ({timestamp}):\n{content}\n"
            
            context_parts.append(context_entry)
            total_tokens += event_tokens
        
        # Add summary
        context_parts.append(f"\nFound {len(similar_events)} relevant memories using {total_tokens} tokens.")
        
        return "".join(context_parts)
    
    def get_stats(self) -> Dict:
        """Get vector database statistics"""
        if not self.available:
            return {"available": False, "total_vectors": 0}
        
        try:
            count = self.collection.count()
            return {
                "available": True,
                "total_vectors": count,
                "data_dir": self.data_dir
            }
        except Exception as e:
            return {
                "available": False,
                "error": str(e),
                "total_vectors": 0
            }
    
    def delete_event(self, event_id: str) -> bool:
        """Delete an event from the vector database"""
        if not self.available:
            return False
        
        try:
            self.collection.delete(ids=[event_id])
            return True
        except Exception as e:
            print(f"Error deleting event from vector database: {e}")
            return False
    
    def update_event(self, event: SemanticEvent) -> bool:
        """Update an existing event in the vector database"""
        if not self.available:
            return False
        
        # Delete the old version and add the new one
        self.delete_event(event.id)
        return self.store_event(event) 
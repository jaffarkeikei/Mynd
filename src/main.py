"""
Main application orchestrator for Mynd
"""
import asyncio
import os
import sys
from pathlib import Path
from typing import Optional

from .database import MyndDB
from .vector_storage import VectorStorage
from .semantic_extractor import SemanticExtractor

class Mynd:
    """Main Mynd application orchestrator"""
    
    def __init__(self, data_dir: Optional[str] = None):
        if data_dir is None:
            data_dir = str(Path.home() / ".myndai")
        
        self.data_dir = data_dir
        os.makedirs(data_dir, exist_ok=True)
        
        # Initialize core components
        self.db = MyndDB(os.path.join(data_dir, "mynd.db"))
        self.vector_store = VectorStorage(os.path.join(data_dir, "chroma_db"))
        self.extractor = SemanticExtractor()
        
        # Server configuration
        self.port = 8080
        
        print("✅ Mynd initialized")
    
    async def initial_capture(self, _days: int = 30):
        """Perform initial data capture from available sources"""
        # Note: _days parameter reserved for future browser history capture
        print("🔍 Starting initial data capture...")
        
        # For now, we'll create some demo data
        # In a full implementation, this would capture from:
        # - Browser history (using _days parameter)
        # - Document directories
        # - Git repositories
        # - Clipboard history
        
        demo_events = [
            {
                "source_type": "browser",
                "source_path": "https://docs.python.org/authentication",
                "content": "Researched JWT vs session authentication. Decided on JWT because mobile app needs stateless auth. Considered security implications of client-side token storage but chose it over Redis complexity.",
                "metadata": {"domain": "docs.python.org", "visit_count": 3}
            },
            {
                "source_type": "document", 
                "source_path": "/Users/dev/projects/auth-decisions.md",
                "content": "Architecture Decision: JWT Authentication. Problem: Need authentication for web and mobile. Solution: JWT with refresh tokens. Reasoning: Stateless, mobile-friendly, scalable. Trade-offs: XSS risk vs infrastructure simplicity.",
                "metadata": {"file_type": "markdown", "size": 1024}
            },
            {
                "source_type": "code",
                "source_path": "/Users/dev/projects/user-service/auth.py", 
                "content": "# Implemented JWT authentication with refresh tokens\n# Choice: Used PyJWT library for token handling\n# Security: Added token expiration and refresh mechanism\n# Performance: Tokens cached in memory for validation speed",
                "metadata": {"language": "python", "lines": 150}
            }
        ]
        
        events_created = 0
        for demo_event in demo_events:
            if self.extractor.is_content_relevant(demo_event["content"]):
                event = self.extractor.create_semantic_event(
                    source_type=demo_event["source_type"],
                    source_path=demo_event["source_path"],
                    content=demo_event["content"],
                    metadata=demo_event["metadata"]
                )
                
                # Store in both database and vector store
                if self.db.store_event(event):
                    self.vector_store.store_event(event)
                    events_created += 1
        
        print(f"✅ Created {events_created} semantic events from demo data")
    
    def get_context_for_query(self, query: str, max_tokens: int = 4000) -> str:
        """Get relevant context for a query"""
        return self.vector_store.get_context_for_query(query, max_tokens)
    
    async def start_mcp_server(self):
        """Start the MCP server"""
        # Import here to avoid circular imports
        from .mcp_server import MCPServer
        
        print(f"🚀 Starting MCP server on http://localhost:{self.port}")
        print("📡 Ready to serve context to AI clients")
        
        # Create and run the MCP server
        mcp_server = MCPServer(mynd_instance=self, port=self.port)
        await mcp_server.run_server()
    
    async def run(self):
        """Run the complete Mynd system"""
        
        # Perform initial capture
        await self.initial_capture()
        
        # Start MCP server
        await self.start_mcp_server()

def main():
    """Main entry point"""
    
    print("""
    🧠 Mynd - Universal AI Memory
    ====================================
    
    Starting up...
    """)
    
    # Create and run Mynd
    vault = Mynd()
    
    try:
        asyncio.run(vault.run())
    except KeyboardInterrupt:
        print("\n👋 Mynd shutting down...")
    except (ConnectionError, OSError) as e:
        print(f"❌ Connection error: {e}")
        sys.exit(1)
    except ImportError as e:
        print(f"❌ Import error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main() 
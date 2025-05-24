"""
MCP Server implementation for Mynd
Provides secure context delivery to AI clients via Model Context Protocol
"""
import asyncio
import hashlib
from datetime import datetime, timedelta
from typing import Dict, List, Optional
from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel
import uvicorn

from .main import Mynd
from .models import CapabilityToken, AuditEvent, MCPResponse, ContextQuery

# Pydantic models for API requests/responses
class ContextRequest(BaseModel):
    query: str
    max_tokens: int = 4000
    source_types: Optional[List[str]] = None
    include_metadata: bool = False

class TokenRequest(BaseModel):
    client_id: str
    scope: str = "context_read"
    ttl_seconds: int = 300
    max_tokens: int = 4000

class MCPServerResponse(BaseModel):
    success: bool
    data: Optional[Dict] = None
    message: str = ""
    timestamp: str = datetime.now().isoformat()

class MCPServer:
    """FastAPI-based MCP server for secure context delivery"""
    
    def __init__(self, mynd_instance: Optional[Mynd] = None, port: int = 8080):
        self.port = port
        self.mynd = mynd_instance or Mynd()
        self.app = FastAPI(
            title="Mynd MCP Server",
            description="Universal AI Memory Context Server",
            version="0.1.0"
        )
        
        # Active capability tokens
        self.active_tokens: Dict[str, CapabilityToken] = {}
        
        # Security
        self.security = HTTPBearer()
        
        # Setup middleware
        self.setup_middleware()
        
        # Setup routes
        self.setup_routes()
    
    def setup_middleware(self):
        """Setup CORS and other middleware"""
        self.app.add_middleware(
            CORSMiddleware,
            allow_origins=["*"],  # In production, restrict this
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )
    
    def setup_routes(self):
        """Setup API routes"""
        
        @self.app.get("/")
        async def root():
            return {"message": "Mynd MCP Server", "status": "running"}
        
        @self.app.get("/api/status")
        async def status():
            """Get server status and statistics"""
            stats = self.mynd.db.get_stats()
            vector_stats = self.mynd.vector_store.get_stats()
            
            return MCPServerResponse(
                success=True,
                data={
                    "server": "running",
                    "database": stats,
                    "vector_store": vector_stats,
                    "active_tokens": len(self.active_tokens),
                    "capabilities": ["context_read", "context_search"]
                },
                message="MCP server operational"
            )
        
        @self.app.post("/api/tokens")
        async def create_capability_token(request: TokenRequest):
            """Create a new capability token for AI client access"""
            try:
                # Create capability token
                token = CapabilityToken.create(
                    client_id=request.client_id,
                    scope=request.scope,
                    ttl_seconds=request.ttl_seconds,
                    max_tokens=request.max_tokens
                )
                
                # Store in database and memory
                self.mynd.db.store_capability_token(token)
                self.active_tokens[token.token_id] = token
                
                # Log token creation
                audit_event = AuditEvent.create(
                    event_type="token_created",
                    ai_client=request.client_id,
                    capability_token_hash=hashlib.sha256(token.token_id.encode()).hexdigest()[:16]
                )
                self.mynd.db.log_audit_event(audit_event)
                
                return MCPServerResponse(
                    success=True,
                    data={
                        "token": token.token_id,
                        "expires_at": token.expires_at.isoformat(),
                        "scope": token.scope,
                        "max_tokens": token.max_tokens
                    },
                    message="Capability token created"
                )
                
            except Exception as e:
                raise HTTPException(status_code=500, detail=f"Token creation failed: {str(e)}") from e
        
        @self.app.post("/api/context")
        async def get_context(
            request: ContextRequest, 
            credentials: HTTPAuthorizationCredentials = Depends(self.security)
        ):
            """Get relevant context for a query (requires capability token)"""
            try:
                # Validate token
                token = await self.validate_token(credentials.credentials)
                
                # Create context query
                context_query = ContextQuery(
                    query=request.query,
                    max_tokens=min(request.max_tokens, token.max_tokens),
                    source_types=request.source_types,
                    include_metadata=request.include_metadata
                )
                
                # Get context from Mynd
                context = self.mynd.get_context_for_query(
                    context_query.query, 
                    max_tokens=context_query.max_tokens
                )
                
                # Count tokens (rough estimation)
                tokens_used = len(context) // 4
                
                # Create MCP response
                mcp_response = MCPResponse(
                    context=context,
                    tokens_used=tokens_used,
                    sources=self.extract_sources(context),
                    capability_token=token.token_id,
                    expires_at=token.expires_at
                )
                
                # Log access
                query_hash = hashlib.sha256(request.query.encode()).hexdigest()[:16]
                audit_event = AuditEvent.create(
                    event_type="context_accessed",
                    ai_client=token.client_id,
                    query_hash=query_hash,
                    context_tokens=tokens_used,
                    capability_token_hash=hashlib.sha256(token.token_id.encode()).hexdigest()[:16]
                )
                self.mynd.db.log_audit_event(audit_event)
                
                return MCPServerResponse(
                    success=True,
                    data=mcp_response.to_dict(),
                    message="Context retrieved successfully"
                )
                
            except HTTPException:
                raise
            except Exception as e:
                raise HTTPException(status_code=500, detail=f"Context retrieval failed: {str(e)}") from e
        
        @self.app.get("/api/search/{query}")
        async def search_context(
            query: str,
            max_tokens: int = 4000,
            credentials: HTTPAuthorizationCredentials = Depends(self.security)
        ):
            """Simple GET endpoint for context search"""
            request = ContextRequest(query=query, max_tokens=max_tokens)
            return await get_context(request, credentials)
        
        @self.app.delete("/api/tokens/{token_id}")
        async def revoke_token(
            token_id: str,
            credentials: HTTPAuthorizationCredentials = Depends(self.security)
        ):
            """Revoke a capability token"""
            try:
                # Validate current token
                current_token = await self.validate_token(credentials.credentials)
                
                # Only allow revoking own token or if admin scope
                if token_id != current_token.token_id and current_token.scope != "admin":
                    raise HTTPException(status_code=403, detail="Cannot revoke other tokens")
                
                # Remove from active tokens
                if token_id in self.active_tokens:
                    del self.active_tokens[token_id]
                
                # Log revocation
                audit_event = AuditEvent.create(
                    event_type="token_revoked",
                    ai_client=current_token.client_id,
                    capability_token_hash=hashlib.sha256(token_id.encode()).hexdigest()[:16]
                )
                self.mynd.db.log_audit_event(audit_event)
                
                return MCPServerResponse(
                    success=True,
                    message="Token revoked successfully"
                )
                
            except HTTPException:
                raise
            except Exception as e:
                raise HTTPException(status_code=500, detail=f"Token revocation failed: {str(e)}") from e
        
        @self.app.get("/api/stats")
        async def get_statistics(
            credentials: HTTPAuthorizationCredentials = Depends(self.security)
        ):
            """Get usage statistics (requires valid token)"""
            try:
                token = await self.validate_token(credentials.credentials)
                
                stats = self.mynd.db.get_stats()
                
                return MCPServerResponse(
                    success=True,
                    data={
                        "client_id": token.client_id,
                        "database_stats": stats,
                        "token_info": {
                            "expires_at": token.expires_at.isoformat(),
                            "scope": token.scope,
                            "max_tokens": token.max_tokens
                        }
                    },
                    message="Statistics retrieved"
                )
                
            except HTTPException:
                raise
            except Exception as e:
                raise HTTPException(status_code=500, detail=f"Statistics retrieval failed: {str(e)}") from e
    
    async def validate_token(self, token_id: str) -> CapabilityToken:
        """Validate a capability token"""
        # Check if token exists in memory
        if token_id not in self.active_tokens:
            # Try to load from database
            # For now, we'll raise an error since we don't have a get_token method
            raise HTTPException(status_code=401, detail="Invalid capability token")
        
        token = self.active_tokens[token_id]
        
        # Check if token is expired
        if not token.is_valid():
            # Remove expired token
            del self.active_tokens[token_id]
            raise HTTPException(status_code=401, detail="Capability token expired")
        
        return token
    
    @staticmethod
    def extract_sources(context: str) -> List[str]:
        """Extract source information from context string"""
        sources = []
        lines = context.split('\n')
        for line in lines:
            if line.strip().startswith('[') and ']' in line:
                # Extract source type from [browser], [document], etc.
                source_end = line.find(']')
                if source_end > 0:
                    source = line[1:source_end]
                    if source not in sources:
                        sources.append(source)
        return sources
    
    def cleanup_expired_tokens(self):
        """Remove expired tokens from memory"""
        expired_tokens = []
        for token_id, token in self.active_tokens.items():
            if not token.is_valid():
                expired_tokens.append(token_id)
        
        for token_id in expired_tokens:
            del self.active_tokens[token_id]
    
    async def start_background_tasks(self):
        """Start background cleanup tasks"""
        while True:
            await asyncio.sleep(60)  # Run every minute
            self.cleanup_expired_tokens()
            self.mynd.db.cleanup_expired_tokens()
    
    async def run_server(self):
        """Run the MCP server"""
        # Start background tasks
        asyncio.create_task(self.start_background_tasks())
        
        # Start the server
        config = uvicorn.Config(
            app=self.app,
            host="0.0.0.0",
            port=self.port,
            log_level="info"
        )
        server = uvicorn.Server(config)
        
        print(f"🚀 Mynd MCP Server starting on http://localhost:{self.port}")
        print("📡 Ready to serve context to AI clients")
        print(f"📚 API Documentation: http://localhost:{self.port}/docs")
        
        await server.serve()

async def main():
    """Main entry point for MCP server"""
    server = MCPServer()
    await server.run_server()

if __name__ == "__main__":
    asyncio.run(main()) 
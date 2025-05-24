"""
Core data models for Mynd
"""
from dataclasses import dataclass, asdict, field
from datetime import datetime, timedelta
from typing import List, Dict, Optional, Any
import json
import uuid

@dataclass
class SemanticEvent:
    """Represents a semantic event extracted from user activity"""
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    timestamp: datetime = field(default_factory=datetime.now)
    source_type: str = ""  # 'browser', 'document', 'code', 'clipboard'
    source_path: str = ""
    semantic_summary: str = ""
    concepts: List[str] = field(default_factory=list)
    decision_context: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)

    @classmethod
    def create(cls, source_type: str, source_path: str, semantic_summary: str, 
              concepts: List[str], **kwargs) -> 'SemanticEvent':
        """Factory method to create a new SemanticEvent"""
        return cls(
            source_type=source_type,
            source_path=source_path,
            semantic_summary=semantic_summary,
            concepts=concepts,
            decision_context=kwargs.get('decision_context'),
            metadata=kwargs.get('metadata', {})
        )

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for storage"""
        return asdict(self)
    
    def to_json(self) -> str:
        """Convert to JSON string"""
        return json.dumps(self.to_dict(), default=str)

@dataclass
class ContextQuery:
    """Represents a query for contextual information"""
    query: str
    max_tokens: int = 4000
    source_types: Optional[List[str]] = None
    time_range: Optional[tuple] = None
    include_metadata: bool = False

@dataclass
class MCPResponse:
    """Response from MCP server with context"""
    context: str
    tokens_used: int
    sources: List[str]
    capability_token: str
    expires_at: datetime
    query_id: str = field(default_factory=lambda: str(uuid.uuid4()))

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for API response"""
        return {
            "context": self.context,
            "tokens_used": self.tokens_used,
            "sources": self.sources,
            "capability_token": self.capability_token,
            "expires_at": self.expires_at.isoformat(),
            "query_id": self.query_id
        }

@dataclass
class CapabilityToken:
    """Represents a capability token for MCP access"""
    token_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    client_id: str = ""
    scope: str = "context_read"
    expires_at: datetime = field(default_factory=lambda: datetime.now() + timedelta(seconds=300))
    max_tokens: int = 4000
    created_at: datetime = field(default_factory=datetime.now)

    @classmethod
    def create(cls, client_id: str, **kwargs) -> 'CapabilityToken':
        """Create a new capability token"""
        ttl_seconds = kwargs.get('ttl_seconds', 300)
        expires_at = datetime.now() + timedelta(seconds=ttl_seconds)
        
        return cls(
            client_id=client_id,
            scope=kwargs.get('scope', 'context_read'),
            expires_at=expires_at,
            max_tokens=kwargs.get('max_tokens', 4000)
        )

    def is_valid(self) -> bool:
        """Check if token is still valid"""
        return datetime.now() < self.expires_at

@dataclass
class AuditEvent:
    """Represents an audit event for security logging"""
    timestamp: datetime = field(default_factory=datetime.now)
    event_type: str = ""
    ai_client: str = ""
    query_hash: str = ""
    context_tokens: int = 0
    capability_token_hash: str = ""
    ip_address: Optional[str] = None

    @classmethod
    def create(cls, event_type: str, ai_client: str, **kwargs) -> 'AuditEvent':
        """Create a new audit event"""
        return cls(
            event_type=event_type,
            ai_client=ai_client,
            query_hash=kwargs.get('query_hash', ''),
            context_tokens=kwargs.get('context_tokens', 0),
            capability_token_hash=kwargs.get('capability_token_hash', ''),
            ip_address=kwargs.get('ip_address')
        ) 
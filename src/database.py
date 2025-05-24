"""
Database layer for Mynd using SQLite
"""
import sqlite3
import json
from datetime import datetime
from typing import List, Optional
from pathlib import Path

from .models import SemanticEvent, AuditEvent

class MyndDB:
    """SQLite database manager for Mynd"""
    
    def __init__(self, db_path: str = "mynd.db"):
        self.db_path = db_path
        # Ensure the directory exists
        Path(self.db_path).parent.mkdir(parents=True, exist_ok=True)
        self.init_database()
    
    def init_database(self):
        """Initialize the database schema"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Events table for semantic events
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS events (
                id TEXT PRIMARY KEY,
                timestamp TEXT NOT NULL,
                source_type TEXT NOT NULL,
                source_path TEXT NOT NULL,
                semantic_summary TEXT NOT NULL,
                concepts TEXT NOT NULL,  -- JSON array
                decision_context TEXT,
                metadata TEXT NOT NULL   -- JSON object
            )
        """)
        
        # Index for faster queries
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_timestamp 
            ON events(timestamp DESC)
        """)
        
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_source_type 
            ON events(source_type)
        """)
        
        # Audit log table for security
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS audit_log (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT NOT NULL,
                event_type TEXT NOT NULL,
                ai_client TEXT NOT NULL,
                query_hash TEXT NOT NULL,
                context_tokens INTEGER NOT NULL,
                capability_token_hash TEXT NOT NULL,
                ip_address TEXT
            )
        """)
        
        # Capability tokens table (for active session management)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS capability_tokens (
                token_id TEXT PRIMARY KEY,
                client_id TEXT NOT NULL,
                scope TEXT NOT NULL,
                expires_at TEXT NOT NULL,
                max_tokens INTEGER NOT NULL,
                created_at TEXT NOT NULL,
                is_active BOOLEAN DEFAULT 1
            )
        """)
        
        conn.commit()
        conn.close()
    
    def store_event(self, event: SemanticEvent) -> bool:
        """Store a semantic event"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute("""
                INSERT INTO events VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                event.id,
                event.timestamp.isoformat(),
                event.source_type,
                event.source_path,
                event.semantic_summary,
                json.dumps(event.concepts),
                event.decision_context,
                json.dumps(event.metadata)
            ))
            
            conn.commit()
            conn.close()
            return True
            
        except sqlite3.Error as e:
            print(f"Database error storing event: {e}")
            return False
    
    def get_recent_events(self, limit: int = 100, 
                         source_type: Optional[str] = None) -> List[SemanticEvent]:
        """Get recent semantic events"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        query = "SELECT * FROM events"
        params = []
        
        if source_type:
            query += " WHERE source_type = ?"
            params.append(source_type)
        
        query += " ORDER BY timestamp DESC LIMIT ?"
        params.append(limit)
        
        cursor.execute(query, params)
        rows = cursor.fetchall()
        conn.close()
        
        events = []
        for row in rows:
            event = SemanticEvent(
                id=row[0],
                timestamp=datetime.fromisoformat(row[1]),
                source_type=row[2],
                source_path=row[3],
                semantic_summary=row[4],
                concepts=json.loads(row[5]),
                decision_context=row[6],
                metadata=json.loads(row[7])
            )
            events.append(event)
        
        return events
    
    def search_events(self, query: str, limit: int = 50) -> List[SemanticEvent]:
        """Search events by semantic summary or concepts"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Simple text search - could be enhanced with FTS
        cursor.execute("""
            SELECT * FROM events 
            WHERE semantic_summary LIKE ? 
               OR concepts LIKE ?
               OR decision_context LIKE ?
            ORDER BY timestamp DESC 
            LIMIT ?
        """, (f"%{query}%", f"%{query}%", f"%{query}%", limit))
        
        rows = cursor.fetchall()
        conn.close()
        
        events = []
        for row in rows:
            event = SemanticEvent(
                id=row[0],
                timestamp=datetime.fromisoformat(row[1]),
                source_type=row[2],
                source_path=row[3],
                semantic_summary=row[4],
                concepts=json.loads(row[5]),
                decision_context=row[6],
                metadata=json.loads(row[7])
            )
            events.append(event)
        
        return events
    
    def log_audit_event(self, audit_event: AuditEvent) -> bool:
        """Log an audit event for security tracking"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute("""
                INSERT INTO audit_log 
                (timestamp, event_type, ai_client, query_hash, 
                 context_tokens, capability_token_hash, ip_address)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (
                audit_event.timestamp.isoformat(),
                audit_event.event_type,
                audit_event.ai_client,
                audit_event.query_hash,
                audit_event.context_tokens,
                audit_event.capability_token_hash,
                audit_event.ip_address
            ))
            
            conn.commit()
            conn.close()
            return True
            
        except sqlite3.Error as e:
            print(f"Database error logging audit: {e}")
            return False
    
    def store_capability_token(self, token) -> bool:
        """Store a capability token for session management"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute("""
                INSERT INTO capability_tokens VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (
                token.token_id,
                token.client_id,
                token.scope,
                token.expires_at.isoformat(),
                token.max_tokens,
                token.created_at.isoformat(),
                True
            ))
            
            conn.commit()
            conn.close()
            return True
            
        except sqlite3.Error as e:
            print(f"Database error storing token: {e}")
            return False
    
    def get_stats(self) -> dict:
        """Get database statistics"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Count events by type
        cursor.execute("""
            SELECT source_type, COUNT(*) 
            FROM events 
            GROUP BY source_type
        """)
        event_counts = dict(cursor.fetchall())
        
        # Total events
        cursor.execute("SELECT COUNT(*) FROM events")
        total_events = cursor.fetchone()[0]
        
        # Recent activity (last 7 days)
        cursor.execute("""
            SELECT COUNT(*) FROM events 
            WHERE datetime(timestamp) > datetime('now', '-7 days')
        """)
        recent_activity = cursor.fetchone()[0]
        
        conn.close()
        
        return {
            "total_events": total_events,
            "recent_activity": recent_activity,
            "event_counts": event_counts,
            "db_path": self.db_path
        }

    def cleanup_expired_tokens(self):
        """Remove expired capability tokens"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            DELETE FROM capability_tokens 
            WHERE datetime(expires_at) < datetime('now')
        """)
        
        deleted_count = cursor.rowcount
        conn.commit()
        conn.close()
        
        return deleted_count 
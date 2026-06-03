"""
Memory System for REX AI - Dual-layer short and long-term memory.
"""

import logging
import sqlite3
import json
import os
from typing import Dict, List, Optional, Any
from datetime import datetime, timedelta
from collections import deque

logger = logging.getLogger(__name__)


class MemoryItem:
    """Represents a single memory item."""
    
    def __init__(self, content: str, memory_type: str = "fact", importance: float = 0.5, tags: Optional[List[str]] = None):
        self.content = content
        self.memory_type = memory_type
        self.importance = min(1.0, max(0.0, importance))
        self.tags = tags or []
        self.created_at = datetime.now()
        self.access_count = 0
        self.last_accessed = datetime.now()
    
    def to_dict(self) -> Dict:
        """Convert to dictionary."""
        return {
            "content": self.content,
            "type": self.memory_type,
            "importance": self.importance,
            "tags": self.tags,
            "created_at": self.created_at.isoformat(),
            "access_count": self.access_count,
            "last_accessed": self.last_accessed.isoformat(),
        }


class MemorySystem:
    """Dual-layer memory system (short-term and long-term)."""
    
    def __init__(self, max_short_term: int = 1000, max_long_term: int = 10000):
        """Initialize memory system."""
        self.max_short_term = max_short_term
        self.max_long_term = max_long_term
        self.short_term_memory: deque = deque(maxlen=max_short_term)
        self.db_path = "memory/memory.db"
        os.makedirs("memory", exist_ok=True)
        self._init_database()
        logger.info(f"MemorySystem initialized")
    
    def _init_database(self):
        """Initialize the SQLite database for long-term memory."""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS memories (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    content TEXT NOT NULL,
                    type TEXT NOT NULL,
                    importance REAL NOT NULL,
                    tags TEXT,
                    created_at TIMESTAMP,
                    access_count INTEGER DEFAULT 0,
                    last_accessed TIMESTAMP
                )
            """)
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_type ON memories(type)")
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_importance ON memories(importance)")
            conn.commit()
            conn.close()
            logger.debug("Database initialized")
        except Exception as e:
            logger.error(f"Failed to initialize database: {e}")
    
    def remember(self, content: str, memory_type: str = "fact", importance: float = 0.5, 
                tags: Optional[List[str]] = None, persist: bool = False) -> bool:
        """Store a memory item."""
        try:
            item = MemoryItem(content, memory_type, importance, tags)
            self.short_term_memory.append(item)
            logger.debug(f"Stored in short-term memory: {memory_type}")
            if persist:
                self._store_long_term(item)
            return True
        except Exception as e:
            logger.error(f"Failed to remember: {e}")
            return False
    
    def recall(self, query: str, limit: int = 10) -> List[Dict]:
        """Recall memories based on a search query."""
        results = []
        query_lower = query.lower()
        for item in self.short_term_memory:
            if query_lower in item.content.lower() or any(tag.lower() == query_lower for tag in item.tags):
                item.access_count += 1
                item.last_accessed = datetime.now()
                results.append(item.to_dict())
        if len(results) < limit:
            long_term_results = self._recall_long_term(query, limit - len(results))
            results.extend(long_term_results)
        results.sort(key=lambda x: (x["importance"], x["access_count"]), reverse=True)
        logger.debug(f"Recalled {len(results)} memory items")
        return results[:limit]
    
    def _store_long_term(self, item: MemoryItem):
        """Store item in long-term memory database."""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            tags_json = json.dumps(item.tags)
            cursor.execute("""
                INSERT INTO memories (content, type, importance, tags, created_at, access_count, last_accessed)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (item.content, item.memory_type, item.importance, tags_json, 
                   item.created_at, item.access_count, item.last_accessed))
            conn.commit()
            conn.close()
        except Exception as e:
            logger.error(f"Failed to store in long-term memory: {e}")
    
    def _recall_long_term(self, query: str, limit: int) -> List[Dict]:
        """Recall items from long-term memory database."""
        results = []
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute("""
                SELECT content, type, importance, tags, created_at, access_count, last_accessed
                FROM memories
                WHERE content LIKE ?
                ORDER BY importance DESC, access_count DESC
                LIMIT ?
            """, (f"%{query}%", limit))
            rows = cursor.fetchall()
            for row in rows:
                results.append({
                    "content": row[0],
                    "type": row[1],
                    "importance": row[2],
                    "tags": json.loads(row[3]),
                    "created_at": row[4],
                    "access_count": row[5],
                    "last_accessed": row[6],
                })
            conn.close()
        except Exception as e:
            logger.error(f"Failed to recall from long-term memory: {e}")
        return results
    
    def clear_short_term(self) -> int:
        """Clear short-term memory."""
        count = len(self.short_term_memory)
        self.short_term_memory.clear()
        logger.info(f"Cleared {count} items from short-term memory")
        return count
    
    def get_memory_stats(self) -> Dict[str, Any]:
        """Get memory statistics."""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM memories")
            long_term_count = cursor.fetchone()[0]
            conn.close()
        except:
            long_term_count = 0
        return {
            "short_term_items": len(self.short_term_memory),
            "short_term_capacity": self.max_short_term,
            "long_term_items": long_term_count,
            "long_term_capacity": self.max_long_term,
            "memory_initialized": True,
        }

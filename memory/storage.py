"""Storage backend for memory system."""
import logging
import sqlite3
import json
from typing import Any, Dict, List, Optional
from datetime import datetime, timedelta
from pathlib import Path

logger = logging.getLogger(__name__)


class StorageBackend:
    """SQLite-based storage backend for memory."""
    
    def __init__(self, db_path: str = "data/rex.db"):
        """Initialize storage backend.
        
        Args:
            db_path: Path to database file
        """
        self.db_path = db_path
        Path(self.db_path).parent.mkdir(parents=True, exist_ok=True)
        self._init_db()
        logger.info(f"Storage backend initialized at {db_path}")
    
    def _init_db(self) -> None:
        """Initialize database tables."""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                # Interactions table
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS interactions (
                        id TEXT PRIMARY KEY,
                        type TEXT,
                        content TEXT,
                        timestamp TEXT,
                        context TEXT,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    )
                """)
                
                # Learning table
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS learning (
                        id TEXT PRIMARY KEY,
                        type TEXT,
                        interaction_id TEXT,
                        feedback TEXT,
                        timestamp TEXT,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    )
                """)
                
                # Facts table
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS facts (
                        id TEXT PRIMARY KEY,
                        key TEXT UNIQUE,
                        value TEXT,
                        timestamp TEXT,
                        ttl INTEGER,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    )
                """)
                
                conn.commit()
        except Exception as e:
            logger.error(f"Database initialization failed: {e}")
            raise
    
    async def store(self, table: str, data: Dict[str, Any]) -> str:
        """Store data in database.
        
        Args:
            table: Table name
            data: Data to store
            
        Returns:
            Data ID
        """
        import uuid
        data_id = str(uuid.uuid4())
        
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                # Convert complex objects to JSON
                data_copy = data.copy()
                for key, value in data_copy.items():
                    if isinstance(value, (dict, list)):
                        data_copy[key] = json.dumps(value)
                
                # Build insert query
                columns = ["id"] + list(data_copy.keys())
                values = [data_id] + list(data_copy.values())
                placeholders = ",".join(["?" for _ in columns])
                
                query = f"INSERT INTO {table} ({','.join(columns)}) VALUES ({placeholders})"
                cursor.execute(query, values)
                conn.commit()
        except Exception as e:
            logger.error(f"Store failed for table {table}: {e}")
            raise
        
        return data_id
    
    async def retrieve(self, table: str, limit: int = 10) -> List[Dict[str, Any]]:
        """Retrieve data from database.
        
        Args:
            table: Table name
            limit: Limit number of results
            
        Returns:
            List of data
        """
        try:
            with sqlite3.connect(self.db_path) as conn:
                conn.row_factory = sqlite3.Row
                cursor = conn.cursor()
                
                query = f"SELECT * FROM {table} ORDER BY created_at DESC LIMIT ?"
                cursor.execute(query, (limit,))
                rows = cursor.fetchall()
                
                results = []
                for row in rows:
                    data = dict(row)
                    # Parse JSON fields
                    for key, value in data.items():
                        if isinstance(value, str) and value.startswith('{'):
                            try:
                                data[key] = json.loads(value)
                            except:
                                pass
                    results.append(data)
                
                return results
        except Exception as e:
            logger.error(f"Retrieve failed for table {table}: {e}")
            return []
    
    async def retrieve_by_field(self, table: str, field: str, value: Any) -> List[Dict[str, Any]]:
        """Retrieve data by field.
        
        Args:
            table: Table name
            field: Field name
            value: Field value
            
        Returns:
            List of matching data
        """
        try:
            with sqlite3.connect(self.db_path) as conn:
                conn.row_factory = sqlite3.Row
                cursor = conn.cursor()
                
                query = f"SELECT * FROM {table} WHERE {field} = ? ORDER BY created_at DESC"
                cursor.execute(query, (value,))
                rows = cursor.fetchall()
                
                return [dict(row) for row in rows]
        except Exception as e:
            logger.error(f"Retrieve by field failed: {e}")
            return []
    
    async def delete_old(self, table: str, days: int) -> int:
        """Delete old records.
        
        Args:
            table: Table name
            days: Delete records older than this many days
            
        Returns:
            Number of records deleted
        """
        try:
            cutoff_date = (datetime.now() - timedelta(days=days)).isoformat()
            
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                query = f"DELETE FROM {table} WHERE created_at < ?"
                cursor.execute(query, (cutoff_date,))
                conn.commit()
                
                return cursor.rowcount
        except Exception as e:
            logger.error(f"Delete old failed: {e}")
            return 0

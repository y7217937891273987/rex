"""Memory Manager - Handles storage and retrieval of information."""
import logging
from typing import Any, Dict, List, Optional
from datetime import datetime
import json
from memory.storage import StorageBackend

logger = logging.getLogger(__name__)


class MemoryManager:
    """Manages all memory and information storage for REX."""
    
    def __init__(self, storage: Optional[StorageBackend] = None):
        """Initialize Memory Manager.
        
        Args:
            storage: Storage backend
        """
        self.storage = storage or StorageBackend()
        self.interaction_cache: Dict[str, Any] = {}
        self.learning_cache: Dict[str, Any] = {}
        logger.info("Memory Manager initialized")
    
    async def store_interaction(self, interaction: Dict[str, Any]) -> str:
        """Store an interaction.
        
        Args:
            interaction: Interaction data
            
        Returns:
            Interaction ID
        """
        interaction_id = await self.storage.store("interactions", interaction)
        self.interaction_cache[interaction_id] = interaction
        logger.debug(f"Stored interaction: {interaction_id}")
        return interaction_id
    
    async def retrieve_interactions(self, limit: int = 10) -> str:
        """Retrieve recent interactions.
        
        Args:
            limit: Number of interactions to retrieve
            
        Returns:
            Formatted interactions string
        """
        interactions = await self.storage.retrieve("interactions", limit=limit)
        
        formatted = ""
        for interaction in interactions:
            formatted += f"[{interaction.get('timestamp', 'N/A')}] {interaction.get('type', 'N/A')}: {interaction.get('content', 'N/A')}\n"
        
        return formatted
    
    async def store_learning(self, learning: Dict[str, Any]) -> str:
        """Store a learning event.
        
        Args:
            learning: Learning data
            
        Returns:
            Learning ID
        """
        learning_id = await self.storage.store("learning", learning)
        self.learning_cache[learning_id] = learning
        logger.debug(f"Stored learning: {learning_id}")
        return learning_id
    
    async def retrieve_learning(self, limit: int = 10) -> List[Dict[str, Any]]:
        """Retrieve learning events.
        
        Args:
            limit: Number of events to retrieve
            
        Returns:
            List of learning events
        """
        return await self.storage.retrieve("learning", limit=limit)
    
    async def store_fact(self, key: str, value: Any, ttl: Optional[int] = None) -> None:
        """Store a fact/knowledge.
        
        Args:
            key: Fact key
            value: Fact value
            ttl: Time to live in seconds
        """
        fact = {
            "key": key,
            "value": value,
            "timestamp": datetime.now().isoformat(),
            "ttl": ttl
        }
        await self.storage.store("facts", fact)
        logger.debug(f"Stored fact: {key}")
    
    async def retrieve_fact(self, key: str) -> Optional[Any]:
        """Retrieve a fact.
        
        Args:
            key: Fact key
            
        Returns:
            Fact value or None
        """
        facts = await self.storage.retrieve_by_field("facts", "key", key)
        if facts:
            return facts[0].get("value")
        return None
    
    async def clear_old_interactions(self, days: int = 30) -> int:
        """Clear old interactions.
        
        Args:
            days: Remove interactions older than this many days
            
        Returns:
            Number of interactions removed
        """
        removed = await self.storage.delete_old("interactions", days)
        logger.info(f"Cleared {removed} old interactions")
        return removed
    
    async def get_statistics(self) -> Dict[str, Any]:
        """Get memory statistics.
        
        Returns:
            Statistics dictionary
        """
        interaction_count = len(await self.storage.retrieve("interactions", limit=10000))
        learning_count = len(await self.storage.retrieve("learning", limit=10000))
        
        return {
            "interactions": interaction_count,
            "learning_events": learning_count,
            "cache_size": len(self.interaction_cache) + len(self.learning_cache)
        }

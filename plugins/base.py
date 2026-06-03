"""Base plugin class for REX system."""
from abc import ABC, abstractmethod
from typing import Any, Dict, Optional
import logging

logger = logging.getLogger(__name__)


class BasePlugin(ABC):
    """Abstract base class for REX plugins."""
    
    def __init__(self, name: str, version: str = "1.0.0", description: str = ""):
        """Initialize plugin.
        
        Args:
            name: Plugin name
            version: Plugin version
            description: Plugin description
        """
        self.name = name
        self.version = version
        self.description = description
        self.enabled = False
        logger.info(f"Plugin {name} ({version}) initialized")
    
    @abstractmethod
    async def initialize(self) -> bool:
        """Initialize the plugin.
        
        Returns:
            Whether initialization was successful
        """
        pass
    
    @abstractmethod
    async def execute(self, command: str, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Execute a plugin command.
        
        Args:
            command: Command to execute
            params: Command parameters
            
        Returns:
            Execution result
        """
        pass
    
    @abstractmethod
    async def shutdown(self) -> bool:
        """Shutdown the plugin.
        
        Returns:
            Whether shutdown was successful
        """
        pass
    
    def get_info(self) -> Dict[str, Any]:
        """Get plugin information.
        
        Returns:
            Plugin info
        """
        return {
            "name": self.name,
            "version": self.version,
            "description": self.description,
            "enabled": self.enabled
        }

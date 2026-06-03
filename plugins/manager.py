"""Plugin Manager - Manages plugin loading and execution."""
import logging
from typing import Any, Dict, List, Optional
from plugins.base import BasePlugin

logger = logging.getLogger(__name__)


class PluginManager:
    """Manages plugin lifecycle and execution."""
    
    def __init__(self):
        """Initialize plugin manager."""
        self.plugins: Dict[str, BasePlugin] = {}
        logger.info("Plugin Manager initialized")
    
    async def register_plugin(self, plugin: BasePlugin) -> bool:
        """Register a plugin.
        
        Args:
            plugin: Plugin to register
            
        Returns:
            Whether registration was successful
        """
        try:
            success = await plugin.initialize()
            if success:
                self.plugins[plugin.name] = plugin
                plugin.enabled = True
                logger.info(f"Plugin registered: {plugin.name}")
                return True
            return False
        except Exception as e:
            logger.error(f"Plugin registration failed: {e}")
            return False
    
    async def execute_plugin(self, plugin_name: str, command: str, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Execute a plugin command.
        
        Args:
            plugin_name: Plugin name
            command: Command to execute
            params: Command parameters
            
        Returns:
            Execution result
        """
        if plugin_name not in self.plugins:
            logger.error(f"Plugin not found: {plugin_name}")
            return {"error": f"Plugin {plugin_name} not found"}
        
        plugin = self.plugins[plugin_name]
        if not plugin.enabled:
            logger.warning(f"Plugin disabled: {plugin_name}")
            return {"error": f"Plugin {plugin_name} is disabled"}
        
        try:
            result = await plugin.execute(command, params)
            return result
        except Exception as e:
            logger.error(f"Plugin execution failed: {e}")
            return {"error": str(e)}
    
    async def unregister_plugin(self, plugin_name: str) -> bool:
        """Unregister a plugin.
        
        Args:
            plugin_name: Plugin name
            
        Returns:
            Whether unregistration was successful
        """
        if plugin_name not in self.plugins:
            return False
        
        plugin = self.plugins[plugin_name]
        try:
            await plugin.shutdown()
            del self.plugins[plugin_name]
            logger.info(f"Plugin unregistered: {plugin_name}")
            return True
        except Exception as e:
            logger.error(f"Plugin unregistration failed: {e}")
            return False
    
    def get_plugin_list(self) -> List[Dict[str, Any]]:
        """Get list of all plugins.
        
        Returns:
            List of plugin info
        """
        return [plugin.get_info() for plugin in self.plugins.values()]

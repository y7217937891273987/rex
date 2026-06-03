#!/usr/bin/env python3
"""REX AI System - Main entry point.

JARVIS-style AI system with advanced capabilities:
- Natural language processing
- Multi-step reasoning
- Memory and learning
- Plugin system
- Autonomous agents
- Voice interface
- Self-modification with permission control
- API server
"""

import asyncio
import logging
from pathlib import Path
from typing import Optional

# Create required directories
Path("logs").mkdir(exist_ok=True)
Path("data").mkdir(exist_ok=True)
Path("plugins").mkdir(exist_ok=True)
Path("agents").mkdir(exist_ok=True)

# Setup logging
from utils.logger import setup_logging
setup_logging()

logger = logging.getLogger(__name__)

# Import core modules
from config.settings import settings
from security.permission_system import init_permission_system
from core.engine import AIEngine
from memory.manager import MemoryManager
from plugins.manager import PluginManager
from agents.manager import AgentManager
from voice.interface import VoiceInterface
from api.server import create_app


class REXSystem:
    """Main REX System coordinator."""
    
    def __init__(self):
        """Initialize REX system."""
        self.running = False
        self.ai_engine: Optional[AIEngine] = None
        self.memory_manager: Optional[MemoryManager] = None
        self.plugin_manager: Optional[PluginManager] = None
        self.agent_manager: Optional[AgentManager] = None
        self.voice_interface: Optional[VoiceInterface] = None
        self.flask_app = None
        
        logger.info("="*60)
        logger.info(f"REX AI System v{settings.PROJECT_VERSION}")
        logger.info(f"Environment: {settings.REX_ENV}")
        logger.info("="*60)
    
    async def initialize(self) -> bool:
        """Initialize all system components.
        
        Returns:
            Whether initialization was successful
        """
        try:
            logger.info("Initializing REX system...")
            
            # Validate settings
            valid, msg = settings.validate_critical_settings()
            if not valid:
                logger.error(f"Configuration error: {msg}")
                return False
            
            # Initialize permission system
            init_permission_system(
                admin_user=settings.REX_ADMIN_USER,
                require_permission=settings.REX_PERMISSION_REQUIRED
            )
            logger.info("✓ Permission system initialized")
            
            # Initialize memory
            self.memory_manager = MemoryManager()
            logger.info("✓ Memory manager initialized")
            
            # Initialize AI engine
            self.ai_engine = AIEngine(self.memory_manager)
            logger.info("✓ AI engine initialized")
            
            # Initialize plugin system
            self.plugin_manager = PluginManager()
            logger.info("✓ Plugin manager initialized")
            
            # Initialize agent system
            self.agent_manager = AgentManager()
            logger.info("✓ Agent manager initialized")
            
            # Initialize voice interface
            if settings.REX_VOICE_ENABLED:
                self.voice_interface = VoiceInterface()
                logger.info("✓ Voice interface initialized")
            
            # Create Flask app
            self.flask_app = create_app(self.ai_engine)
            self.flask_app.plugin_manager = self.plugin_manager
            self.flask_app.agent_manager = self.agent_manager
            logger.info("✓ API server created")
            
            self.running = True
            logger.info("\n" + "="*60)
            logger.info("REX System initialized successfully!")
            logger.info("="*60)
            return True
        
        except Exception as e:
            logger.error(f"Initialization failed: {e}", exc_info=True)
            return False
    
    async def run_server(self) -> None:
        """Run the Flask API server."""
        if not self.flask_app:
            logger.error("Flask app not initialized")
            return
        
        try:
            logger.info(f"\nStarting API server on {settings.REX_API_HOST}:{settings.REX_API_PORT}")
            logger.info(f"API Documentation: http://{settings.REX_API_HOST}:{settings.REX_API_PORT}/health")
            logger.info(f"Chat Endpoint: POST http://{settings.REX_API_HOST}:{settings.REX_API_PORT}/api/v1/chat")
            logger.info("\nSending chat request:")
            logger.info("curl -X POST http://localhost:5000/api/v1/chat -H 'Content-Type: application/json' -d '{\"message\": \"Hello REX\"}'")
            
            # Run Flask app
            self.flask_app.run(
                host=settings.REX_API_HOST,
                port=settings.REX_API_PORT,
                debug=settings.is_development,
                use_reloader=False
            )
        except Exception as e:
            logger.error(f"Server error: {e}", exc_info=True)
    
    async def interactive_mode(self) -> None:
        """Run in interactive mode."""
        logger.info("\nStarting interactive mode...")
        logger.info("Type 'exit' to quit")
        logger.info()
        
        while self.running:
            try:
                user_input = input("You: ").strip()
                
                if not user_input:
                    continue
                
                if user_input.lower() in ['exit', 'quit', 'bye']:
                    logger.info("Shutting down...")
                    self.running = False
                    break
                
                # Process input
                response = await self.ai_engine.process_input(user_input)
                print(f"\nREX: {response['response']}\n")
            
            except KeyboardInterrupt:
                logger.info("\nShutting down...")
                self.running = False
                break
            except Exception as e:
                logger.error(f"Error: {e}")
    
    async def shutdown(self) -> None:
        """Shutdown the system gracefully.
        
        Returns:
            None
        """
        logger.info("\nShutting down REX system...")
        self.running = False
        
        if self.memory_manager:
            stats = await self.memory_manager.get_statistics()
            logger.info(f"Memory stats: {stats}")
        
        logger.info("REX system shutdown complete.")


async def main() -> None:
    """Main entry point."""
    system = REXSystem()
    
    # Initialize
    if not await system.initialize():
        logger.error("Failed to initialize REX system")
        return
    
    try:
        # Run in server mode (default)
        await system.run_server()
        # Alternatively, run in interactive mode:
        # await system.interactive_mode()
    except KeyboardInterrupt:
        logger.info("\nReceived interrupt signal")
    finally:
        await system.shutdown()


if __name__ == "__main__":
    # Run the system
    asyncio.run(main())

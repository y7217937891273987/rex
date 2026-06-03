"""
AI Engine - Main orchestrator for REX AI System.
"""

import logging
from typing import Dict, Any, Optional
from datetime import datetime

from core.nlp import NLPEngine
from core.memory import MemorySystem
from core.reasoning import ReasoningEngine
from security.permission_system import PermissionManager, request_permission

logger = logging.getLogger(__name__)


class AIEngine:
    """Main AI Engine - Orchestrates all core systems."""
    
    def __init__(self, permission_manager: PermissionManager):
        """Initialize the AI Engine."""
        self.permission_manager = permission_manager
        self.nlp_engine = NLPEngine()
        self.memory_system = MemorySystem()
        self.reasoning_engine = ReasoningEngine()
        
        self.initialized = False
        self.query_count = 0
        self.start_time = None
        
        logger.info("AIEngine created")
    
    def initialize(self) -> bool:
        """
        Initialize the engine.
        
        Returns:
            True if initialization successful
        """
        try:
            logger.info("Initializing AIEngine systems...")
            
            # Verify permission manager
            if not self.permission_manager:
                logger.error("Permission manager not provided")
                return False
            
            # Initialize memory
            memory_stats = self.memory_system.get_memory_stats()
            logger.info(f"Memory system initialized: {memory_stats}")
            
            self.initialized = True
            self.start_time = datetime.now()
            
            logger.info("AIEngine initialized successfully")
            return True
        except Exception as e:
            logger.error(f"Failed to initialize AIEngine: {e}")
            return False
    
    def process(self, user_input: str) -> str:
        """
        Process user input through the AI pipeline.
        
        Args:
            user_input: User's natural language input
            
        Returns:
            AI response
        """
        if not self.initialized:
            return "Error: Engine not initialized"
        
        try:
            self.query_count += 1
            logger.info(f"Processing query #{self.query_count}: {user_input}")
            
            # Step 1: Parse query with NLP
            parsed_query = self.nlp_engine.parse_query(user_input)
            logger.debug(f"Parsed query type: {parsed_query.query_type.value}")
            
            # Step 2: Recall relevant memory
            context = self.memory_system.recall(parsed_query.intent, limit=5)
            logger.debug(f"Retrieved {len(context)} context items")
            
            # Step 3: Check permissions if needed
            if parsed_query.query_type.name == "COMMAND_EXECUTION":
                if not request_permission("external_api_call", f"Execute command: {user_input}"):
                    return "Permission denied for this command."
            
            # Step 4: Apply reasoning
            conclusion, confidence = self.reasoning_engine.reason(user_input)
            
            # Step 5: Build response
            response = self._generate_response(parsed_query, conclusion, confidence)
            
            # Step 6: Store interaction in memory
            self.memory_system.remember(
                f"Q: {user_input}\\nA: {response}",
                memory_type="interaction",
                importance=confidence,
                persist=True
            )
            
            logger.info(f"Query processed successfully (confidence: {confidence})")
            return response
        
        except Exception as e:
            logger.error(f"Error processing query: {e}")
            return f"Error processing your request: {str(e)}"
    
    def _generate_response(self, parsed_query, conclusion: str, confidence: float) -> str:
        """Generate a response based on reasoning."""
        response = f"Based on {parsed_query.query_type.value}:\\n{conclusion}"
        
        if confidence >= 0.8:
            response += "\\n[Confidence: HIGH ✓]"
        elif confidence >= 0.6:
            response += "\\n[Confidence: MEDIUM]"
        else:
            response += "\\n[Confidence: LOW]"
        
        return response
    
    def get_status(self) -> str:
        """
        Get system status.
        
        Returns:
            Status string
        """
        if not self.initialized:
            return "Engine not initialized"
        
        uptime = (datetime.now() - self.start_time).total_seconds()
        memory_stats = self.memory_system.get_memory_stats()
        reasoning_trace = self.reasoning_engine.get_reasoning_trace()
        
        status = f"""
╔════════════════════════════════════╗
║        REX System Status           ║
╚════════════════════════════════════╝

Status: RUNNING ✓
Uptime: {int(uptime)}s
Queries Processed: {self.query_count}
Last Activity: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

Memory Status:
- Short-term items: {memory_stats['short_term_items']}
- Memory initialized: {memory_stats['memory_initialized']}

Reasoning:
- Last paths used: {', '.join(reasoning_trace['paths_used'])}
- Average confidence: {reasoning_trace['avg_confidence']:.2%}

Components: All Operational ✓
        """
        return status
    
    def shutdown(self):
        """Shutdown the engine gracefully."""
        logger.info(f"Shutting down AIEngine - Processed {self.query_count} queries")
        self.initialized = False

"""Core AI Engine - Main intelligence hub for REX system."""
import logging
from typing import Any, Dict, List, Optional
from datetime import datetime
from config.settings import settings
from core.llm_manager import LLMManager
from core.reasoning import ReasoningEngine
from memory.manager import MemoryManager
from security.permission_system import request_permission

logger = logging.getLogger(__name__)


class AIEngine:
    """Core AI Engine for REX system."""
    
    def __init__(self, memory_manager: Optional[MemoryManager] = None):
        """Initialize AI Engine.
        
        Args:
            memory_manager: Memory manager instance
        """
        self.llm_manager = LLMManager(settings.OPENAI_API_KEY, settings.OPENAI_MODEL)
        self.reasoning_engine = ReasoningEngine()
        self.memory_manager = memory_manager or MemoryManager()
        self.conversation_history: List[Dict[str, str]] = []
        self.context_window = 10  # Keep last 10 messages
        logger.info("AI Engine initialized")
    
    async def process_input(self, user_input: str, context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Process user input and generate response.
        
        Args:
            user_input: User input message
            context: Additional context
            
        Returns:
            Response dictionary
        """
        logger.info(f"Processing input: {user_input[:100]}...")
        
        # Store in memory
        await self.memory_manager.store_interaction({
            "type": "input",
            "content": user_input,
            "timestamp": datetime.now().isoformat(),
            "context": context
        })
        
        # Add to conversation history
        self.conversation_history.append({"role": "user", "content": user_input})
        
        # Apply reasoning
        reasoning_result = await self.reasoning_engine.reason(user_input, context)
        
        # Get response from LLM
        messages = self._prepare_messages(user_input)
        response = await self.llm_manager.get_completion(
            messages=messages,
            temperature=settings.OPENAI_TEMPERATURE,
            max_tokens=settings.OPENAI_MAX_TOKENS
        )
        
        # Store response
        await self.memory_manager.store_interaction({
            "type": "output",
            "content": response,
            "timestamp": datetime.now().isoformat(),
            "reasoning": reasoning_result
        })
        
        # Add to history
        self.conversation_history.append({"role": "assistant", "content": response})
        
        # Maintain context window
        if len(self.conversation_history) > self.context_window * 2:
            self.conversation_history = self.conversation_history[-self.context_window * 2:]
        
        return {
            "response": response,
            "reasoning": reasoning_result,
            "timestamp": datetime.now().isoformat()
        }
    
    def _prepare_messages(self, current_input: str) -> List[Dict[str, str]]:
        """Prepare messages for LLM.
        
        Args:
            current_input: Current user input
            
        Returns:
            List of message dictionaries
        """
        messages = [
            {
                "role": "system",
                "content": "You are REX, an advanced AI assistant based on JARVIS. You are helpful, intelligent, and autonomous. You can think critically, learn from interactions, and improve yourself when given permission. Maintain a professional and helpful tone."
            }
        ]
        
        # Add recent conversation history
        messages.extend(self.conversation_history[-self.context_window:])
        
        return messages
    
    async def learn_from_feedback(self, feedback: str, interaction_id: str) -> bool:
        """Learn from user feedback.
        
        Args:
            feedback: User feedback
            interaction_id: ID of the interaction being reviewed
            
        Returns:
            Whether learning was successful
        """
        if not request_permission("modify_core_logic", f"Learning from feedback: {feedback[:50]}"):
            logger.warning("Permission denied for learning")
            return False
        
        await self.memory_manager.store_learning({
            "type": "feedback",
            "interaction_id": interaction_id,
            "feedback": feedback,
            "timestamp": datetime.now().isoformat()
        })
        
        logger.info(f"Learned from feedback: {feedback[:50]}...")
        return True
    
    async def get_summary(self, topic: str = "") -> str:
        """Get a summary of interactions.
        
        Args:
            topic: Topic to summarize
            
        Returns:
            Summary string
        """
        interactions = await self.memory_manager.retrieve_interactions(limit=50)
        
        if not interactions:
            return "No interactions to summarize."
        
        summary_prompt = f"""Summarize the following interactions{f' about {topic}' if topic else ''}:

{interactions}

Provide a concise summary."""
        
        summary = await self.llm_manager.get_completion(
            messages=[{"role": "user", "content": summary_prompt}]
        )
        
        return summary

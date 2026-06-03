"""Base agent class for autonomous agents."""
from abc import ABC, abstractmethod
from typing import Any, Dict, Optional, List
import logging
from datetime import datetime

logger = logging.getLogger(__name__)


class BaseAgent(ABC):
    """Abstract base class for autonomous agents."""
    
    def __init__(self, name: str, description: str = "", goal: str = ""):
        """Initialize agent.
        
        Args:
            name: Agent name
            description: Agent description
            goal: Agent goal
        """
        self.name = name
        self.description = description
        self.goal = goal
        self.active = False
        self.task_queue: List[Dict[str, Any]] = []
        self.execution_history: List[Dict[str, Any]] = []
        logger.info(f"Agent {name} initialized")
    
    @abstractmethod
    async def initialize(self) -> bool:
        """Initialize the agent.
        
        Returns:
            Whether initialization was successful
        """
        pass
    
    @abstractmethod
    async def execute_task(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Execute a task.
        
        Args:
            task: Task to execute
            
        Returns:
            Task result
        """
        pass
    
    async def add_task(self, task: Dict[str, Any]) -> str:
        """Add a task to the queue.
        
        Args:
            task: Task to add
            
        Returns:
            Task ID
        """
        import uuid
        task_id = str(uuid.uuid4())
        task['id'] = task_id
        task['created_at'] = datetime.now().isoformat()
        self.task_queue.append(task)
        logger.debug(f"Task added to {self.name}: {task_id}")
        return task_id
    
    async def process_tasks(self) -> List[Dict[str, Any]]:
        """Process all tasks in the queue.
        
        Returns:
            List of task results
        """
        results = []
        while self.task_queue:
            task = self.task_queue.pop(0)
            result = await self.execute_task(task)
            self.execution_history.append(result)
            results.append(result)
        return results
    
    def get_info(self) -> Dict[str, Any]:
        """Get agent information.
        
        Returns:
            Agent info
        """
        return {
            "name": self.name,
            "description": self.description,
            "goal": self.goal,
            "active": self.active,
            "pending_tasks": len(self.task_queue),
            "completed_tasks": len(self.execution_history)
        }

"""Agent Manager - Manages autonomous agents."""
import logging
from typing import Any, Dict, List, Optional
from agents.base import BaseAgent

logger = logging.getLogger(__name__)


class AgentManager:
    """Manages autonomous agent lifecycle and coordination."""
    
    def __init__(self):
        """Initialize agent manager."""
        self.agents: Dict[str, BaseAgent] = {}
        logger.info("Agent Manager initialized")
    
    async def register_agent(self, agent: BaseAgent) -> bool:
        """Register an agent.
        
        Args:
            agent: Agent to register
            
        Returns:
            Whether registration was successful
        """
        try:
            success = await agent.initialize()
            if success:
                self.agents[agent.name] = agent
                agent.active = True
                logger.info(f"Agent registered: {agent.name}")
                return True
            return False
        except Exception as e:
            logger.error(f"Agent registration failed: {e}")
            return False
    
    async def assign_task(self, agent_name: str, task: Dict[str, Any]) -> str:
        """Assign a task to an agent.
        
        Args:
            agent_name: Agent name
            task: Task to assign
            
        Returns:
            Task ID
        """
        if agent_name not in self.agents:
            logger.error(f"Agent not found: {agent_name}")
            raise ValueError(f"Agent {agent_name} not found")
        
        agent = self.agents[agent_name]
        task_id = await agent.add_task(task)
        return task_id
    
    async def process_agent_tasks(self, agent_name: str) -> List[Dict[str, Any]]:
        """Process tasks for an agent.
        
        Args:
            agent_name: Agent name
            
        Returns:
            List of task results
        """
        if agent_name not in self.agents:
            logger.error(f"Agent not found: {agent_name}")
            return []
        
        agent = self.agents[agent_name]
        results = await agent.process_tasks()
        return results
    
    def get_agent_list(self) -> List[Dict[str, Any]]:
        """Get list of all agents.
        
        Returns:
            List of agent info
        """
        return [agent.get_info() for agent in self.agents.values()]

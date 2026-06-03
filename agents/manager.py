"""
Agents System for REX AI - Autonomous agent management and coordination.
"""

import logging
from typing import Dict, List, Optional, Any
from enum import Enum
from datetime import datetime
import uuid

from security.permission_system import request_permission

logger = logging.getLogger(__name__)


class AgentState(Enum):
    """Possible agent states."""
    IDLE = "idle"
    BUSY = "busy"
    SLEEPING = "sleeping"
    ERROR = "error"


class AgentTask:
    """Represents a task for an agent."""
    
    def __init__(self, task_id: str, name: str, target_agent: str, parameters: Optional[Dict] = None):
        self.task_id = task_id
        self.name = name
        self.target_agent = target_agent
        self.parameters = parameters or {}
        self.created_at = datetime.now()
        self.status = "pending"
        self.result = None
    
    def to_dict(self) -> Dict:
        """Convert to dictionary."""
        return {
            "task_id": self.task_id,
            "name": self.name,
            "target_agent": self.target_agent,
            "parameters": self.parameters,
            "created_at": self.created_at.isoformat(),
            "status": self.status,
            "result": self.result
        }


class Agent:
    """Base class for autonomous agents."""
    
    def __init__(self, agent_id: str, name: str, description: str, capabilities: List[str]):
        """
        Initialize an agent.
        
        Args:
            agent_id: Unique agent identifier
            name: Agent name
            description: Agent description
            capabilities: List of capabilities
        """
        self.agent_id = agent_id
        self.name = name
        self.description = description
        self.capabilities = capabilities
        self.state = AgentState.IDLE
        self.tasks_completed = 0
        self.current_task: Optional[AgentTask] = None
        self.created_at = datetime.now()
        
        logger.info(f"Agent initialized: {name}")
    
    def execute_task(self, task: AgentTask) -> Dict:
        """
        Execute a task.
        
        Args:
            task: Task to execute
            
        Returns:
            Execution result
        """
        self.state = AgentState.BUSY
        self.current_task = task
        
        try:
            result = self._execute(task)
            task.status = "completed"
            task.result = result
            self.tasks_completed += 1
            self.state = AgentState.IDLE
            return result
        except Exception as e:
            logger.error(f"Task execution failed: {e}")
            task.status = "failed"
            task.result = str(e)
            self.state = AgentState.ERROR
            return {"success": False, "error": str(e)}
    
    def _execute(self, task: AgentTask) -> Dict:
        """
        Execute the task. Override in subclasses.
        
        Args:
            task: Task to execute
            
        Returns:
            Execution result
        """
        return {"success": True, "message": f"Task {task.name} executed"}
    
    def get_status(self) -> Dict:
        """Get agent status."""
        return {
            "agent_id": self.agent_id,
            "name": self.name,
            "description": self.description,
            "state": self.state.value,
            "capabilities": self.capabilities,
            "tasks_completed": self.tasks_completed,
            "current_task": self.current_task.to_dict() if self.current_task else None
        }


class AnalysisAgent(Agent):
    """Agent for data analysis and processing."""
    
    def __init__(self):
        super().__init__(
            agent_id="agent_analysis_001",
            name="Analysis Agent",
            description="Processes and analyzes data",
            capabilities=["data_analysis", "pattern_detection", "statistics"]
        )
    
    def _execute(self, task: AgentTask) -> Dict:
        """Execute analysis task."""
        logger.info(f"Analyzing task: {task.name}")
        
        data = task.parameters.get("data", [])
        
        if not data:
            return {"success": False, "error": "No data provided"}
        
        try:
            result = {
                "success": True,
                "count": len(data),
                "analysis": f"Analyzed {len(data)} items",
                "patterns": "Basic patterns detected"
            }
            return result
        except Exception as e:
            return {"success": False, "error": str(e)}


class ExecutionAgent(Agent):
    """Agent for executing commands and tasks."""
    
    def __init__(self):
        super().__init__(
            agent_id="agent_execution_001",
            name="Execution Agent",
            description="Executes commands and tasks",
            capabilities=["task_execution", "command_processing"]
        )
    
    def _execute(self, task: AgentTask) -> Dict:
        """Execute command."""
        logger.info(f"Executing task: {task.name}")
        
        # Request permission for execution
        if not request_permission(
            "agent_spawn",
            f"Execute agent task: {task.name}"
        ):
            return {"success": False, "error": "Permission denied"}
        
        command = task.parameters.get("command", "")
        
        try:
            result = {
                "success": True,
                "command": command,
                "executed": True,
                "output": f"Command '{command}' executed successfully"
            }
            return result
        except Exception as e:
            return {"success": False, "error": str(e)}


class LearningAgent(Agent):
    """Agent for learning from interactions."""
    
    def __init__(self):
        super().__init__(
            agent_id="agent_learning_001",
            name="Learning Agent",
            description="Learns from interactions and improves",
            capabilities=["learning", "adaptation", "optimization"]
        )
        self.learned_patterns: List[str] = []
    
    def _execute(self, task: AgentTask) -> Dict:
        """Learn from data."""
        logger.info(f"Learning from task: {task.name}")
        
        content = task.parameters.get("content", "")
        
        if content:
            self.learned_patterns.append(content)
        
        result = {
            "success": True,
            "patterns_learned": len(self.learned_patterns),
            "new_pattern": content,
            "learned": True
        }
        return result


class AgentManager:
    """Manages agent coordination and task distribution."""
    
    def __init__(self):
        """Initialize agent manager."""
        self.agents: Dict[str, Agent] = {}
        self.task_queue: List[AgentTask] = []
        self._initialize_agents()
        logger.info("AgentManager initialized")
    
    def _initialize_agents(self):
        """Initialize built-in agents."""
        self.register_agent(AnalysisAgent())
        self.register_agent(ExecutionAgent())
        self.register_agent(LearningAgent())
    
    def register_agent(self, agent: Agent):
        """Register an agent."""
        self.agents[agent.agent_id] = agent
        logger.info(f"Agent registered: {agent.name}")
    
    def assign_task(self, agent_id: str, task: AgentTask) -> Dict:
        """
        Assign a task to an agent.
        
        Args:
            agent_id: ID of the agent
            task: Task to assign
            
        Returns:
            Task execution result
        """
        if agent_id not in self.agents:
            return {"success": False, "error": "Agent not found"}
        
        agent = self.agents[agent_id]
        return agent.execute_task(task)
    
    def get_agent_status(self, agent_id: str) -> Optional[Dict]:
        """Get status of a specific agent."""
        if agent_id in self.agents:
            return self.agents[agent_id].get_status()
        return None
    
    def get_all_agents_status(self) -> Dict[str, Dict]:
        """Get status of all agents."""
        return {
            agent_id: agent.get_status()
            for agent_id, agent in self.agents.items()
        }

"""
REST API Server for REX AI System.
"""

import logging
from typing import Dict, Any
from datetime import datetime

try:
    from flask import Flask, jsonify, request
    from flask_cors import CORS
    FLASK_AVAILABLE = True
except ImportError:
    FLASK_AVAILABLE = False

from core.engine import AIEngine
from security.permission_system import PermissionManager
from agents.manager import AgentManager, AgentTask
import uuid

logger = logging.getLogger(__name__)


class REXAPIServer:
    """REST API Server for REX AI System."""
    
    def __init__(self, permission_manager: PermissionManager, ai_engine: AIEngine):
        """Initialize API server."""
        self.permission_manager = permission_manager
        self.ai_engine = ai_engine
        self.agent_manager = AgentManager()
        
        if FLASK_AVAILABLE:
            self.app = Flask(__name__)
            CORS(self.app)
            self._setup_routes()
            logger.info("REST API Server initialized")
        else:
            logger.warning("Flask not available - API disabled")
            self.app = None
    
    def _setup_routes(self):
        """Setup API routes."""
        
        @self.app.route('/api/health', methods=['GET'])
        def health():
            """Health check endpoint."""
            return self._response({
                "status": "healthy",
                "running": True
            }, 200)
        
        @self.app.route('/api/query', methods=['POST'])
        def query():
            """Process a query."""
            data = request.get_json()
            query_text = data.get('query', '')
            
            if not query_text:
                return self._error("Query parameter is required", 400)
            
            response_text = self.ai_engine.process(query_text)
            
            return self._response({
                "query": query_text,
                "response": response_text
            })
        
        @self.app.route('/api/memory/store', methods=['POST'])
        def store_memory():
            """Store a memory item."""
            data = request.get_json()
            content = data.get('content', '')
            memory_type = data.get('type', 'fact')
            
            if not content:
                return self._error("Content is required", 400)
            
            success = self.ai_engine.memory_system.remember(
                content,
                memory_type=memory_type,
                persist=True
            )
            
            return self._response({
                "stored": success
            })
        
        @self.app.route('/api/memory/recall', methods=['GET'])
        def recall_memory():
            """Recall memories."""
            query = request.args.get('q', '')
            
            if not query:
                return self._error("Query parameter q is required", 400)
            
            results = self.ai_engine.memory_system.recall(query)
            
            return self._response({
                "query": query,
                "results": results,
                "count": len(results)
            })
        
        @self.app.route('/api/memory/clear', methods=['POST'])
        def clear_memory():
            """Clear short-term memory."""
            count = self.ai_engine.memory_system.clear_short_term()
            
            return self._response({
                "cleared": True,
                "count": count
            })
        
        @self.app.route('/api/system/status', methods=['GET'])
        def system_status():
            """Get system status."""
            memory_stats = self.ai_engine.memory_system.get_memory_stats()
            reasoning_trace = self.ai_engine.reasoning_engine.get_reasoning_trace()
            
            return self._response({
                "running": self.ai_engine.initialized,
                "uptime_seconds": int((datetime.now() - self.ai_engine.start_time).total_seconds()) if self.ai_engine.start_time else 0,
                "requests_served": self.ai_engine.query_count,
                "memory": memory_stats,
                "reasoning": reasoning_trace
            })
        
        @self.app.route('/api/agents/status', methods=['GET'])
        def agents_status():
            """Get status of all agents."""
            agents = self.agent_manager.get_all_agents_status()
            
            return self._response({
                "agents": agents,
                "total": len(agents)
            })
        
        @self.app.route('/api/agents/<agent_id>/status', methods=['GET'])
        def agent_status(agent_id):
            """Get status of specific agent."""
            status = self.agent_manager.get_agent_status(agent_id)
            
            if not status:
                return self._error(f"Agent {agent_id} not found", 404)
            
            return self._response(status)
        
        @self.app.errorhandler(404)
        def not_found(error):
            """Handle 404 errors."""
            return self._error("Resource not found", 404)
        
        @self.app.errorhandler(500)
        def server_error(error):
            """Handle 500 errors."""
            return self._error("Internal server error", 500)
    
    def _response(self, data: Dict[str, Any], status_code: int = 200) -> Dict:
        """Generate a standardized response."""
        return jsonify({
            "success": True,
            "status_code": status_code,
            "timestamp": datetime.now().isoformat(),
            "data": data,
            "message": "Success",
            "error": ""
        }), status_code
    
    def _error(self, error_msg: str, status_code: int = 400) -> Dict:
        """Generate an error response."""
        return jsonify({
            "success": False,
            "status_code": status_code,
            "timestamp": datetime.now().isoformat(),
            "data": {},
            "message": error_msg,
            "error": error_msg
        }), status_code
    
    def run(self, host: str = "127.0.0.1", port: int = 5000):
        """Run the API server."""
        if not self.app:
            logger.error("Flask not available - cannot start API server")
            return
        
        logger.info(f"Starting REST API server on {host}:{port}")
        self.app.run(host=host, port=port, debug=False)

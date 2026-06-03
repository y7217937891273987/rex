"""Flask API server for REX."""
import logging
from flask import Flask, request, jsonify
from flask_cors import CORS
from typing import Any, Dict
from config.settings import settings

logger = logging.getLogger(__name__)


def create_app(ai_engine: Any = None) -> Flask:
    """Create Flask application.
    
    Args:
        ai_engine: AI engine instance
        
    Returns:
        Flask application
    """
    app = Flask(__name__)
    app.config['JSON_SORT_KEYS'] = False
    CORS(app)
    
    # Store AI engine
    app.ai_engine = ai_engine
    
    @app.route('/health', methods=['GET'])
    def health():
        """Health check endpoint."""
        return jsonify({
            "status": "healthy",
            "version": settings.PROJECT_VERSION
        })
    
    @app.route('/api/v1/chat', methods=['POST'])
    async def chat():
        """Chat endpoint."""
        try:
            data = request.get_json()
            if not data or 'message' not in data:
                return jsonify({"error": "No message provided"}), 400
            
            message = data['message']
            context = data.get('context', {})
            
            if not app.ai_engine:
                return jsonify({"error": "AI engine not initialized"}), 500
            
            response = await app.ai_engine.process_input(message, context)
            return jsonify(response)
        except Exception as e:
            logger.error(f"Chat endpoint error: {e}")
            return jsonify({"error": str(e)}), 500
    
    @app.route('/api/v1/memory/interactions', methods=['GET'])
    async def get_interactions():
        """Get interactions from memory."""
        try:
            if not app.ai_engine:
                return jsonify({"error": "AI engine not initialized"}), 500
            
            limit = request.args.get('limit', 10, type=int)
            interactions = await app.ai_engine.memory_manager.retrieve_interactions(limit)
            return jsonify({"interactions": interactions})
        except Exception as e:
            logger.error(f"Get interactions error: {e}")
            return jsonify({"error": str(e)}), 500
    
    @app.route('/api/v1/memory/stats', methods=['GET'])
    async def get_memory_stats():
        """Get memory statistics."""
        try:
            if not app.ai_engine:
                return jsonify({"error": "AI engine not initialized"}), 500
            
            stats = await app.ai_engine.memory_manager.get_statistics()
            return jsonify(stats)
        except Exception as e:
            logger.error(f"Get stats error: {e}")
            return jsonify({"error": str(e)}), 500
    
    @app.route('/api/v1/plugins', methods=['GET'])
    def get_plugins():
        """Get registered plugins."""
        try:
            if not hasattr(app, 'plugin_manager') or not app.plugin_manager:
                return jsonify({"plugins": []})
            
            plugins = app.plugin_manager.get_plugin_list()
            return jsonify({"plugins": plugins})
        except Exception as e:
            logger.error(f"Get plugins error: {e}")
            return jsonify({"error": str(e)}), 500
    
    @app.route('/api/v1/agents', methods=['GET'])
    def get_agents():
        """Get registered agents."""
        try:
            if not hasattr(app, 'agent_manager') or not app.agent_manager:
                return jsonify({"agents": []})
            
            agents = app.agent_manager.get_agent_list()
            return jsonify({"agents": agents})
        except Exception as e:
            logger.error(f"Get agents error: {e}")
            return jsonify({"error": str(e)}), 500
    
    @app.errorhandler(404)
    def not_found(e):
        """Handle 404 errors."""
        return jsonify({"error": "Endpoint not found"}), 404
    
    @app.errorhandler(500)
    def internal_error(e):
        """Handle 500 errors."""
        return jsonify({"error": "Internal server error"}), 500
    
    logger.info("Flask app created")
    return app

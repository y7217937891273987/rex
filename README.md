# REX AI System

A modular, extensible JARVIS-style AI system with advanced capabilities including autonomous reasoning, memory management, plugin architecture, voice interface, and permission-based self-modification.

## Features

- **Core AI Engine**: Advanced language model integration with OpenAI GPT-4
- **Reasoning Engine**: Multi-step logical reasoning for complex problems
- **Memory System**: Persistent storage with interaction history and learning capabilities
- **Plugin System**: Extensible architecture for custom functionality
- **Autonomous Agents**: Task-based agents that can operate independently
- **Voice Interface**: Speech recognition and text-to-speech capabilities
- **Security Layer**: Permission-based access control for sensitive operations
- **Self-Modification**: Code analysis and generation with permission gates
- **API Server**: RESTful API for integration with other systems

## Quick Start

### Prerequisites

- Python 3.8+
- OpenAI API key
- pip (Python package manager)

### Installation

1. Clone the repository:
```bash
git clone <repo-url>
cd rex
```

2. Create virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\\Scripts\\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Configure environment:
```bash
cp .env.example .env
# Edit .env and add your OpenAI API key
```

### Running REX

#### API Server Mode (Default)
```bash
python main.py
```

The server will start at `http://localhost:5000`

#### Interactive Mode
Edit `main.py` and change:
```python
await system.run_server()
```
to:
```python
await system.interactive_mode()
```

### API Endpoints

#### Health Check
```bash
GET /health
```

#### Chat
```bash
POST /api/v1/chat
Content-Type: application/json

{
  "message": "Hello REX",
  "context": {}
}
```

#### Memory Interactions
```bash
GET /api/v1/memory/interactions?limit=10
```

#### Memory Statistics
```bash
GET /api/v1/memory/stats
```

#### Plugins
```bash
GET /api/v1/plugins
```

#### Agents
```bash
GET /api/v1/agents
```

## Project Structure

```
rex/
├── config/              # Configuration management
├── core/               # Core AI engine
├── security/           # Permission system & encryption
├── memory/             # Memory management system
├── plugins/            # Plugin framework
├── agents/             # Autonomous agents
├── voice/              # Voice interface
├── api/                # REST API server
├── self_expansion/     # Self-modification system
├── utils/              # Utility functions
├── main.py             # Entry point
├── requirements.txt    # Python dependencies
├── .env.example        # Example configuration
└── README.md           # This file
```

## Configuration

Edit `.env` file to configure:

```env
# OpenAI Configuration
OPENAI_API_KEY=your_key_here
OPENAI_MODEL=gpt-4-turbo-preview

# REX Configuration
REX_ENV=development
REX_LOG_LEVEL=INFO
REX_API_PORT=5000
REX_API_HOST=0.0.0.0

# Security
REX_PERMISSION_REQUIRED=true
REX_ADMIN_USER=admin

# Voice
REX_VOICE_ENABLED=true
REX_VOICE_RATE=150

# Self-Modification
REX_SELF_MODIFY_ENABLED=true
REX_CODE_REVIEW_REQUIRED=true
```

## Permission System

All sensitive operations require permission:

```python
from security.permission_system import request_permission

# Request permission for an action
if request_permission("modify_core_logic", "Description of action"):
    # Perform sensitive operation
    pass
else:
    # Permission denied
    pass
```

## Creating Custom Plugins

```python
from plugins.base import BasePlugin
from typing import Any, Dict, Optional

class MyPlugin(BasePlugin):
    async def initialize(self) -> bool:
        return True
    
    async def execute(self, command: str, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        return {"result": "success"}
    
    async def shutdown(self) -> bool:
        return True
```

## Creating Custom Agents

```python
from agents.base import BaseAgent
from typing import Any, Dict

class MyAgent(BaseAgent):
    async def initialize(self) -> bool:
        return True
    
    async def execute_task(self, task: Dict[str, Any]) -> Dict[str, Any]:
        return {"task_id": task.get("id"), "result": "completed"}
```

## Development

### Running Tests
```bash
pytest
```

### Code Style
Follow PEP 8 and maintain docstrings for all functions.

## Security Considerations

1. Always use permission system for sensitive operations
2. Keep `REX_SECRET_KEY` secure in production
3. Enable `REX_PERMISSION_REQUIRED` in production
4. Regularly review audit logs
5. Use HTTPS in production

## Performance Tips

1. Adjust memory retention with `REX_MEMORY_MAX_ITEMS`
2. Enable Redis for distributed caching
3. Use async/await for I/O operations
4. Monitor logs for bottlenecks

## Troubleshooting

### OpenAI API errors
- Check API key in `.env`
- Verify API key has proper permissions
- Check rate limits

### Voice issues
- Ensure microphone is connected and working
- Check audio permissions
- Try adjusting `REX_VOICE_RATE`

### Memory issues
- Check database file permissions
- Run memory cleanup: `memory_manager.clear_old_interactions()`
- Monitor disk space

## Contributing

Contributions are welcome! Please:
1. Follow the project architecture
2. Add tests for new features
3. Update documentation
4. Use permission system for sensitive operations

## License

MIT License - See LICENSE file for details

## Support

For issues and feature requests, please use GitHub Issues.

## Roadmap

- [ ] Multi-language support
- [ ] Advanced reasoning strategies
- [ ] Distributed agent network
- [ ] Advanced visualization UI
- [ ] Cloud deployment options
- [ ] Plugin marketplace

## Credits

Inspired by JARVIS and built with modern AI best practices.

---

**REX: Your Autonomous AI Assistant**

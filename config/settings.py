"""
Configuration settings for REX AI System.
"""

import os
from typing import Dict, Any
from dotenv import load_dotenv

load_dotenv()

# System Configuration
SYSTEM_CONFIG: Dict[str, Any] = {
    "name": "REX",
    "version": "1.0.0",
    "description": "Reasoning Engine eXtended - Advanced JARVIS-like AI",
    "author": "anthonyiceflame784-byte",
    "max_memory_mb": 2048,
    "max_agents": 10,
    "timeout_seconds": 300,
}

# Logging Configuration
LOG_LEVEL = os.getenv("REX_LOG_LEVEL", "INFO")
LOG_FILE = os.getenv("REX_LOG_FILE", "rex.log")
LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

# API Configuration
API_CONFIG = {
    "enable_rest_api": True,
    "api_port": int(os.getenv("REX_API_PORT", 5000)),
    "api_host": os.getenv("REX_API_HOST", "127.0.0.1"),
    "enable_cors": True,
}

# Voice Configuration
VOICE_CONFIG = {
    "enabled": True,
    "engine": "google",
    "language": "en-US",
    "voice_speed": 1.0,
}

# Memory Configuration
MEMORY_CONFIG = {
    "max_short_term_items": 1000,
    "max_long_term_items": 10000,
    "memory_retention_days": 365,
    "enable_encryption": False,
}

# Security Configuration
SECURITY_CONFIG = {
    "require_permissions": True,
    "permission_level": "strict",
    "enable_audit_log": True,
    "audit_retention_days": 30,
}

# Plugin Configuration
PLUGIN_CONFIG = {
    "plugin_directory": "plugins",
    "auto_load_plugins": True,
    "enable_plugin_sandboxing": True,
}

# Reasoning Configuration
REASONING_CONFIG = {
    "max_reasoning_steps": 10,
    "reasoning_timeout": 30,
    "enable_multi_path_reasoning": True,
    "confidence_threshold": 0.7,
}

# Self-Expansion Configuration
SELF_EXPANSION_CONFIG = {
    "enabled": True,
    "max_code_generation_attempts": 5,
    "auto_learn_enabled": True,
    "code_review_required": True,
}

# Agent Configuration
AGENT_CONFIG = {
    "default_timeout": 60,
    "max_parallel_agents": 5,
    "enable_agent_communication": True,
}

# OpenAI Configuration
OPENAI_CONFIG = {
    "api_key": os.getenv("OPENAI_API_KEY"),
    "model": "gpt-4",
    "temperature": 0.7,
    "max_tokens": 2000,
}

"""
Self-Expansion System for REX AI - Autonomous code generation and self-modification.
"""

import logging
import os
import re
from typing import Dict, Optional, List, Tuple
from datetime import datetime

try:
    import openai
    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False

from security.permission_system import request_permission

logger = logging.getLogger(__name__)


class CodeValidator:
    """Validates generated code for safety."""
    
    FORBIDDEN_PATTERNS = [
        r'__import__',
        r'exec\(',
        r'eval\(',
        r'os\.system',
        r'subprocess',
        r'socket\.',
        r'open\(',
    ]
    
    @staticmethod
    def is_safe(code: str) -> Tuple[bool, str]:
        """
        Check if code is safe to execute.
        
        Args:
            code: Python code to validate
            
        Returns:
            Tuple of (is_safe, reason)
        """
        for pattern in CodeValidator.FORBIDDEN_PATTERNS:
            if re.search(pattern, code):
                return False, f"Forbidden pattern detected: {pattern}"
        
        # Basic syntax check
        try:
            compile(code, '<string>', 'exec')
        except SyntaxError as e:
            return False, f"Syntax error: {e}"
        
        return True, "Code is safe"


class SelfExpansionSystem:
    """Handles autonomous code generation and system expansion."""
    
    def __init__(self):
        """Initialize self-expansion system."""
        self.api_key = os.getenv("OPENAI_API_KEY")
        self.model = "gpt-4"
        self.generation_history: List[Dict] = []
        self.code_validator = CodeValidator()
        
        if OPENAI_AVAILABLE and self.api_key:
            openai.api_key = self.api_key
            logger.info("Self-expansion system initialized with OpenAI")
        else:
            logger.warning("OpenAI not available - self-expansion limited")
    
    def generate_module(self, module_name: str, description: str) -> Dict:
        """
        Generate a new module based on description.
        
        Args:
            module_name: Name of the module to generate
            description: Description of what the module should do
            
        Returns:
            Dictionary with generation results
        """
        # Request permission
        if not request_permission(
            "self_expansion",
            f"Generate new module: {module_name}",
            "high"
        ):
            return {
                "success": False,
                "error": "Permission denied",
                "module_name": module_name
            }
        
        try:
            if not OPENAI_AVAILABLE:
                return self._generate_module_template(module_name, description)
            
            # Generate using OpenAI
            prompt = f"""
Generate a production-ready Python module for the REX AI system.

Module Name: {module_name}
Purpose: {description}

Requirements:
1. Professional, well-documented code
2. Comprehensive error handling
3. Logging integration
4. Type hints throughout
5. Docstrings for all functions
6. Security-conscious implementation

Provide ONLY the Python code, nothing else.
"""
            
            response = openai.ChatCompletion.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are an expert Python developer for AI systems."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=2000
            )
            
            generated_code = response.choices[0].message.content.strip()
            
            # Validate code
            is_safe, reason = self.code_validator.is_safe(generated_code)
            
            result = {
                "success": is_safe,
                "module_name": module_name,
                "code": generated_code,
                "validation": reason,
                "timestamp": datetime.now().isoformat()
            }
            
            if is_safe:
                self.generation_history.append(result)
                logger.info(f"Generated module: {module_name}")
            else:
                logger.warning(f"Generated code failed validation: {reason}")
            
            return result
        
        except Exception as e:
            logger.error(f"Failed to generate module: {e}")
            return {
                "success": False,
                "error": str(e),
                "module_name": module_name
            }
    
    def _generate_module_template(self, module_name: str, description: str) -> Dict:
        """Generate a template module when OpenAI is not available."""
        
        template = f'''"""
{description}

Auto-generated module for REX AI System.
"""

import logging
from typing import Dict, List, Optional, Any

logger = logging.getLogger(__name__)


class {module_name.capitalize()}:
    """
    {description}
    
    This is a template module. Implement specific functionality.
    """
    
    def __init__(self):
        """Initialize the {module_name} module."""
        logger.info("{module_name} initialized")
    
    def execute(self, **kwargs) -> Dict[str, Any]:
        """
        Execute the module.
        
        Args:
            **kwargs: Additional parameters
            
        Returns:
            Dictionary with results
        """
        logger.debug(f"Executing {module_name}")
        return {{"success": True, "message": "{module_name} executed"}}
'''
        
        return {
            "success": True,
            "module_name": module_name,
            "code": template,
            "validation": "Template generated",
            "timestamp": datetime.now().isoformat()
        }
    
    def improve_module(self, module_path: str, improvement_request: str) -> Dict:
        """
        Improve an existing module.
        
        Args:
            module_path: Path to the module file
            improvement_request: Description of desired improvements
            
        Returns:
            Dictionary with improvement results
        """
        if not request_permission(
            "self_expansion",
            f"Improve module: {module_path}",
            "high"
        ):
            return {"success": False, "error": "Permission denied"}
        
        try:
            # Read existing module
            if not os.path.exists(module_path):
                return {"success": False, "error": "Module not found"}
            
            with open(module_path, 'r') as f:
                existing_code = f.read()
            
            if not OPENAI_AVAILABLE:
                logger.info(f"Would improve {module_path}: {improvement_request}")
                return {
                    "success": True,
                    "message": "Improvement suggestion logged",
                    "module_path": module_path
                }
            
            # Generate improvement using OpenAI
            prompt = f"""
Improve the following Python module for the REX AI system.

Current Code:
{existing_code}

Improvement Request:
{improvement_request}

Provide ONLY the improved Python code, nothing else.
Maintain all existing functionality and add the requested improvements.
"""
            
            response = openai.ChatCompletion.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are an expert Python developer for AI systems."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=2000
            )
            
            improved_code = response.choices[0].message.content.strip()
            
            # Validate improved code
            is_safe, reason = self.code_validator.is_safe(improved_code)
            
            result = {
                "success": is_safe,
                "module_path": module_path,
                "improved_code": improved_code,
                "validation": reason,
                "timestamp": datetime.now().isoformat()
            }
            
            if is_safe:
                logger.info(f"Successfully improved module: {module_path}")
            
            return result
        
        except Exception as e:
            logger.error(f"Failed to improve module: {e}")
            return {
                "success": False,
                "error": str(e),
                "module_path": module_path
            }
    
    def get_generation_history(self) -> List[Dict]:
        """Get the history of generated modules."""
        return self.generation_history

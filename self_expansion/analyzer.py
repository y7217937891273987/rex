"""Code analyzer for self-expansion."""
import logging
import ast
import inspect
from typing import Any, Dict, List, Optional
from core.llm_manager import LLMManager
from security.permission_system import request_permission

logger = logging.getLogger(__name__)


class CodeAnalyzer:
    """Analyzes code for potential improvements and bugs."""
    
    def __init__(self, llm_manager: Optional[LLMManager] = None):
        """Initialize code analyzer.
        
        Args:
            llm_manager: LLM manager instance
        """
        self.llm_manager = llm_manager
        logger.info("Code Analyzer initialized")
    
    async def analyze_code(self, code: str) -> Dict[str, Any]:
        """Analyze code for issues and improvements.
        
        Args:
            code: Code to analyze
            
        Returns:
            Analysis results
        """
        if not request_permission("code_execution", f"Analyzing code: {code[:50]}..."):
            return {"error": "Permission denied"}
        
        analysis = {
            "syntax_valid": False,
            "errors": [],
            "warnings": [],
            "suggestions": []
        }
        
        # Check syntax
        try:
            ast.parse(code)
            analysis["syntax_valid"] = True
        except SyntaxError as e:
            analysis["errors"].append(f"Syntax error: {str(e)}")
            return analysis
        
        # Basic checks
        analysis["warnings"].extend(self._check_style(code))
        analysis["warnings"].extend(self._check_security(code))
        
        # Use LLM for detailed analysis if available
        if self.llm_manager:
            llm_analysis = await self.llm_manager.analyze_code(code)
            analysis["llm_analysis"] = llm_analysis
        
        return analysis
    
    def _check_style(self, code: str) -> List[str]:
        """Check code style issues.
        
        Args:
            code: Code to check
            
        Returns:
            List of style warnings
        """
        warnings = []
        lines = code.split('\n')
        
        for i, line in enumerate(lines, 1):
            # Check line length
            if len(line) > 100:
                warnings.append(f"Line {i}: exceeds 100 characters ({len(line)}). Consider breaking it up.")
            
            # Check for TODO/FIXME
            if 'TODO' in line or 'FIXME' in line:
                warnings.append(f"Line {i}: contains TODO/FIXME comment")
        
        return warnings
    
    def _check_security(self, code: str) -> List[str]:
        """Check security issues.
        
        Args:
            code: Code to check
            
        Returns:
            List of security warnings
        """
        warnings = []
        dangerous_functions = ['eval', 'exec', 'compile', '__import__']
        
        for func in dangerous_functions:
            if func in code:
                warnings.append(f"Potential security issue: '{func}' function used")
        
        return warnings

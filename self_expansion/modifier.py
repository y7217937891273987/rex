"""Code modifier for self-expansion and self-modification."""
import logging
from typing import Any, Dict, Optional, List
from pathlib import Path
from security.permission_system import request_permission
from core.llm_manager import LLMManager
from self_expansion.analyzer import CodeAnalyzer

logger = logging.getLogger(__name__)


class CodeModifier:
    """Modifies and generates code for self-expansion."""
    
    def __init__(self, llm_manager: Optional[LLMManager] = None):
        """Initialize code modifier.
        
        Args:
            llm_manager: LLM manager instance
        """
        self.llm_manager = llm_manager
        self.analyzer = CodeAnalyzer(llm_manager)
        self.modification_history: List[Dict[str, Any]] = []
        logger.info("Code Modifier initialized")
    
    async def suggest_improvements(self, code: str) -> Dict[str, Any]:
        """Suggest code improvements.
        
        Args:
            code: Code to improve
            
        Returns:
            Suggestions
        """
        if not self.llm_manager:
            return {"error": "LLM manager not available"}
        
        analysis = await self.analyzer.analyze_code(code)
        
        if not analysis.get("syntax_valid"):
            return {"error": "Code has syntax errors", "analysis": analysis}
        
        prompt = f"""Suggest improvements for this Python code:

```python
{code}
```

Focus on:
1. Performance
2. Readability
3. Maintainability
4. Security
5. Best practices

Provide specific, actionable suggestions."""
        
        suggestions = await self.llm_manager.get_completion(
            messages=[{"role": "user", "content": prompt}]
        )
        
        return {
            "original_code": code[:100],
            "analysis": analysis,
            "suggestions": suggestions
        }
    
    async def generate_feature(self, description: str) -> Dict[str, Any]:
        """Generate code for a new feature.
        
        Args:
            description: Feature description
            
        Returns:
            Generated code
        """
        if not self.llm_manager:
            return {"error": "LLM manager not available"}
        
        if not request_permission("self_expansion", f"Generating feature: {description[:50]}..."):
            return {"error": "Permission denied"}
        
        code = await self.llm_manager.generate_code(
            description=description,
            language="python",
            context="For a modular AI system"
        )
        
        # Analyze generated code
        analysis = await self.analyzer.analyze_code(code)
        
        return {
            "description": description,
            "code": code,
            "analysis": analysis
        }
    
    async def apply_modification(self, file_path: str, modifications: str) -> Dict[str, Any]:
        """Apply modifications to a file.
        
        Args:
            file_path: Path to file to modify
            modifications: Modifications to apply
            
        Returns:
            Modification result
        """
        if not request_permission("file_system_access", f"Modifying {file_path}"):
            return {"error": "Permission denied"}
        
        try:
            path = Path(file_path)
            if not path.exists():
                return {"error": f"File not found: {file_path}"}
            
            # Read original content
            with open(path, 'r') as f:
                original_content = f.read()
            
            # Apply modifications
            modified_content = self._apply_modifications(original_content, modifications)
            
            # Analyze new code
            analysis = await self.analyzer.analyze_code(modified_content)
            
            if not analysis.get("syntax_valid"):
                return {
                    "error": "Modified code has syntax errors",
                    "original": original_content,
                    "attempted": modified_content,
                    "analysis": analysis
                }
            
            # Write modified content
            with open(path, 'w') as f:
                f.write(modified_content)
            
            # Log modification
            self.modification_history.append({
                "file": file_path,
                "original": original_content[:200],
                "modified": modified_content[:200]
            })
            
            logger.info(f"File modified: {file_path}")
            return {
                "success": True,
                "file": file_path,
                "message": "File successfully modified"
            }
        except Exception as e:
            logger.error(f"Modification failed: {e}")
            return {"error": str(e)}
    
    def _apply_modifications(self, original: str, modifications: str) -> str:
        """Apply modifications to code.
        
        Args:
            original: Original code
            modifications: Modifications description
            
        Returns:
            Modified code
        """
        # This is a placeholder - in production, this would use more sophisticated patching
        return original + f"\n# Applied modification: {modifications}"
    
    def get_modification_history(self) -> List[Dict[str, Any]]:
        """Get modification history.
        
        Returns:
            History list
        """
        return self.modification_history.copy()

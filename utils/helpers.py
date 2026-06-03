"""Helper utility functions."""
from typing import Any, Dict, Optional


def validate_input(text: str, min_length: int = 1, max_length: int = 10000) -> tuple[bool, Optional[str]]:
    """Validate user input.
    
    Args:
        text: Input text
        min_length: Minimum length
        max_length: Maximum length
        
    Returns:
        Tuple of (is_valid, error_message)
    """
    if not text or not text.strip():
        return False, "Input cannot be empty"
    
    if len(text) < min_length:
        return False, f"Input too short (minimum {min_length} characters)"
    
    if len(text) > max_length:
        return False, f"Input too long (maximum {max_length} characters)"
    
    return True, None


def format_response(response: Any, include_metadata: bool = True) -> Dict[str, Any]:
    """Format response for API.
    
    Args:
        response: Response data
        include_metadata: Whether to include metadata
        
    Returns:
        Formatted response
    """
    formatted = {
        "data": response,
        "success": True
    }
    
    if include_metadata:
        import datetime
        formatted["timestamp"] = datetime.datetime.now().isoformat()
    
    return formatted

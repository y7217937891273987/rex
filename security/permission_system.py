"""Permission system for controlling AI self-modification and sensitive operations."""
import json
from typing import Dict, List, Optional, Callable, Any
from datetime import datetime
from enum import Enum
import logging

logger = logging.getLogger(__name__)


class PermissionLevel(Enum):
    """Permission levels for the system."""
    DENIED = 0
    USER_REVIEW = 1
    AUTO_APPROVE = 2
    ADMIN_ONLY = 3


class PermissionSystem:
    """Manages permissions for sensitive AI operations."""
    
    def __init__(self, admin_user: str = "admin", require_permission: bool = True):
        """Initialize permission system.
        
        Args:
            admin_user: Administrator username
            require_permission: Whether to require permissions
        """
        self.admin_user = admin_user
        self.require_permission = require_permission
        self.permissions: Dict[str, PermissionLevel] = {
            "modify_core_logic": PermissionLevel.ADMIN_ONLY,
            "modify_memory": PermissionLevel.USER_REVIEW,
            "modify_plugins": PermissionLevel.USER_REVIEW,
            "modify_agents": PermissionLevel.USER_REVIEW,
            "self_expansion": PermissionLevel.ADMIN_ONLY,
            "code_execution": PermissionLevel.USER_REVIEW,
            "file_system_access": PermissionLevel.ADMIN_ONLY,
            "network_operations": PermissionLevel.USER_REVIEW,
        }
        self.permission_callbacks: Dict[str, List[Callable]] = {}
        self.audit_log: List[Dict[str, Any]] = []
    
    def request_permission(self, action: str, details: Optional[str] = None) -> bool:
        """Request permission for an action.
        
        Args:
            action: Action requiring permission
            details: Additional details about the action
            
        Returns:
            Whether permission was granted
        """
        if not self.require_permission:
            return True
        
        perm_level = self.permissions.get(action, PermissionLevel.USER_REVIEW)
        
        # Log the request
        self._log_permission_request(action, details, perm_level)
        
        # Execute callbacks
        if action in self.permission_callbacks:
            for callback in self.permission_callbacks[action]:
                if not callback(action, details):
                    self._log_permission_result(action, False)
                    return False
        
        # Check permission level
        if perm_level == PermissionLevel.DENIED:
            logger.warning(f"Permission denied for action: {action}")
            self._log_permission_result(action, False)
            return False
        
        if perm_level == PermissionLevel.ADMIN_ONLY:
            logger.warning(f"Admin-only action requested: {action}")
            self._log_permission_result(action, False)
            return False
        
        if perm_level == PermissionLevel.USER_REVIEW:
            # In production, this would trigger user notification
            logger.info(f"User review required for action: {action}")
        
        self._log_permission_result(action, True)
        return True
    
    def set_permission_level(self, action: str, level: PermissionLevel) -> None:
        """Set permission level for an action.
        
        Args:
            action: Action name
            level: Permission level
        """
        self.permissions[action] = level
        logger.info(f"Permission level set for {action}: {level.name}")
    
    def register_callback(self, action: str, callback: Callable[[str, Optional[str]], bool]) -> None:
        """Register a callback for permission decisions.
        
        Args:
            action: Action name
            callback: Callback function that returns True if permission granted
        """
        if action not in self.permission_callbacks:
            self.permission_callbacks[action] = []
        self.permission_callbacks[action].append(callback)
    
    def _log_permission_request(self, action: str, details: Optional[str], level: PermissionLevel) -> None:
        """Log permission request."""
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "action": action,
            "details": details,
            "level": level.name,
            "type": "request"
        }
        self.audit_log.append(log_entry)
    
    def _log_permission_result(self, action: str, granted: bool) -> None:
        """Log permission result."""
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "action": action,
            "granted": granted,
            "type": "result"
        }
        self.audit_log.append(log_entry)
    
    def get_audit_log(self) -> List[Dict[str, Any]]:
        """Get the audit log."""
        return self.audit_log.copy()


# Global permission system instance
_permission_system: Optional[PermissionSystem] = None


def init_permission_system(admin_user: str = "admin", require_permission: bool = True) -> PermissionSystem:
    """Initialize the global permission system."""
    global _permission_system
    _permission_system = PermissionSystem(admin_user, require_permission)
    return _permission_system


def get_permission_system() -> PermissionSystem:
    """Get the global permission system instance."""
    global _permission_system
    if _permission_system is None:
        _permission_system = PermissionSystem()
    return _permission_system


def request_permission(action: str, details: Optional[str] = None) -> bool:
    """Request permission for an action (convenience function).
    
    Args:
        action: Action requiring permission
        details: Additional details about the action
        
    Returns:
        Whether permission was granted
    """
    return get_permission_system().request_permission(action, details)

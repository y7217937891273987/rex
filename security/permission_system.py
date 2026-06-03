"""
Permission System for REX AI - Security layer for sensitive operations.
"""

import logging
from typing import Dict, List, Optional, Callable
from datetime import datetime
import json
from enum import Enum
import os

logger = logging.getLogger(__name__)


class PermissionLevel(Enum):
    """Permission levels in the system."""
    DENY = 0
    USER_APPROVAL = 1
    RESTRICTED = 2
    ALLOWED = 3


class PermissionRequest:
    """Represents a permission request."""
    
    def __init__(self, action: str, description: str, risk_level: str = "medium"):
        self.action = action
        self.description = description
        self.risk_level = risk_level
        self.timestamp = datetime.now()
        self.approved = False
        self.approver = None
    
    def to_dict(self) -> Dict:
        """Convert to dictionary."""
        return {
            "action": self.action,
            "description": self.description,
            "risk_level": self.risk_level,
            "timestamp": self.timestamp.isoformat(),
            "approved": self.approved,
            "approver": self.approver
        }


class PermissionManager:
    """Manages permissions and security policies."""
    
    def __init__(self):
        """Initialize permission manager."""
        self.permissions: Dict[str, PermissionLevel] = {
            "core_modification": PermissionLevel.DENY,
            "memory_write": PermissionLevel.RESTRICTED,
            "plugin_install": PermissionLevel.USER_APPROVAL,
            "agent_spawn": PermissionLevel.RESTRICTED,
            "system_shutdown": PermissionLevel.USER_APPROVAL,
            "code_generation": PermissionLevel.RESTRICTED,
            "self_modify": PermissionLevel.DENY,
            "external_api_call": PermissionLevel.ALLOWED,
            "file_system_access": PermissionLevel.RESTRICTED,
            "network_access": PermissionLevel.ALLOWED,
            "model_inference": PermissionLevel.ALLOWED,
            "self_expansion": PermissionLevel.USER_APPROVAL,
        }
        
        self.permission_history: List[PermissionRequest] = []
        self.approval_callbacks: Dict[str, Callable] = {}
        self.audit_log_enabled = True
        
        logger.info("PermissionManager initialized")
    
    def request_permission(self, action: str, description: str = "", 
                          risk_level: str = "medium") -> bool:
        """
        Request permission for an action.
        
        Args:
            action: The action being requested
            description: Description of the action
            risk_level: Risk level (low, medium, high)
            
        Returns:
            True if permission granted, False otherwise
        """
        perm_level = self.permissions.get(action, PermissionLevel.DENY)
        perm_request = PermissionRequest(action, description, risk_level)
        
        # Log the request
        self._log_request(perm_request)
        
        if perm_level == PermissionLevel.DENY:
            logger.warning(f"Permission DENIED for action: {action}")
            perm_request.approved = False
            self.permission_history.append(perm_request)
            return False
        
        elif perm_level == PermissionLevel.ALLOWED:
            logger.info(f"Permission ALLOWED for action: {action}")
            perm_request.approved = True
            self.permission_history.append(perm_request)
            return True
        
        elif perm_level == PermissionLevel.RESTRICTED:
            logger.info(f"Permission RESTRICTED for action: {action} - requires review")
            perm_request.approved = True
            self.permission_history.append(perm_request)
            return True
        
        elif perm_level == PermissionLevel.USER_APPROVAL:
            logger.info(f"Permission requires USER APPROVAL for action: {action}")
            approved = self._get_user_approval(perm_request)
            perm_request.approved = approved
            self.permission_history.append(perm_request)
            return approved
        
        return False
    
    def grant_permission(self, action: str, level: PermissionLevel):
        """Grant permission for an action."""
        if action in self.permissions:
            self.permissions[action] = level
            logger.info(f"Permission granted: {action} -> {level.name}")
        else:
            logger.warning(f"Unknown action: {action}")
    
    def revoke_permission(self, action: str):
        """Revoke permission for an action."""
        if action in self.permissions:
            self.permissions[action] = PermissionLevel.DENY
            logger.info(f"Permission revoked for action: {action}")
    
    def register_approval_callback(self, action: str, callback: Callable):
        """Register a callback for permission approvals."""
        self.approval_callbacks[action] = callback
    
    def _get_user_approval(self, request: PermissionRequest) -> bool:
        """Get user approval for a permission request."""
        if request.action in self.approval_callbacks:
            return self.approval_callbacks[request.action](request)
        
        # For self-expansion and critical operations, prompt user
        if request.action in ["self_expand", "self_modify", "plugin_install", "system_shutdown"]:
            print(f"\n⚠️  PERMISSION REQUEST ⚠️")
            print(f"Action: {request.action}")
            print(f"Description: {request.description}")
            print(f"Risk Level: {request.risk_level}")
            response = input("\nApprove? (yes/no): ").strip().lower()
            approved = response in ["yes", "y", "approve"]
            if approved:
                request.approver = "user_input"
                logger.info(f"User approved: {request.action}")
            else:
                logger.warning(f"User denied: {request.action}")
            return approved
        
        logger.info(f"Auto-approving action: {request.action}")
        return True
    
    def _log_request(self, request: PermissionRequest):
        """Log a permission request to audit log."""
        if self.audit_log_enabled:
            os.makedirs("logs", exist_ok=True)
            with open("logs/audit.log", "a") as f:
                f.write(json.dumps(request.to_dict()) + "\n")
    
    def get_permission_history(self, action: Optional[str] = None) -> List[Dict]:
        """Get permission history."""
        history = self.permission_history
        
        if action:
            history = [p for p in history if p.action == action]
        
        return [p.to_dict() for p in history]
    
    def is_action_allowed(self, action: str) -> bool:
        """Quick check if action is allowed."""
        perm_level = self.permissions.get(action, PermissionLevel.DENY)
        return perm_level in [PermissionLevel.ALLOWED, PermissionLevel.RESTRICTED]


def request_permission(action: str, description: str = "", 
                      risk_level: str = "medium") -> bool:
    """
    Module-level function to request permission.
    
    Args:
        action: The action being requested
        description: Description of the action
        risk_level: Risk level (low, medium, high)
        
    Returns:
        True if permission granted, False otherwise
    """
    if not hasattr(request_permission, '_manager'):
        logger.warning("PermissionManager not initialized")
        return False
    
    return request_permission._manager.request_permission(action, description, risk_level)


def set_permission_manager(manager: PermissionManager):
    """Set the global permission manager."""
    request_permission._manager = manager

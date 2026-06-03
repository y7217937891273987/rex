"""Encryption and data protection utilities."""
from cryptography.fernet import Fernet
import base64
import hashlib
from typing import Union
import logging

logger = logging.getLogger(__name__)


class EncryptionManager:
    """Manages encryption and decryption of sensitive data."""
    
    def __init__(self, secret_key: str):
        """Initialize encryption manager.
        
        Args:
            secret_key: Secret key for encryption
        """
        # Derive a key from the secret
        key_hash = hashlib.sha256(secret_key.encode()).digest()
        self.cipher = Fernet(base64.urlsafe_b64encode(key_hash))
    
    def encrypt(self, data: Union[str, bytes]) -> str:
        """Encrypt data.
        
        Args:
            data: Data to encrypt
            
        Returns:
            Encrypted data as string
        """
        if isinstance(data, str):
            data = data.encode()
        try:
            encrypted = self.cipher.encrypt(data)
            return encrypted.decode()
        except Exception as e:
            logger.error(f"Encryption failed: {e}")
            raise
    
    def decrypt(self, encrypted_data: Union[str, bytes]) -> str:
        """Decrypt data.
        
        Args:
            encrypted_data: Encrypted data
            
        Returns:
            Decrypted data as string
        """
        if isinstance(encrypted_data, str):
            encrypted_data = encrypted_data.encode()
        try:
            decrypted = self.cipher.decrypt(encrypted_data)
            return decrypted.decode()
        except Exception as e:
            logger.error(f"Decryption failed: {e}")
            raise

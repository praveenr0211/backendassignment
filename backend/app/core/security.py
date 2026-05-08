"""
Security utilities for JWT token handling and password hashing.
"""
from datetime import datetime, timedelta, timezone
from typing import Optional, Dict, Any
from jose import JWTError, jwt
from passlib.context import CryptContext
import logging

from app.core.config import settings

logger = logging.getLogger(__name__)

# Password hashing context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class PasswordUtils:
    """Utility class for password operations."""
    
    @staticmethod
    def hash_password(password: str) -> str:
        """
        Hash a password using bcrypt.
        
        Args:
            password: Plain text password.
            
        Returns:
            Hashed password.
        """
        return pwd_context.hash(password)
    
    @staticmethod
    def verify_password(plain_password: str, hashed_password: str) -> bool:
        """
        Verify a plain password against a hashed password.
        
        Args:
            plain_password: Plain text password.
            hashed_password: Hashed password.
            
        Returns:
            True if password is correct, False otherwise.
        """
        return pwd_context.verify(plain_password, hashed_password)


class JWTUtils:
    """Utility class for JWT token operations."""
    
    @staticmethod
    def create_access_token(
        data: Dict[str, Any],
        expires_delta: Optional[timedelta] = None
    ) -> tuple[str, int]:
        """
        Create a JWT access token.
        
        Args:
            data: Data to encode in token.
            expires_delta: Token expiration time delta.
            
        Returns:
            Tuple of (token, expires_in_seconds).
        """
        to_encode = data.copy()
        
        if expires_delta:
            expire = datetime.now(timezone.utc) + expires_delta
        else:
            expire = datetime.now(timezone.utc) + timedelta(
                minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
            )
        
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(
            to_encode,
            settings.SECRET_KEY,
            algorithm=settings.ALGORITHM
        )
        
        expires_in = int(expires_delta.total_seconds()) if expires_delta else (
            settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60
        )
        
        return encoded_jwt, expires_in
    
    @staticmethod
    def create_refresh_token(data: Dict[str, Any]) -> str:
        """
        Create a JWT refresh token.
        
        Args:
            data: Data to encode in token.
            
        Returns:
            Refresh token string.
        """
        to_encode = data.copy()
        expire = datetime.now(timezone.utc) + timedelta(
            days=settings.REFRESH_TOKEN_EXPIRE_DAYS
        )
        to_encode.update({"exp": expire})
        
        encoded_jwt = jwt.encode(
            to_encode,
            settings.SECRET_KEY,
            algorithm=settings.ALGORITHM
        )
        
        return encoded_jwt
    
    @staticmethod
    def decode_token(token: str) -> Optional[Dict[str, Any]]:
        """
        Decode a JWT token.
        
        Args:
            token: JWT token string.
            
        Returns:
            Decoded token data or None if invalid.
        """
        try:
            payload = jwt.decode(
                token,
                settings.SECRET_KEY,
                algorithms=[settings.ALGORITHM]
            )
            return payload
        except JWTError as e:
            logger.error(f"JWT decode error: {str(e)}")
            return None
    
    @staticmethod
    def is_token_expired(token: str) -> bool:
        """
        Check if a JWT token is expired.
        
        Args:
            token: JWT token string.
            
        Returns:
            True if token is expired, False otherwise.
        """
        payload = JWTUtils.decode_token(token)
        if not payload:
            return True
        
        try:
            exp = payload.get("exp")
            if exp is None:
                return True
            
            exp_datetime = datetime.fromtimestamp(exp, tz=timezone.utc)
            return exp_datetime <= datetime.now(timezone.utc)
        except Exception as e:
            logger.error(f"Error checking token expiration: {str(e)}")
            return True

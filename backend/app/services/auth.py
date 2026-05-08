"""
Business logic for authentication operations.
"""
from sqlalchemy.orm import Session
from typing import Optional, Dict, Any
from datetime import timedelta
import logging

from app.models import User
from app.schemas import UserRegister, UserLogin, TokenResponse
from app.core.security import PasswordUtils, JWTUtils
from app.services.user import UserService

logger = logging.getLogger(__name__)


class AuthService:
    """Service class for authentication operations."""
    
    @staticmethod
    def register_user(db: Session, user_data: UserRegister) -> User:
        """
        Register a new user.
        
        Args:
            db: Database session.
            user_data: User registration data.
            
        Returns:
            Created user object.
            
        Raises:
            ValueError: If email already exists.
        """
        from app.schemas import UserCreate
        
        user_create = UserCreate(
            name=user_data.name,
            email=user_data.email,
            password=user_data.password
        )
        
        return UserService.create_user(db, user_create)
    
    @staticmethod
    def authenticate_user(
        db: Session,
        email: str,
        password: str
    ) -> Optional[User]:
        """
        Authenticate user with email and password.
        
        Args:
            db: Database session.
            email: User email.
            password: User password.
            
        Returns:
            User object if authentication successful, None otherwise.
        """
        user = UserService.get_user_by_email(db, email)
        if not user:
            return None
        
        if not PasswordUtils.verify_password(password, user.password_hash):
            return None
        
        if not user.is_active:
            return None
        
        return user
    
    @staticmethod
    def create_tokens(user: User) -> TokenResponse:
        """
        Create access and refresh tokens for user.
        
        Args:
            user: User object.
            
        Returns:
            Token response object.
        """
        # Prepare token data
        token_data = {
            "user_id": user.id,
            "email": user.email,
            "role": user.role.value
        }
        
        # Create access token
        access_token, expires_in = JWTUtils.create_access_token(token_data)
        
        # Create refresh token
        refresh_token = JWTUtils.create_refresh_token(token_data)
        
        return TokenResponse(
            access_token=access_token,
            refresh_token=refresh_token,
            token_type="bearer",
            expires_in=expires_in
        )
    
    @staticmethod
    def login_user(db: Session, login_data: UserLogin) -> TokenResponse:
        """
        Login user and return tokens.
        
        Args:
            db: Database session.
            login_data: User login data.
            
        Returns:
            Token response object.
            
        Raises:
            ValueError: If credentials are invalid.
        """
        # Authenticate user
        user = AuthService.authenticate_user(db, login_data.email, login_data.password)
        if not user:
            raise ValueError("Invalid email or password")
        
        logger.info(f"User logged in successfully: {user.email}")
        
        # Create tokens
        return AuthService.create_tokens(user)
    
    @staticmethod
    def refresh_access_token(refresh_token: str) -> Dict[str, Any]:
        """
        Create new access token from refresh token.
        
        Args:
            refresh_token: Refresh token string.
            
        Returns:
            New access token and expiration time.
            
        Raises:
            ValueError: If refresh token is invalid.
        """
        payload = JWTUtils.decode_token(refresh_token)
        if not payload:
            raise ValueError("Invalid refresh token")
        
        # Extract user data
        user_id = payload.get("user_id")
        email = payload.get("email")
        role = payload.get("role")
        
        if not all([user_id, email, role]):
            raise ValueError("Invalid refresh token data")
        
        # Create new access token
        token_data = {
            "user_id": user_id,
            "email": email,
            "role": role
        }
        
        access_token, expires_in = JWTUtils.create_access_token(token_data)
        
        return {
            "access_token": access_token,
            "token_type": "bearer",
            "expires_in": expires_in
        }

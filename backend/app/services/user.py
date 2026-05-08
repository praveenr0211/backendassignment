"""
Business logic for user operations.
"""
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from typing import Optional, List
import logging

from app.models import User, UserRole
from app.schemas import UserCreate, UserUpdate, UserResponse
from app.core.security import PasswordUtils

logger = logging.getLogger(__name__)


class UserService:
    """Service class for user operations."""
    
    @staticmethod
    def create_user(db: Session, user_data: UserCreate) -> User:
        """
        Create a new user.
        
        Args:
            db: Database session.
            user_data: User creation data.
            
        Returns:
            Created user object.
            
        Raises:
            ValueError: If email already exists.
        """
        try:
            # Check if email already exists
            existing_user = db.query(User).filter(User.email == user_data.email).first()
            if existing_user:
                raise ValueError(f"Email {user_data.email} is already registered")
            
            # Hash password
            password_hash = PasswordUtils.hash_password(user_data.password)
            
            # Create user
            db_user = User(
                name=user_data.name,
                email=user_data.email,
                password_hash=password_hash,
                role=user_data.role
            )
            
            db.add(db_user)
            db.commit()
            db.refresh(db_user)
            
            logger.info(f"User created successfully: {db_user.email}")
            return db_user
            
        except IntegrityError:
            db.rollback()
            raise ValueError(f"Email {user_data.email} is already registered")
        except Exception as e:
            db.rollback()
            logger.error(f"Error creating user: {str(e)}")
            raise
    
    @staticmethod
    def get_user_by_email(db: Session, email: str) -> Optional[User]:
        """
        Get user by email.
        
        Args:
            db: Database session.
            email: User email.
            
        Returns:
            User object or None if not found.
        """
        return db.query(User).filter(User.email == email).first()
    
    @staticmethod
    def get_user_by_id(db: Session, user_id: int) -> Optional[User]:
        """
        Get user by ID.
        
        Args:
            db: Database session.
            user_id: User ID.
            
        Returns:
            User object or None if not found.
        """
        return db.query(User).filter(User.id == user_id).first()
    
    @staticmethod
    def get_all_users(
        db: Session,
        skip: int = 0,
        limit: int = 10,
        search: Optional[str] = None
    ) -> tuple[List[User], int]:
        """
        Get all users with optional search and pagination.
        
        Args:
            db: Database session.
            skip: Number of records to skip.
            limit: Number of records to return.
            search: Search query for name or email.
            
        Returns:
            Tuple of (list of users, total count).
        """
        query = db.query(User)
        
        # Apply search filter
        if search:
            search_term = f"%{search}%"
            query = query.filter(
                (User.name.ilike(search_term)) | (User.email.ilike(search_term))
            )
        
        total = query.count()
        users = query.offset(skip).limit(limit).all()
        
        return users, total
    
    @staticmethod
    def update_user(
        db: Session,
        user: User,
        update_data: UserUpdate
    ) -> User:
        """
        Update user information.
        
        Args:
            db: Database session.
            user: User object to update.
            update_data: Update data.
            
        Returns:
            Updated user object.
        """
        try:
            if update_data.name:
                user.name = update_data.name
            
            if update_data.email:
                # Check if new email already exists
                existing = db.query(User).filter(
                    (User.email == update_data.email) & (User.id != user.id)
                ).first()
                if existing:
                    raise ValueError(f"Email {update_data.email} is already registered")
                user.email = update_data.email
            
            if update_data.password:
                user.password_hash = PasswordUtils.hash_password(update_data.password)
            
            db.commit()
            db.refresh(user)
            
            logger.info(f"User updated successfully: {user.email}")
            return user
            
        except IntegrityError:
            db.rollback()
            raise ValueError(f"Email is already registered")
        except Exception as e:
            db.rollback()
            logger.error(f"Error updating user: {str(e)}")
            raise
    
    @staticmethod
    def delete_user(db: Session, user: User) -> bool:
        """
        Delete a user.
        
        Args:
            db: Database session.
            user: User object to delete.
            
        Returns:
            True if deletion was successful.
        """
        try:
            db.delete(user)
            db.commit()
            logger.info(f"User deleted successfully: {user.email}")
            return True
        except Exception as e:
            db.rollback()
            logger.error(f"Error deleting user: {str(e)}")
            raise
    
    @staticmethod
    def deactivate_user(db: Session, user: User) -> User:
        """
        Deactivate a user.
        
        Args:
            db: Database session.
            user: User object to deactivate.
            
        Returns:
            Updated user object.
        """
        try:
            user.is_active = False
            db.commit()
            db.refresh(user)
            logger.info(f"User deactivated: {user.email}")
            return user
        except Exception as e:
            db.rollback()
            logger.error(f"Error deactivating user: {str(e)}")
            raise

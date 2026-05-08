"""
Pydantic schemas for request and response validation.
"""
from pydantic import BaseModel, EmailStr, Field, field_validator, ConfigDict
from datetime import datetime
from typing import Optional, List, Generic, TypeVar
from enum import Enum

from app.core.config import settings

T = TypeVar('T')


class UserRole(str, Enum):
    """User role enum."""
    USER = "user"
    ADMIN = "admin"


class TaskStatus(str, Enum):
    """Task status enum."""
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    CANCELLED = "cancelled"


# ==================== Auth Schemas ====================

class UserRegister(BaseModel):
    """Schema for user registration."""
    name: str = Field(..., min_length=1, max_length=255, description="User full name")
    email: EmailStr = Field(..., description="User email address")
    password: str = Field(..., min_length=settings.PASSWORD_MIN_LENGTH, description="User password")
    
    @field_validator("password")
    @classmethod
    def validate_password(cls, v: str) -> str:
        """Validate password strength."""
        if not any(char.isdigit() for char in v):
            raise ValueError("Password must contain at least one digit")
        if not any(char.isupper() for char in v):
            raise ValueError("Password must contain at least one uppercase letter")
        return v
    
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "name": "John Doe",
                "email": "john@example.com",
                "password": "SecurePass123"
            }
        }
    )


class UserLogin(BaseModel):
    """Schema for user login."""
    email: EmailStr = Field(..., description="User email address")
    password: str = Field(..., description="User password")
    
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "email": "john@example.com",
                "password": "SecurePass123"
            }
        }
    )


class TokenResponse(BaseModel):
    """Schema for token response."""
    access_token: str = Field(..., description="JWT access token")
    refresh_token: str = Field(..., description="JWT refresh token")
    token_type: str = Field(default="bearer", description="Token type")
    expires_in: int = Field(..., description="Token expiration time in seconds")


class TokenData(BaseModel):
    """Schema for token data."""
    user_id: int
    email: str
    role: str


# ==================== User Schemas ====================

class UserBase(BaseModel):
    """Base schema for user."""
    name: str = Field(..., min_length=1, max_length=255)
    email: EmailStr
    role: UserRole = Field(default=UserRole.USER)


class UserCreate(UserBase):
    """Schema for creating user."""
    password: str = Field(..., min_length=settings.PASSWORD_MIN_LENGTH)


class UserUpdate(BaseModel):
    """Schema for updating user."""
    name: Optional[str] = Field(None, min_length=1, max_length=255)
    email: Optional[EmailStr] = None
    password: Optional[str] = Field(None, min_length=settings.PASSWORD_MIN_LENGTH)


class UserResponse(UserBase):
    """Schema for user response."""
    id: int = Field(..., description="User ID")
    is_active: bool = Field(..., description="Is user active")
    created_at: datetime = Field(..., description="User creation timestamp")
    updated_at: datetime = Field(..., description="User update timestamp")
    
    model_config = ConfigDict(from_attributes=True)


# ==================== Task Schemas ====================

class TaskBase(BaseModel):
    """Base schema for task."""
    title: str = Field(..., min_length=1, max_length=255, description="Task title")
    description: Optional[str] = Field(None, max_length=5000, description="Task description")
    status: TaskStatus = Field(default=TaskStatus.PENDING, description="Task status")
    starred: bool = Field(default=False, description="Whether the task is starred")


class TaskCreate(TaskBase):
    """Schema for creating task."""
    pass


class TaskUpdate(BaseModel):
    """Schema for updating task."""
    title: Optional[str] = Field(None, min_length=1, max_length=255)
    description: Optional[str] = Field(None, max_length=5000)
    status: Optional[TaskStatus] = None
    starred: Optional[bool] = None


class TaskResponse(TaskBase):
    """Schema for task response."""
    id: int = Field(..., description="Task ID")
    user_id: int = Field(..., description="User ID")
    created_at: datetime = Field(..., description="Task creation timestamp")
    updated_at: datetime = Field(..., description="Task update timestamp")
    
    model_config = ConfigDict(from_attributes=True)


class TaskWithUser(TaskResponse):
    """Schema for task response with user information."""
    user: UserResponse


# ==================== Pagination Schemas ====================

class PaginationParams(BaseModel):
    """Schema for pagination parameters."""
    skip: int = Field(default=settings.DEFAULT_SKIP, ge=0, description="Number of records to skip")
    limit: int = Field(default=settings.DEFAULT_LIMIT, ge=1, le=settings.MAX_LIMIT, description="Number of records to return")


class PaginatedResponse(BaseModel, Generic[T]):
    """Schema for paginated response."""
    total: int = Field(..., description="Total number of records")
    skip: int = Field(..., description="Number of records skipped")
    limit: int = Field(..., description="Number of records returned")
    data: List[T] = Field(..., description="Data records")


class PaginatedTaskResponse(BaseModel):
    """Schema for paginated task response."""
    total: int = Field(..., description="Total number of records")
    skip: int = Field(..., description="Number of records skipped")
    limit: int = Field(..., description="Number of records returned")
    data: List['TaskResponse'] = Field(..., description="Task records")


class PaginatedUserResponse(BaseModel):
    """Schema for paginated user response."""
    total: int = Field(..., description="Total number of records")
    skip: int = Field(..., description="Number of records skipped")
    limit: int = Field(..., description="Number of records returned")
    data: List['UserResponse'] = Field(..., description="User records")


# ==================== Error Schemas ====================

class ErrorResponse(BaseModel):
    """Schema for error response."""
    status_code: int = Field(..., description="HTTP status code")
    message: str = Field(..., description="Error message")
    detail: Optional[dict] = Field(None, description="Additional error details")
    
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "status_code": 400,
                "message": "Validation error",
                "detail": {"field": "Invalid value"}
            }
        }
    )

"""
Task API routes.
"""
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import Optional, List
import logging

from app.database import get_db
from app.schemas import TaskCreate, TaskUpdate, TaskResponse, PaginatedTaskResponse
from app.services.task import TaskService
from app.models import User, UserRole
from app.dependencies.auth import get_current_user, get_current_admin_user

logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/api/v1/tasks",
    tags=["Tasks"]
)


@router.post(
    "",
    response_model=TaskResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new task",
    description="Create a new task for the current user"
)
async def create_task(
    task_data: TaskCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Create a new task.
    
    - **title**: Task title (required)
    - **description**: Task description (optional)
    - **status**: Task status (pending, in_progress, completed, cancelled)
    
    Returns:
        Created task object
    """
    try:
        task = TaskService.create_task(db, task_data, current_user)
        return task
    except Exception as e:
        logger.error(f"Error creating task: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error creating task"
        )


@router.get(
    "",
    response_model=PaginatedTaskResponse,
    status_code=status.HTTP_200_OK,
    summary="Get tasks",
    description="Get tasks based on user role"
)
async def get_tasks(
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(10, ge=1, le=100, description="Number of records to return"),
    status: Optional[str] = Query(None, description="Filter by task status"),
    search: Optional[str] = Query(None, description="Search in title and description"),
    starred: Optional[bool] = Query(None, description="Filter by starred status"),
    user_id: Optional[int] = Query(None, description="Filter by user ID (admin only)"),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get tasks.
    
    - Regular users: Get only their own tasks
    - Admin users: Get all tasks or filter by user
    
    Query Parameters:
        - **skip**: Number of records to skip (default: 0)
        - **limit**: Number of records to return (default: 10, max: 100)
        - **status**: Filter by status (pending, in_progress, completed, cancelled)
        - **search**: Search in task title and description
        - **starred**: Filter by starred status
        - **user_id**: Filter by user ID (admin only)
    
    Returns:
        Paginated list of tasks
    """
    try:
        # Admin can get all tasks or filter by user
        if current_user.role == UserRole.ADMIN:
            tasks, total = TaskService.get_all_tasks(
                db,
                skip=skip,
                limit=limit,
                status=status,
                search=search,
                starred=starred,
                user_id=user_id
            )
        else:
            # Regular users can only get their own tasks
            if user_id and user_id != current_user.id:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="You can only view your own tasks"
                )
            tasks, total = TaskService.get_user_tasks(
                db,
                current_user,
                skip=skip,
                limit=limit,
                status=status,
                search=search,
                starred=starred
            )
        
        return PaginatedTaskResponse(
            total=total,
            skip=skip,
            limit=limit,
            data=tasks
        )
    except Exception as e:
        logger.error(f"Error retrieving tasks: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error retrieving tasks"
        )


@router.get(
    "/{task_id}",
    response_model=TaskResponse,
    status_code=status.HTTP_200_OK,
    summary="Get task by ID",
    description="Get a specific task by its ID"
)
async def get_task(
    task_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get a specific task.
    
    - Regular users: Can only get their own tasks
    - Admin users: Can get any task
    
    Path Parameters:
        - **task_id**: ID of the task
    
    Returns:
        Task object
    """
    task = TaskService.get_task_by_id(db, task_id)
    
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )
    
    # Check authorization
    if current_user.role != UserRole.ADMIN and task.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You don't have permission to view this task"
        )
    
    return task


@router.put(
    "/{task_id}",
    response_model=TaskResponse,
    status_code=status.HTTP_200_OK,
    summary="Update task",
    description="Update a task"
)
async def update_task(
    task_id: int,
    task_data: TaskUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Update a task.
    
    - Regular users: Can only update their own tasks
    - Admin users: Can update any task
    
    Path Parameters:
        - **task_id**: ID of the task
    
    Request Body:
        - **title**: Task title (optional)
        - **description**: Task description (optional)
        - **status**: Task status (optional)
    
    Returns:
        Updated task object
    """
    task = TaskService.get_task_by_id(db, task_id)
    
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )
    
    # Check authorization
    if current_user.role != UserRole.ADMIN and task.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You don't have permission to update this task"
        )
    
    try:
        updated_task = TaskService.update_task(db, task, task_data)
        return updated_task
    except Exception as e:
        logger.error(f"Error updating task: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error updating task"
        )


@router.delete(
    "/{task_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete task",
    description="Delete a task"
)
async def delete_task(
    task_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Delete a task.
    
    - Regular users: Can only delete their own tasks
    - Admin users: Can delete any task
    
    Path Parameters:
        - **task_id**: ID of the task
    """
    task = TaskService.get_task_by_id(db, task_id)
    
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )
    
    # Check authorization
    if current_user.role != UserRole.ADMIN and task.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You don't have permission to delete this task"
        )
    
    try:
        TaskService.delete_task(db, task)
    except Exception as e:
        logger.error(f"Error deleting task: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error deleting task"
        )

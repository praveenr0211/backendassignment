"""
Business logic for task operations.
"""
from sqlalchemy.orm import Session
from sqlalchemy import and_
from typing import Optional, List, Tuple
import logging
from datetime import datetime

from app.models import Task, User, TaskStatus
from app.schemas import TaskCreate, TaskUpdate

logger = logging.getLogger(__name__)


class TaskService:
    """Service class for task operations."""
    
    @staticmethod
    def create_task(
        db: Session,
        task_data: TaskCreate,
        user: User
    ) -> Task:
        """
        Create a new task.
        
        Args:
            db: Database session.
            task_data: Task creation data.
            user: Owner of the task.
            
        Returns:
            Created task object.
        """
        try:
            db_task = Task(
                title=task_data.title,
                description=task_data.description,
                status=task_data.status,
                starred=task_data.starred,
                user_id=user.id
            )
            
            db.add(db_task)
            db.commit()
            db.refresh(db_task)
            
            logger.info(f"Task created successfully: {db_task.id} by user {user.email}")
            return db_task
            
        except Exception as e:
            db.rollback()
            logger.error(f"Error creating task: {str(e)}")
            raise
    
    @staticmethod
    def get_task_by_id(db: Session, task_id: int) -> Optional[Task]:
        """
        Get task by ID.
        
        Args:
            db: Database session.
            task_id: Task ID.
            
        Returns:
            Task object or None if not found.
        """
        return db.query(Task).filter(Task.id == task_id).first()
    
    @staticmethod
    def get_user_tasks(
        db: Session,
        user: User,
        skip: int = 0,
        limit: int = 10,
        status: Optional[str] = None,
        search: Optional[str] = None,
        starred: Optional[bool] = None
    ) -> Tuple[List[Task], int]:
        """
        Get all tasks for a user with optional filters.
        
        Args:
            db: Database session.
            user: User object.
            skip: Number of records to skip.
            limit: Number of records to return.
            status: Filter by task status.
            search: Search in title and description.
            starred: Filter by starred status.
            
        Returns:
            Tuple of (list of tasks, total count).
        """
        query = db.query(Task).filter(Task.user_id == user.id)
        
        # Apply status filter
        if status:
            query = query.filter(Task.status == TaskStatus[status.upper()])
        
        # Apply starred filter
        if starred is not None:
            query = query.filter(Task.starred == starred)
            
        # Apply search filter
        if search:
            search_term = f"%{search}%"
            query = query.filter(
                (Task.title.ilike(search_term)) | (Task.description.ilike(search_term))
            )
        
        total = query.count()
        tasks = query.offset(skip).limit(limit).all()
        
        return tasks, total
    
    @staticmethod
    def get_all_tasks(
        db: Session,
        skip: int = 0,
        limit: int = 10,
        status: Optional[str] = None,
        search: Optional[str] = None,
        user_id: Optional[int] = None,
        starred: Optional[bool] = None
    ) -> Tuple[List[Task], int]:
        """
        Get all tasks (admin only).
        
        Args:
            db: Database session.
            skip: Number of records to skip.
            limit: Number of records to return.
            status: Filter by task status.
            search: Search in title and description.
            user_id: Filter by user ID.
            starred: Filter by starred status.
            
        Returns:
            Tuple of (list of tasks, total count).
        """
        query = db.query(Task)
        
        # Apply status filter
        if status:
            query = query.filter(Task.status == TaskStatus[status.upper()])
        
        # Apply starred filter
        if starred is not None:
            query = query.filter(Task.starred == starred)
            
        # Apply user filter
        if user_id:
            query = query.filter(Task.user_id == user_id)
        
        # Apply search filter
        if search:
            search_term = f"%{search}%"
            query = query.filter(
                (Task.title.ilike(search_term)) | (Task.description.ilike(search_term))
            )
        
        total = query.count()
        tasks = query.offset(skip).limit(limit).all()
        
        return tasks, total
    
    @staticmethod
    def update_task(
        db: Session,
        task: Task,
        update_data: TaskUpdate
    ) -> Task:
        """
        Update task information.
        
        Args:
            db: Database session.
            task: Task object to update.
            update_data: Update data.
            
        Returns:
            Updated task object.
        """
        try:
            # Update task fields
            if update_data.title is not None:
                task.title = update_data.title
            if update_data.description is not None:
                task.description = update_data.description
            if update_data.status is not None:
                task.status = update_data.status
            if update_data.starred is not None:
                task.starred = update_data.starred
            
            task.updated_at = datetime.utcnow()
            
            db.commit()
            db.refresh(task)
            
            logger.info(f"Task updated successfully: {task.id}")
            return task
            
        except Exception as e:
            db.rollback()
            logger.error(f"Error updating task: {str(e)}")
            raise
    
    @staticmethod
    def delete_task(db: Session, task: Task) -> bool:
        """
        Delete a task.
        
        Args:
            db: Database session.
            task: Task object to delete.
            
        Returns:
            True if deletion was successful.
        """
        try:
            db.delete(task)
            db.commit()
            logger.info(f"Task deleted successfully: {task.id}")
            return True
        except Exception as e:
            db.rollback()
            logger.error(f"Error deleting task: {str(e)}")
            raise
    
    @staticmethod
    def is_task_owner(task: Task, user: User) -> bool:
        """
        Check if user is the owner of the task.
        
        Args:
            task: Task object.
            user: User object.
            
        Returns:
            True if user is owner, False otherwise.
        """
        return task.user_id == user.id

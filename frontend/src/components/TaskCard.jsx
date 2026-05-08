import React from 'react';
import '../styles/tasks.css';

const TaskCard = ({ task, onEdit, onDelete, onToggleStarred }) => {
  const formatDate = (dateString) => {
    return new Date(dateString).toLocaleDateString('en-US', {
      month: 'short',
      day: 'numeric',
      year: 'numeric',
    });
  };

  const getStatusClass = (status) => {
    return status.replace('_', '-');
  };

  return (
    <div className="task-card">
      <div className="task-header">
        <h3 className="task-title">{task.title}</h3>
        <div className="task-header-right">
          <span className={`task-status ${getStatusClass(task.status)}`}>
            {task.status.replace('_', ' ')}
          </span>
          <button
            className={`star-button ${task.starred ? 'starred' : ''}`}
            onClick={onToggleStarred}
          >
            {task.starred ? '★' : '☆'}
          </button>
        </div>
      </div>

      {task.description && (
        <p className="task-description">{task.description}</p>
      )}

      <div className="task-footer">
        <span className="task-date">{formatDate(task.created_at)}</span>
        <div className="task-actions">
          <button
            className="task-button btn-edit"
            onClick={() => onEdit(task)}
          >
            ✏️ Edit
          </button>
          <button
            className="task-button btn-delete"
            onClick={() => onDelete(task.id)}
          >
            🗑️ Delete
          </button>
        </div>
      </div>
    </div>
  );
};

export default TaskCard;

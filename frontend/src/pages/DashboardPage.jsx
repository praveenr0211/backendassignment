import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import { tasksAPI } from '../services/api';
import TaskCard from '../components/TaskCard';
import TaskModal from '../components/TaskModal';
import Alert from '../components/Alert';
import '../styles/dashboard.css';
import '../styles/tasks.css';

export const DashboardPage = () => {
  const { user, logout } = useAuth();
  const navigate = useNavigate();
  const [tasks, setTasks] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');
  const [showModal, setShowModal] = useState(false);
  const [editingTask, setEditingTask] = useState(null);
  const [filters, setFilters] = useState({
    skip: 0,
    limit: 10,
    status: '',
    search: '',
    starred: false,
  });
  const [sidebarOpen, setSidebarOpen] = useState(false);

  // Fetch tasks
  useEffect(() => {
    loadTasks();
  }, [filters]);

  const loadTasks = async () => {
    setLoading(true);
    try {
      const params = {
        skip: filters.skip,
        limit: filters.limit,
        starred: filters.starred,
      };
      if (filters.status) params.status = filters.status;
      if (filters.search) params.search = filters.search;

      const response = await tasksAPI.getTasks(params);
      setTasks(response.data.data);
      setError('');
    } catch (err) {
      setError('Failed to load tasks. Please try again.');
      console.error('Error loading tasks:', err);
    } finally {
      setLoading(false);
    }
  };

  const handleCreateTask = async (formData) => {
    try {
      await tasksAPI.createTask(formData);
      setSuccess('Task created successfully');
      setShowModal(false);
      loadTasks();
      setTimeout(() => setSuccess(''), 3000);
    } catch (err) {
      setError(err.response?.data?.detail || 'Failed to create task');
    }
  };

  const handleUpdateTask = async (taskId, formData) => {
    try {
      await tasksAPI.updateTask(taskId, formData);
      setSuccess('Task updated successfully');
      setEditingTask(null);
      setShowModal(false);
      loadTasks();
      setTimeout(() => setSuccess(''), 3000);
    } catch (err) {
      setError(err.response?.data?.detail || 'Failed to update task');
    }
  };

  const handleToggleStarred = async (task) => {
    try {
      await tasksAPI.updateTask(task.id, { starred: !task.starred });
      setSuccess(`Task ${task.starred ? 'unstarred' : 'starred'}`);
      loadTasks();
      setTimeout(() => setSuccess(''), 3000);
    } catch (err) {
      setError('Failed to update task');
    }
  };

  const handleDeleteTask = async (taskId) => {
    if (confirm('Are you sure you want to delete this task?')) {
      try {
        await tasksAPI.deleteTask(taskId);
        setSuccess('Task deleted successfully');
        loadTasks();
        setTimeout(() => setSuccess(''), 3000);
      } catch (err) {
        setError(err.response?.data?.detail || 'Failed to delete task');
      }
    }
  };

  const handleEditTask = (task) => {
    setEditingTask(task);
    setShowModal(true);
  };

  const handleLogout = () => {
    logout();
    navigate('/login');
  };

  const handleFilterChange = (e) => {
    const { name, value } = e.target;
    setFilters({
      ...filters,
      [name]: value,
      skip: 0,
    });
  };

  const handleSearch = (e) => {
    const value = e.target.value;
    setFilters({
      ...filters,
      search: value,
      skip: 0,
    });
  };

  const handleStarredFilter = () => {
    setFilters({
      ...filters,
      starred: !filters.starred,
      skip: 0,
    });
  };

  return (
    <div className="dashboard-container">
      {/* Sidebar */}
      <aside className={`sidebar ${sidebarOpen ? 'open' : ''}`}>
        <div className="sidebar-header">
          <h1 className="sidebar-title">TaskFlow</h1>
        </div>

        <nav className="sidebar-nav">
          <li>
            <div
              className={`sidebar-link ${!filters.starred ? 'active' : ''}`}
              onClick={() => setFilters({ ...filters, starred: false, skip: 0 })}
            >
              📋 My Tasks
            </div>
          </li>
          <li>
            <div
              className={`sidebar-link ${filters.starred ? 'active' : ''}`}
              onClick={handleStarredFilter}
            >
              ⭐ Starred
            </div>
          </li>
          {user?.role === 'admin' && (
            <>
              <li>
                <div className="sidebar-link">
                  👥 Users
                </div>
              </li>
              <li>
                <div className="sidebar-link">
                  ⚙️ Settings
                </div>
              </li>
            </>
          )}
        </nav>

        <div className="sidebar-footer">
          <div className="sidebar-user">
            <div className="user-avatar">
              {user?.name?.charAt(0).toUpperCase()}
            </div>
            <div className="user-info">
              <p className="user-name">{user?.name}</p>
              <p className="user-role">{user?.role}</p>
            </div>
          </div>
          <button className="sidebar-button" onClick={handleLogout}>
            Logout
          </button>
        </div>
      </aside>

      {/* Main Content */}
      <main className="main-content">
        <div className="header">
          <div>
            <h1 className="header-title">
              {filters.starred ? 'Starred Tasks' : 'My Tasks'}
            </h1>
            <p style={{ margin: 0, color: 'var(--text-secondary)' }}>
              Manage and track your tasks
            </p>
          </div>
          <div className="header-actions">
            <button
              className="button button-primary"
              onClick={() => {
                setEditingTask(null);
                setShowModal(true);
              }}
            >
              New Task
            </button>
          </div>
        </div>

        {/* Alerts */}
        {error && (
          <Alert
            type="error"
            message={error}
            onClose={() => setError('')}
          />
        )}
        {success && (
          <Alert
            type="success"
            message={success}
            onClose={() => setSuccess('')}
          />
        )}

        {/* Filters */}
        <div className="filters-container">
          <input
            type="text"
            placeholder="Search tasks..."
            className="filter-input"
            value={filters.search}
            onChange={handleSearch}
          />
          <select
            name="status"
            className="filter-select"
            value={filters.status}
            onChange={handleFilterChange}
          >
            <option value="">All Status</option>
            <option value="pending">Pending</option>
            <option value="in_progress">In Progress</option>
            <option value="completed">Completed</option>
            <option value="cancelled">Cancelled</option>
          </select>
        </div>

        {/* Tasks Grid */}
        {loading ? (
          <div className="spinner-container">
            <div className="spinner"></div>
          </div>
        ) : tasks.length === 0 ? (
          <div className="empty-state">
            <div className="empty-state-icon">📭</div>
            <p className="empty-state-text">
              No tasks found. Create one to get started!
            </p>
            <button
              className="button button-primary"
              onClick={() => {
                setEditingTask(null);
                setShowModal(true);
              }}
            >
              Create First Task
            </button>
          </div>
        ) : (
          <div className="tasks-container">
            {tasks.map((task) => (
              <TaskCard
                key={task.id}
                task={task}
                onEdit={() => {
                  setEditingTask(task);
                  setShowModal(true);
                }}
                onDelete={() => handleDeleteTask(task.id)}
                onToggleStarred={() => handleToggleStarred(task)}
              />
            ))}
          </div>
        )}
      </main>

      {/* Task Modal */}
      {showModal && (
        <TaskModal
          task={editingTask}
          onClose={() => {
            setShowModal(false);
            setEditingTask(null);
          }}
          onSubmit={editingTask ? handleUpdateTask : handleCreateTask}
        />
      )}
    </div>
  );
};

export default DashboardPage;

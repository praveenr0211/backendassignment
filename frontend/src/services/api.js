import axios from 'axios';

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

// Create axios instance
const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Request interceptor - Add token to headers
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('access_token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Response interceptor - Handle token refresh
api.interceptors.response.use(
  (response) => response,
  async (error) => {
    const originalRequest = error.config;

    // If token expired and we have refresh token, try to refresh
    if (error.response?.status === 401 && !originalRequest._retry) {
      originalRequest._retry = true;
      const refreshToken = localStorage.getItem('refresh_token');

      if (refreshToken) {
        try {
          const response = await axios.post(`${API_BASE_URL}/api/v1/auth/refresh`, {
            refresh_token: refreshToken,
          });

          const { access_token } = response.data;
          localStorage.setItem('access_token', access_token);

          // Retry original request
          api.defaults.headers.common['Authorization'] = `Bearer ${access_token}`;
          originalRequest.headers['Authorization'] = `Bearer ${access_token}`;
          return api(originalRequest);
        } catch (refreshError) {
          // Refresh failed, logout user
          localStorage.removeItem('access_token');
          localStorage.removeItem('refresh_token');
          window.location.href = '/login';
          return Promise.reject(refreshError);
        }
      }
    }

    return Promise.reject(error);
  }
);

// Authentication API
export const authAPI = {
  register: (data) => api.post('/api/v1/auth/register', data),
  login: (data) => api.post('/api/v1/auth/login', data),
  getCurrentUser: () => api.get('/api/v1/auth/me'),
  refreshToken: (refreshToken) =>
    api.post('/api/v1/auth/refresh', { refresh_token: refreshToken }),
};

// Tasks API
export const tasksAPI = {
  getTasks: (params) => api.get('/api/v1/tasks', { params }),
  getTask: (taskId) => api.get(`/api/v1/tasks/${taskId}`),
  createTask: (data) => api.post('/api/v1/tasks', data),
  updateTask: (taskId, data) => api.put(`/api/v1/tasks/${taskId}`, data),
  deleteTask: (taskId) => api.delete(`/api/v1/tasks/${taskId}`),
};

// Admin API
export const adminAPI = {
  getUsers: (params) => api.get('/api/v1/admin/users', { params }),
  getUser: (userId) => api.get(`/api/v1/admin/users/${userId}`),
  updateUser: (userId, data) => api.put(`/api/v1/admin/users/${userId}`, data),
  deleteUser: (userId) => api.delete(`/api/v1/admin/users/${userId}`),
  deactivateUser: (userId) => api.post(`/api/v1/admin/users/${userId}/deactivate`),
};

export default api;

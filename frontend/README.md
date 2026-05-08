# Task Management Frontend

A modern, responsive React application for task management with a dark theme UI.

## Features

- ✅ User authentication (login/register)
- ✅ JWT token handling with auto-refresh
- ✅ Task CRUD operations
- ✅ Task filtering and search
- ✅ Dark modern dashboard design
- ✅ Responsive layout
- ✅ Protected routes
- ✅ Axios interceptors for API calls

## Project Structure

```
frontend/
├── src/
│   ├── components/           # Reusable React components
│   │   ├── TaskCard.jsx
│   │   ├── TaskModal.jsx
│   │   ├── Alert.jsx
│   │   └── PrivateRoute.jsx
│   ├── pages/                # Page components
│   │   ├── LoginPage.jsx
│   │   ├── RegisterPage.jsx
│   │   └── DashboardPage.jsx
│   ├── services/             # API services
│   │   └── api.js           # Axios setup with interceptors
│   ├── context/              # React Context
│   │   └── AuthContext.jsx
│   ├── styles/               # CSS files
│   │   ├── global.css
│   │   ├── auth.css
│   │   ├── dashboard.css
│   │   ├── tasks.css
│   │   └── components.css
│   ├── App.jsx
│   └── main.jsx
├── public/                   # Static assets
├── index.html
├── package.json
├── vite.config.js
└── README.md
```

## Installation

### Prerequisites
- Node.js 16+ and npm

### Setup

```bash
# Navigate to frontend directory
cd frontend

# Install dependencies
npm install

# Create .env file
cp .env.example .env

# Edit .env with your API URL
# VITE_API_URL=http://localhost:8000
```

## Development

```bash
# Start development server
npm run dev

# The app will open at http://localhost:5173
```

## Build for Production

```bash
# Create optimized build
npm run build

# Preview production build
npm run preview
```

## Environment Variables

Create a `.env` file:

```
VITE_API_URL=http://localhost:8000
```

## Features Explained

### Authentication
- JWT tokens stored in localStorage
- Auto token refresh on expiration
- Protected routes for authenticated users
- Login/Register pages

### Task Management
- Create, read, update, delete tasks
- Filter by status (pending, in_progress, completed, cancelled)
- Search functionality
- Pagination support

### UI/UX
- Dark modern dashboard design
- Responsive grid layout for tasks
- Smooth animations and transitions
- Toast notifications for success/error messages
- Modal dialogs for task creation/editing

## Component Overview

### Pages
- **LoginPage**: User login with email and password
- **RegisterPage**: User registration with validation
- **DashboardPage**: Main dashboard with task management

### Components
- **TaskCard**: Displays individual task with actions
- **TaskModal**: Form for creating/editing tasks
- **Alert**: Toast notification component
- **PrivateRoute**: Route protection wrapper

### Services
- **api.js**: Centralized API client with:
  - Request interceptor for token addition
  - Response interceptor for token refresh
  - Auth, Tasks, and Admin API endpoints

### Context
- **AuthContext**: Global authentication state management

## Styling

All styling uses external CSS files (no Tailwind, no inline styles):

- `global.css` - Global styles and CSS variables
- `auth.css` - Authentication page styles
- `dashboard.css` - Dashboard layout styles
- `tasks.css` - Task-related component styles
- `components.css` - Reusable component styles

## API Integration

All API calls go through the `api.js` service:

```javascript
import { authAPI, tasksAPI } from '../services/api';

// Auth
await authAPI.login({ email, password });
await authAPI.register({ name, email, password });

// Tasks
await tasksAPI.getTasks(params);
await tasksAPI.createTask(data);
await tasksAPI.updateTask(id, data);
await tasksAPI.deleteTask(id);
```

## Error Handling

- API errors are caught and displayed via Alert components
- Authentication errors trigger automatic logout and redirect to login
- Form validation errors are shown inline

## Performance

- Lazy component loading via React Router
- Optimized CSS with minimal class names
- Efficient API calls with pagination
- Token refresh handled automatically

## Browser Support

- Chrome (latest)
- Firefox (latest)
- Safari (latest)
- Edge (latest)

## Production Deployment

```bash
# Build for production
npm run build

# Serve dist folder with a static server
npm install -g serve
serve -s dist

# Or use Docker
docker build -t task-frontend .
docker run -p 3000:3000 task-frontend
```

## Troubleshooting

**API connection issues:**
- Check if backend is running on http://localhost:8000
- Verify VITE_API_URL in .env file
- Check browser console for CORS errors

**Login/Token issues:**
- Clear localStorage: `localStorage.clear()`
- Verify backend SECRET_KEY matches
- Check token expiration time

**Styling issues:**
- Hard refresh: `Ctrl+Shift+R` (Windows/Linux) or `Cmd+Shift+R` (Mac)
- Check CSS file paths
- Verify global CSS is imported in main.jsx

## Development Tips

1. Use React DevTools for debugging
2. Check Network tab for API calls
3. Use Console for JavaScript errors
4. Use ColorPicker for CSS color values

## Next Steps

- Implement pagination UI
- Add task categories/tags
- Add task comments
- Add due dates
- Implement task notifications
- Add dark/light theme toggle
- Add analytics dashboard

---

**Version**: 1.0.0

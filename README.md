# Task Management Application - Full Stack

A production-ready full-stack task management application built with **FastAPI** (backend) and **React + Vite** (frontend).

## 🎯 Project Overview

This is a complete task management system featuring:
- ✅ Secure user authentication with JWT tokens
- ✅ Role-based access control (RBAC) — User & Admin roles
- ✅ Task CRUD operations with starred/favorites feature
- ✅ Task filtering, pagination, and search
- ✅ Modern, responsive React UI with Vite
- ✅ Production-ready architecture with Docker support
- ✅ Comprehensive API documentation (Swagger/ReDoc)

## 📁 Project Structure

```
backendassignment/
├── backend/                    # FastAPI backend (Python)
│   ├── app/
│   │   ├── main.py            # FastAPI app factory
│   │   ├── database.py        # SQLAlchemy database config
│   │   ├── models/            # SQLAlchemy ORM models
│   │   ├── schemas/           # Pydantic validation schemas
│   │   ├── routes/            # API endpoints
│   │   ├── services/          # Business logic layer
│   │   ├── core/              # Security, config
│   │   └── middleware/        # CORS, logging
│   ├── tests/
│   ├── requirements.txt
│   ├── .env.example
│   ├── Postman_Collection.json # API testing collection
│   ├── Dockerfile
│   ├── docker-compose.yml
│   └── README.md
│
└── frontend/                   # React + Vite frontend
    ├── src/
    │   ├── pages/             # Page components
    │   ├── components/        # Reusable UI components
    │   ├── services/          # API client services
    │   ├── context/           # React Context (auth)
    │   └── styles/            # CSS styles
    ├── public/
    ├── package.json
    ├── vite.config.js
    ├── .env.example
    └── README.md
```

## 🚀 Quick Start Guide

### Prerequisites
- **Python 3.11+** (for backend)
- **Node.js 16+** (for frontend)
- **npm** or **yarn**
- SQLite (included) or PostgreSQL (optional for production)

### Backend Setup

```bash
cd backend

# Create virtual environment
python -m venv venv

# Activate (Windows)
venv\Scripts\activate
# Or (Linux/Mac)
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Copy and configure .env
cp .env.example .env

# Run development server
python -m uvicorn app.main:app --reload
```

**Backend runs at:** `http://localhost:8000`  
**API Docs:** `http://localhost:8000/api/docs`

### Frontend Setup

```bash
cd frontend

# Install dependencies
npm install

# Copy and configure .env
cp .env.example .env

# Start development server
npm run dev
```

**Frontend runs at:** `http://localhost:5173` (or next available port)

### With Docker

```bash
cd backend
docker-compose up -d
```

This starts:
- Backend API: `http://localhost:8000`
- PostgreSQL: `localhost:5432`
- Redis: `localhost:6379` (optional)

## 🔧 Environment Configuration

### Backend Setup (.env)

Copy `backend/.env.example` to `backend/.env` and update values:

```env
# Database Configuration
# For development (SQLite):
DATABASE_URL=sqlite:///./test.db
# For production (PostgreSQL):
# DATABASE_URL=postgresql://user:password@localhost:5432/task_manager

# Security
SECRET_KEY=your-secret-key-change-in-production-min-32-chars-long
DEBUG=False

# JWT Configuration
ACCESS_TOKEN_EXPIRE_MINUTES=30
REFRESH_TOKEN_EXPIRE_DAYS=7

# API Configuration
API_V1_STR=/api/v1

# CORS Origins (comma-separated)
# CORS_ORIGINS=http://localhost:3000,http://localhost:5173

# Password Configuration
PASSWORD_MIN_LENGTH=8
```

### Frontend Setup (.env)

Copy `frontend/.env.example` to `frontend/.env`:

```env
# API Configuration
VITE_API_URL=http://localhost:8000
```

## 📚 API Documentation

### Authentication Endpoints

```
POST /api/v1/auth/register      - Register new user
POST /api/v1/auth/login         - Login user
POST /api/v1/auth/refresh       - Refresh access token
GET  /api/v1/auth/me            - Get current user info
```

### Task Endpoints

```
GET    /api/v1/tasks            - Get tasks (with pagination & filters)
POST   /api/v1/tasks            - Create new task
GET    /api/v1/tasks/{id}       - Get task by ID
PUT    /api/v1/tasks/{id}       - Update task
DELETE /api/v1/tasks/{id}       - Delete task
```

**Query Parameters for GET /api/v1/tasks:**
- `skip` (int): Pagination offset (default: 0)
- `limit` (int): Items per page (default: 10)
- `status` (str): Filter by status (pending, in_progress, completed, cancelled)
- `starred` (bool): Filter starred tasks only

### Admin Endpoints (requires admin role)

```
GET    /api/v1/admin/users              - Get all users
GET    /api/v1/admin/users/{id}         - Get user by ID
PUT    /api/v1/admin/users/{id}         - Update user
DELETE /api/v1/admin/users/{id}         - Delete user
POST   /api/v1/admin/users/{id}/deactivate - Deactivate user
```

## 📝 API Examples

### Register User
```bash
curl -X POST http://localhost:8000/api/v1/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "name": "John Doe",
    "email": "john@example.com",
    "password": "SecurePass123"
  }'
```

### Login
```bash
curl -X POST http://localhost:8000/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "john@example.com",
    "password": "SecurePass123"
  }'
```

### Create Task
```bash
curl -X POST http://localhost:8000/api/v1/tasks \
  -H "Authorization: Bearer {access_token}" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Complete project",
    "description": "Finish backend development",
    "status": "pending"
  }'
```

### Get Starred Tasks
```bash
curl -X GET "http://localhost:8000/api/v1/tasks?starred=true" \
  -H "Authorization: Bearer {access_token}"
```

## 🧪 Testing with Postman

1. **Import Collection:**
   - Open Postman → Import → select `backend/Postman_Collection.json`

2. **Set Environment Variables:**
   - Create environment: `base_url = http://localhost:8000`
   - Set `token` variable after login

3. **Run Requests:**
   - Register a user
   - Login and copy `access_token`
   - Use token in Authorization header for protected endpoints

## 💾 Database Schema

### Users Table
- `id` (Primary Key, Integer)
- `name` (String, required)
- `email` (String, unique, required)
- `password_hash` (String)
- `role` (String: "user" or "admin", default: "user")
- `is_active` (Boolean, default: True)
- `created_at` (DateTime, auto)
- `updated_at` (DateTime, auto)

### Tasks Table
- `id` (Primary Key, Integer)
- `title` (String, required)
- `description` (String, optional)
- `status` (String: "pending", "in_progress", "completed", "cancelled")
- `starred` (Boolean, default: False)
- `user_id` (Foreign Key → users.id)
- `created_at` (DateTime, auto)
- `updated_at` (DateTime, auto)

## 🔐 Security Features

- ✅ Password hashing with bcrypt
- ✅ JWT token authentication (access + refresh tokens)
- ✅ Role-based access control (RBAC)
- ✅ Input validation with Pydantic
- ✅ CORS protection
- ✅ SQL injection prevention (SQLAlchemy ORM)
- ✅ Secure token handling
- ✅ Email validation on registration

## 🧪 Testing

```bash
cd backend

# Run all tests
pytest

# Run with coverage report
pytest --cov=app tests/

# Run specific test file
pytest tests/test_auth.py
```

See [PRODUCTION_READY.md](PRODUCTION_READY.md) for a complete production configuration summary, and [QUICK_DEPLOY.md](QUICK_DEPLOY.md) for a 5-minute quick reference.

## 🌐 Deployment on Render

### Prerequisites
- Render account (free tier available at [render.com](https://render.com))
- GitHub repository (code must be on GitHub)
- PostgreSQL database (Render provides free tier)

### Step 1: Create PostgreSQL Database on Render

1. Go to [Render Dashboard](https://dashboard.render.com)
2. Click **New +** → **PostgreSQL**
3. Configure:
   - **Name**: `task_manager_db` (or your choice)
   - **Database**: `task_manager`
   - **User**: `postgres` (or custom)
   - **Region**: Select closest to you
   - **PostgreSQL Version**: Latest available
4. Click **Create Database**
5. Copy the **Internal Database URL** (starts with `postgresql://`) — save this for backend setup

### Step 2: Deploy Backend on Render

1. Push code to GitHub repository
2. In Render Dashboard, click **New +** → **Web Service**
3. Configure:
   - **Repository**: Select your GitHub repo
   - **Branch**: `main` (or your branch)
   - **Name**: `task-management-api`
   - **Region**: Same as database
   - **Runtime**: Python 3.11
   - **Build Command**: 
     ```bash
     pip install -r backend/requirements.txt
     ```
   - **Start Command**: 
     ```bash
     gunicorn -w 4 -k uvicorn.workers.UvicornWorker -b 0.0.0.0:8000 backend.app.main:app
     ```
4. Set **Environment Variables**:
   - `DATABASE_URL`: (paste your PostgreSQL URL from Step 1)
   - `SECRET_KEY`: Generate with: `python -c "import secrets; print(secrets.token_urlsafe(32))"`
   - `DEBUG`: `False`
   - `CORS_ORIGINS`: (will add frontend URL after deployment)
   - `ACCESS_TOKEN_EXPIRE_MINUTES`: `30`
   - `REFRESH_TOKEN_EXPIRE_DAYS`: `7`

5. Click **Create Web Service**
6. Wait for deployment (5-10 minutes)
7. Note your backend URL: `https://task-management-api.onrender.com` (example)

### Step 3: Deploy Frontend on Render

1. In Render Dashboard, click **New +** → **Static Site**
2. Configure:
   - **Repository**: Select your GitHub repo
   - **Branch**: `main`
   - **Name**: `task-management-ui`
   - **Root Directory**: `frontend`
   - **Build Command**: 
     ```bash
     npm install && npm run build
     ```
   - **Publish Directory**: `dist`

3. Click **Create Static Site**
4. Wait for deployment (3-5 minutes)
5. Note your frontend URL: `https://task-management-ui.onrender.com` (example)

### Step 4: Update Backend CORS

1. Go back to backend service on Render
2. Update **Environment Variables**:
   - `CORS_ORIGINS`: `https://task-management-ui.onrender.com,https://www.task-management-ui.onrender.com`
3. Click **Save** (automatic redeployment)

### Step 5: Update Frontend Environment

1. Create/update `frontend/.env.production`:
   ```env
   VITE_API_URL=https://task-management-api.onrender.com
   ```

2. Or set as build environment variable in Render:
   - Go to frontend static site settings
   - Add **Environment Variable**: `VITE_API_URL=https://task-management-api.onrender.com`
   - Redeploy

### Step 6: Test Deployment

1. Visit your frontend URL: `https://task-management-ui.onrender.com`
2. Test registration and login
3. Create a task and verify it's saved
4. Check backend logs in Render Dashboard

### Troubleshooting Deployment

**Backend not starting?**
```bash
# Check build/start commands are correct
# View deployment logs in Render Dashboard
# Verify DATABASE_URL is set correctly
# Ensure SECRET_KEY is at least 32 characters
```

**Database connection error?**
```bash
# Verify DATABASE_URL format: postgresql://user:password@host:port/database
# Ensure database exists and is ready
# Check firewall settings in Render
```

**Frontend not connecting to backend?**
```bash
# Verify VITE_API_URL points to correct backend URL
# Check CORS_ORIGINS includes frontend URL
# Clear browser cache and hard refresh (Ctrl+Shift+R)
```

**CORS errors in browser?**
```bash
# Add frontend URL to backend CORS_ORIGINS
# Redeploy backend after updating environment variables
```

### Alternative: Docker Deployment

**Backend:**
```bash
pip install gunicorn
gunicorn app.main:app --workers 4 --worker-class uvicorn.workers.UvicornWorker
```

**Frontend (Vite Build):**
```bash
npm run build
# Deploy contents of dist/ folder
```

**Docker Deployment:**
```bash
docker build -t task-management-api .
docker run -p 8000:8000 --env-file .env task-management-api
```

## 📊 Features Checklist

**Authentication & Security**
- ✅ User registration with validation
- ✅ Secure login with JWT
- ✅ Token refresh mechanism
- ✅ Role-based access control

**Task Management**
- ✅ CRUD operations
- ✅ Task status tracking
- ✅ Star/favorite tasks
- ✅ Task filtering (status, starred)
- ✅ Pagination support
- ✅ Search functionality

**API & Documentation**
- ✅ REST API with versioning
- ✅ Swagger/OpenAPI UI
- ✅ ReDoc documentation
- ✅ Postman collection

**Infrastructure**
- ✅ SQLite dev database
- ✅ PostgreSQL production ready
- ✅ Docker & docker-compose
- ✅ Environment configuration

**Frontend**
- ✅ React + Vite
- ✅ Responsive design
- ✅ Task card grid layout
- ✅ Modern UI theme
- ✅ Protected routes
- ✅ Toast notifications

## 🚦 HTTP Status Codes

- `200` - Success
- `201` - Created
- `204` - No Content
- `400` - Bad Request
- `401` - Unauthorized
- `403` - Forbidden
- `404` - Not Found
- `409` - Conflict
- `500` - Server Error

## 📱 Frontend Features

- Modern dashboard with task cards
- Real-time status updates
- Star/favorite task toggle
- Task filtering by status and starred status
- Create/edit task modals
- User authentication flow
- Toast notification system
- Responsive grid layout
- Dark/light theme support
- Protected routes with authentication

## 🔄 Scalability Considerations

For production deployment with high traffic, consider:

1. **Database:** Use PostgreSQL with read replicas for scaling read operations
2. **Caching:** Implement Redis for caching frequently accessed tasks
3. **Load Balancing:** Deploy multiple API instances behind a load balancer (Nginx, HAProxy)
4. **Message Queue:** Use Celery + RabbitMQ for async task processing
5. **Monitoring:** Implement logging, metrics, and alerting (Prometheus, Grafana)
6. **Container Orchestration:** Use Kubernetes for production deployments
7. **API Rate Limiting:** Implement request throttling to prevent abuse

See [SCALABILITY.md](SCALABILITY.md) for detailed scalability strategies.

## 📞 Support & Troubleshooting

### Backend not starting?
- Check Python version: `python --version` (requires 3.11+)
- Verify .env file exists and DATABASE_URL is correct
- Delete `test.db` and restart if using SQLite
- Check if port 8000 is available

### Frontend not connecting to backend?
- Verify backend is running: `http://localhost:8000/api/docs`
- Check VITE_API_URL in frontend/.env
- Clear browser cache and restart dev server
- Check browser console for CORS errors

### Database errors?
- For SQLite: Delete `test.db` and restart backend
- For PostgreSQL: Verify connection string and database exists
- Run migrations: `alembic upgrade head` (if using migrations)

## 📄 License

MIT License - Feel free to use this project for learning and development.

## 👨‍💻 Development Team

Created as a comprehensive full-stack internship assignment demonstrating:
- FastAPI backend development
- React frontend development
- Database design
- API design principles
- Security best practices
- Deployment strategies

- Logout functionality

## 🔄 Workflow

1. User registers or logs in
2. JWT token stored in localStorage
3. Token automatically added to API requests
4. Token auto-refreshed on expiration
5. Protected routes redirect to login if not authenticated
6. User can create, read, update, delete tasks
7. Admin can manage all users and tasks

## 📈 Scalability Notes

### Horizontal Scaling
- Stateless API design
- Load balancer compatible
- Database connection pooling

### Caching
- Redis support included
- Cache-Control headers
- Response caching ready

### Database
- PostgreSQL for production
- SQLAlchemy ORM optimization
- Index on frequently queried columns

### Monitoring
- Structured logging
- Request ID tracking
- Performance metrics

## 🎓 Learning Resources

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [React Documentation](https://react.dev/)
- [SQLAlchemy Documentation](https://docs.sqlalchemy.org/)
- [JWT Authentication](https://jwt.io/)
- [Vite Guide](https://vitejs.dev/)

## 🤝 Contributing

This is a complete project template. Feel free to:
- Add new features
- Improve styling
- Add more tests
- Enhance documentation

## 📄 License

MIT License - Free for educational and commercial use

---

**Version**: 1.0.0  
**Last Updated**: January 2024  
**Status**: Production Ready ✅

# Task Management REST API

A scalable, production-ready REST API for task management with authentication, role-based access control, and comprehensive documentation.

## 🚀 Features

### Authentication & Security
- ✅ User registration with email validation
- ✅ Secure login with JWT tokens
- ✅ Password hashing with bcrypt
- ✅ Token refresh mechanism
- ✅ Role-based access control (RBAC)

### Core Features
- ✅ CRUD operations for tasks
- ✅ User management (admin only)
- ✅ Task filtering and search
- ✅ Pagination support
- ✅ Error handling and validation
- ✅ API versioning (/api/v1)

### API Documentation
- ✅ Swagger/OpenAPI UI at `/api/docs`
- ✅ ReDoc documentation at `/api/redoc`
- ✅ Postman collection ready

### Scalability & DevOps
- ✅ Docker support with docker-compose
- ✅ PostgreSQL database with SQLAlchemy ORM
- ✅ Structured logging middleware
- ✅ CORS configuration
- ✅ Health check endpoint

## 📋 Project Structure

```
backend/
├── app/
│   ├── __init__.py
│   ├── main.py                 # FastAPI app factory
│   ├── database.py             # Database configuration
│   ├── core/
│   │   ├── config.py          # Settings and configuration
│   │   ├── security.py        # JWT and password utilities
│   │   └── __init__.py
│   ├── models/
│   │   └── __init__.py        # SQLAlchemy models (User, Task)
│   ├── schemas/
│   │   └── __init__.py        # Pydantic schemas for validation
│   ├── routes/
│   │   ├── auth.py            # Authentication endpoints
│   │   ├── tasks.py           # Task CRUD endpoints
│   │   ├── admin.py           # Admin endpoints
│   │   └── __init__.py
│   ├── services/
│   │   ├── auth.py            # Authentication business logic
│   │   ├── user.py            # User operations
│   │   ├── task.py            # Task operations
│   │   └── __init__.py
│   ├── dependencies/
│   │   ├── auth.py            # Dependency injection for auth
│   │   └── __init__.py
│   ├── middleware/
│   │   └── __init__.py        # CORS and logging middleware
│   └── utils/
│       └── __init__.py
├── tests/
│   ├── test_auth.py           # Authentication tests
│   └── __init__.py
├── requirements.txt           # Python dependencies
├── .env.example               # Environment variables template
├── Dockerfile                 # Docker configuration
├── docker-compose.yml         # Docker Compose setup
└── README.md                  # This file
```

## 🔧 Installation & Setup

### Prerequisites
- Python 3.11+
- PostgreSQL 12+ (or SQLite for development)
- Docker & Docker Compose (optional)

### 1. Clone and Setup

```bash
# Navigate to backend directory
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On Linux/Mac:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Configure Environment

```bash
# Copy example env file
cp .env.example .env

# Edit .env with your configuration
# Database URL, SECRET_KEY, etc.
```

### 3. Database Setup

```bash
# For PostgreSQL, create database:
createdb task_manager

# Update DATABASE_URL in .env:
DATABASE_URL=postgresql://user:password@localhost:5432/task_manager
```

### 4. Run Application

```bash
# Development mode
python -m uvicorn app.main:app --reload

# Production mode
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000
```

API will be available at: `http://localhost:8000`
- Swagger Docs: `http://localhost:8000/api/docs`
- ReDoc: `http://localhost:8000/api/redoc`
- Health Check: `http://localhost:8000/health`

## 🐳 Docker Setup

### Using Docker Compose

```bash
# Start all services (PostgreSQL, Redis, API)
docker-compose up -d

# View logs
docker-compose logs -f backend

# Stop services
docker-compose down
```

Services:
- Backend API: `http://localhost:8000`
- PostgreSQL: `localhost:5432`
- Redis: `localhost:6379`

## 🧪 Testing

```bash
# Run tests
pytest

# Run with coverage
pytest --cov=app tests/

# Run specific test file
pytest tests/test_auth.py
```

## 📚 API Endpoints

### Authentication Endpoints

#### Register User
```
POST /api/v1/auth/register
Content-Type: application/json

{
    "name": "John Doe",
    "email": "john@example.com",
    "password": "SecurePass123"
}

Response: 201 Created
{
    "id": 1,
    "name": "John Doe",
    "email": "john@example.com",
    "role": "user",
    "is_active": true,
    "created_at": "2024-01-15T10:30:00Z",
    "updated_at": "2024-01-15T10:30:00Z"
}
```

#### Login User
```
POST /api/v1/auth/login
Content-Type: application/json

{
    "email": "john@example.com",
    "password": "SecurePass123"
}

Response: 200 OK
{
    "access_token": "eyJhbGciOiJIUzI1NiIs...",
    "refresh_token": "eyJhbGciOiJIUzI1NiIs...",
    "token_type": "bearer",
    "expires_in": 1800
}
```

#### Get Current User
```
GET /api/v1/auth/me
Authorization: Bearer {access_token}

Response: 200 OK
{
    "id": 1,
    "name": "John Doe",
    "email": "john@example.com",
    "role": "user",
    "is_active": true,
    "created_at": "2024-01-15T10:30:00Z",
    "updated_at": "2024-01-15T10:30:00Z"
}
```

#### Refresh Token
```
POST /api/v1/auth/refresh
Content-Type: application/json

{
    "refresh_token": "eyJhbGciOiJIUzI1NiIs..."
}

Response: 200 OK
{
    "access_token": "eyJhbGciOiJIUzI1NiIs...",
    "token_type": "bearer",
    "expires_in": 1800
}
```

### Task Endpoints

#### Create Task
```
POST /api/v1/tasks
Authorization: Bearer {access_token}
Content-Type: application/json

{
    "title": "Complete project",
    "description": "Finish the backend development",
    "status": "pending"
}

Response: 201 Created
{
    "id": 1,
    "title": "Complete project",
    "description": "Finish the backend development",
    "status": "pending",
    "user_id": 1,
    "created_at": "2024-01-15T10:30:00Z",
    "updated_at": "2024-01-15T10:30:00Z"
}
```

#### Get Tasks
```
GET /api/v1/tasks?skip=0&limit=10&status=pending&search=project
Authorization: Bearer {access_token}

Response: 200 OK
{
    "total": 1,
    "skip": 0,
    "limit": 10,
    "data": [
        {
            "id": 1,
            "title": "Complete project",
            "description": "Finish the backend development",
            "status": "pending",
            "user_id": 1,
            "created_at": "2024-01-15T10:30:00Z",
            "updated_at": "2024-01-15T10:30:00Z"
        }
    ]
}
```

#### Get Task by ID
```
GET /api/v1/tasks/{task_id}
Authorization: Bearer {access_token}

Response: 200 OK
{
    "id": 1,
    "title": "Complete project",
    "description": "Finish the backend development",
    "status": "pending",
    "user_id": 1,
    "created_at": "2024-01-15T10:30:00Z",
    "updated_at": "2024-01-15T10:30:00Z"
}
```

#### Update Task
```
PUT /api/v1/tasks/{task_id}
Authorization: Bearer {access_token}
Content-Type: application/json

{
    "title": "Complete project",
    "description": "Finish the backend development",
    "status": "in_progress"
}

Response: 200 OK
{
    "id": 1,
    "title": "Complete project",
    "description": "Finish the backend development",
    "status": "in_progress",
    "user_id": 1,
    "created_at": "2024-01-15T10:30:00Z",
    "updated_at": "2024-01-15T10:35:00Z"
}
```

#### Delete Task
```
DELETE /api/v1/tasks/{task_id}
Authorization: Bearer {access_token}

Response: 204 No Content
```

### Admin Endpoints

#### Get All Users
```
GET /api/v1/admin/users?skip=0&limit=10&search=john
Authorization: Bearer {admin_token}

Response: 200 OK
{
    "total": 1,
    "skip": 0,
    "limit": 10,
    "data": [...]
}
```

#### Get User by ID
```
GET /api/v1/admin/users/{user_id}
Authorization: Bearer {admin_token}

Response: 200 OK
{...}
```

#### Update User
```
PUT /api/v1/admin/users/{user_id}
Authorization: Bearer {admin_token}
Content-Type: application/json

{
    "name": "Jane Doe",
    "email": "jane@example.com"
}

Response: 200 OK
{...}
```

#### Delete User
```
DELETE /api/v1/admin/users/{user_id}
Authorization: Bearer {admin_token}

Response: 204 No Content
```

#### Deactivate User
```
POST /api/v1/admin/users/{user_id}/deactivate
Authorization: Bearer {admin_token}

Response: 200 OK
{...}
```

## 🔐 Security Features

### Password Security
- Minimum 8 characters
- Must contain at least 1 digit
- Must contain at least 1 uppercase letter
- Hashed with bcrypt (cost factor: 12)

### JWT Authentication
- Access token expiration: 30 minutes
- Refresh token expiration: 7 days
- Algorithm: HS256
- Secure token validation

### Input Validation
- Email format validation
- Password strength requirements
- Pydantic schema validation
- SQL injection prevention via SQLAlchemy ORM

### CORS Protection
- Configurable allowed origins
- Credentials handling
- HTTP methods restriction

## 📊 Database Schema

### Users Table
```sql
CREATE TABLE users (
    id INTEGER PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    role ENUM('user', 'admin') DEFAULT 'user',
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);
```

### Tasks Table
```sql
CREATE TABLE tasks (
    id INTEGER PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    description TEXT,
    status ENUM('pending', 'in_progress', 'completed', 'cancelled') DEFAULT 'pending',
    user_id INTEGER NOT NULL,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW(),
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);
```

## 🚀 Scalability & Deployment

### Horizontal Scaling
- Stateless API design allows multiple instances
- Load balancer compatible (Nginx, HAProxy)
- Database connection pooling

### Caching Strategy
- Redis integration ready (docker-compose includes Redis)
- Cache-Control headers support
- Request ID tracking for debugging

### Performance Optimization
- Pagination for large datasets
- Database query optimization
- Connection pooling
- Async request handling

### Deployment Options

#### Development
```bash
uvicorn app.main:app --reload
```

#### Production with Gunicorn
```bash
pip install gunicorn
gunicorn app.main:app --workers 4 --worker-class uvicorn.workers.UvicornWorker
```

#### Docker
```bash
docker build -t task-api .
docker run -p 8000:8000 task-api
```

#### Kubernetes
Use the provided docker image with Kubernetes manifests

## 📝 Logging

Structured logging with:
- Request ID tracking
- Request/response logging
- Error logging with stack traces
- Performance metrics (request duration)

Log format:
```
[REQUEST_ID] METHOD PATH | Status: CODE | Duration: 0.123s
```

## 🔧 Environment Variables

```bash
# Database
DATABASE_URL=postgresql://user:password@localhost:5432/task_manager

# Security
SECRET_KEY=your-secret-key-min-32-chars
DEBUG=False

# JWT
ACCESS_TOKEN_EXPIRE_MINUTES=30
REFRESH_TOKEN_EXPIRE_DAYS=7

# Password
PASSWORD_MIN_LENGTH=8
```

## 🤝 Error Handling

Standard HTTP status codes:
- `200 OK` - Successful GET request
- `201 Created` - Successful POST request
- `204 No Content` - Successful DELETE request
- `400 Bad Request` - Validation error
- `401 Unauthorized` - Missing or invalid token
- `403 Forbidden` - Insufficient permissions
- `404 Not Found` - Resource not found
- `500 Internal Server Error` - Server error

## 📚 API Documentation

- **Swagger UI**: http://localhost:8000/api/docs
- **ReDoc**: http://localhost:8000/api/redoc
- **OpenAPI JSON**: http://localhost:8000/api/openapi.json

## 🔄 Continuous Integration/Deployment

Recommended CI/CD setup:
1. Run tests on every commit
2. Build Docker image
3. Push to registry
4. Deploy to staging
5. Run integration tests
6. Deploy to production

## 📦 Dependencies

See `requirements.txt` for complete list:
- FastAPI 0.104+
- SQLAlchemy 2.0+
- PostgreSQL driver (psycopg2)
- JWT handling (python-jose)
- Password hashing (passlib, bcrypt)
- Validation (Pydantic)

## 📄 License

MIT License - Feel free to use this project for learning and development.

## 🙋 Support

For issues or questions:
1. Check the API documentation at `/api/docs`
2. Review error messages and logs
3. Check database connectivity
4. Verify environment variables

## 🎯 Next Steps

- [ ] Implement Alembic migrations
- [ ] Add Redis caching
- [ ] Implement advanced search/filtering
- [ ] Add task comments/attachments
- [ ] Implement activity logging
- [ ] Add notification system
- [ ] Set up CI/CD pipeline
- [ ] Deploy to production

---

**Version**: 1.0.0  
**Last Updated**: January 15, 2024

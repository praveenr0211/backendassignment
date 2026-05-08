"""
Unit tests for authentication API.
"""
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.main import app, create_app
from app.database import Base, get_db
from app.schemas import UserRegister, UserLogin


# Test database
SQLALCHEMY_TEST_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(
    SQLALCHEMY_TEST_DATABASE_URL,
    connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def override_get_db():
    """Override get_db for testing."""
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


# Override dependency
app.dependency_overrides[get_db] = override_get_db

# Create test client
client = TestClient(app)


@pytest.fixture(autouse=True)
def setup_database():
    """Setup and teardown test database."""
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


def test_health_check():
    """Test health check endpoint."""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"


def test_register_user():
    """Test user registration."""
    user_data = {
        "name": "Test User",
        "email": "test@example.com",
        "password": "TestPass123"
    }
    response = client.post("/api/v1/auth/register", json=user_data)
    assert response.status_code == 201
    data = response.json()
    assert data["email"] == user_data["email"]
    assert data["name"] == user_data["name"]


def test_register_duplicate_email():
    """Test registration with duplicate email."""
    user_data = {
        "name": "Test User",
        "email": "test@example.com",
        "password": "TestPass123"
    }
    
    # First registration
    response1 = client.post("/api/v1/auth/register", json=user_data)
    assert response1.status_code == 201
    
    # Duplicate registration
    response2 = client.post("/api/v1/auth/register", json=user_data)
    assert response2.status_code == 400


def test_login_user():
    """Test user login."""
    # Register user first
    user_data = {
        "name": "Test User",
        "email": "test@example.com",
        "password": "TestPass123"
    }
    client.post("/api/v1/auth/register", json=user_data)
    
    # Login
    login_data = {
        "email": "test@example.com",
        "password": "TestPass123"
    }
    response = client.post("/api/v1/auth/login", json=login_data)
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert "refresh_token" in data
    assert data["token_type"] == "bearer"


def test_login_invalid_credentials():
    """Test login with invalid credentials."""
    # Register user first
    user_data = {
        "name": "Test User",
        "email": "test@example.com",
        "password": "TestPass123"
    }
    client.post("/api/v1/auth/register", json=user_data)
    
    # Login with wrong password
    login_data = {
        "email": "test@example.com",
        "password": "WrongPassword"
    }
    response = client.post("/api/v1/auth/login", json=login_data)
    assert response.status_code == 401


def test_get_current_user():
    """Test getting current user info."""
    # Register and login user
    user_data = {
        "name": "Test User",
        "email": "test@example.com",
        "password": "TestPass123"
    }
    client.post("/api/v1/auth/register", json=user_data)
    
    login_response = client.post("/api/v1/auth/login", json={
        "email": "test@example.com",
        "password": "TestPass123"
    })
    token = login_response.json()["access_token"]
    
    # Get current user
    response = client.get(
        "/api/v1/auth/me",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == "test@example.com"


def test_get_current_user_without_token():
    """Test getting current user without token."""
    response = client.get("/api/v1/auth/me")
    assert response.status_code == 403

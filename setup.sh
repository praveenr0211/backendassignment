#!/bin/bash

# Setup script for Task Management Application - Linux/Mac
# This script sets up both backend and frontend for development

set -e

echo "====================================="
echo "Task Management Application - Setup"
echo "====================================="
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "ERROR: Python 3 is not installed"
    echo "Please install Python 3.11+ from https://www.python.org"
    exit 1
fi

# Check if Node.js is installed
if ! command -v node &> /dev/null; then
    echo "ERROR: Node.js is not installed"
    echo "Please install Node.js from https://nodejs.org"
    exit 1
fi

echo "[OK] Python and Node.js are installed"
echo "Python version: $(python3 --version)"
echo "Node.js version: $(node --version)"
echo ""

# Setup Backend
echo "====================================="
echo "Setting up Backend..."
echo "====================================="

cd backend

# Check if venv exists
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
    echo "[OK] Virtual environment created"
else
    echo "[OK] Virtual environment already exists"
fi

# Activate venv
source venv/bin/activate
echo "[OK] Virtual environment activated"

# Install requirements
echo "Installing Python dependencies..."
pip install --upgrade pip
pip install -r requirements.txt
echo "[OK] Dependencies installed"

# Create .env file if it doesn't exist
if [ ! -f ".env" ]; then
    echo "Creating .env file..."
    cp .env.example .env
    echo "[OK] .env file created"
    echo "NOTE: Update .env with your database URL and settings"
else
    echo "[OK] .env file already exists"
fi

# Return to root directory
cd ..
echo ""

# Setup Frontend
echo "====================================="
echo "Setting up Frontend..."
echo "====================================="

cd frontend

# Install dependencies
echo "Installing Node dependencies..."
npm install
echo "[OK] Dependencies installed"

# Create .env file if it doesn't exist
if [ ! -f ".env" ]; then
    echo "Creating .env file..."
    cp .env.example .env
    echo "[OK] .env file created"
else
    echo "[OK] .env file already exists"
fi

# Return to root directory
cd ..
echo ""

# Print instructions
echo "====================================="
echo "Setup Complete!"
echo "====================================="
echo ""
echo "Next steps:"
echo ""
echo "1. Backend Setup:"
echo "   - Update backend/.env with your database configuration"
echo "   - Option A (SQLite - Quick Start):"
echo "     DATABASE_URL=sqlite:///./test.db"
echo "   - Option B (PostgreSQL - Production):"
echo "     DATABASE_URL=postgresql://user:password@localhost:5432/task_manager"
echo ""
echo "2. Start Backend:"
echo "   - cd backend"
echo "   - source venv/bin/activate"
echo "   - python -m uvicorn app.main:app --reload"
echo "   - Backend will run on http://localhost:8000"
echo ""
echo "3. Start Frontend:"
echo "   - cd frontend"
echo "   - npm run dev"
echo "   - Frontend will run on http://localhost:5173"
echo ""
echo "4. API Documentation:"
echo "   - Swagger UI: http://localhost:8000/api/docs"
echo "   - ReDoc: http://localhost:8000/api/redoc"
echo ""
echo "5. For Production Deployment:"
echo "   - See DEPLOYMENT.md for Render setup instructions"
echo "   - See PRODUCTION_CHECKLIST.md for deployment checklist"
echo ""
echo "====================================="
echo ""

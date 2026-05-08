@echo off
REM Setup script for Task Management Application - Windows
REM This script sets up both backend and frontend for development

setlocal enabledelayedexpansion

echo =====================================
echo Task Management Application - Setup
echo =====================================
echo.

REM Colors (Windows CMD doesn't support true colors, so we use labels)
echo Starting setup process...
echo.

REM Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.11+ from https://www.python.org
    pause
    exit /b 1
)

REM Check if Node.js is installed
node --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Node.js is not installed or not in PATH
    echo Please install Node.js from https://nodejs.org
    pause
    exit /b 1
)

echo [OK] Python and Node.js are installed
echo.

REM Setup Backend
echo =====================================
echo Setting up Backend...
echo =====================================
cd backend

REM Check if venv exists
if not exist "venv" (
    echo Creating virtual environment...
    python -m venv venv
    echo [OK] Virtual environment created
) else (
    echo [OK] Virtual environment already exists
)

REM Activate venv
call venv\Scripts\activate.bat
echo [OK] Virtual environment activated

REM Install requirements
echo Installing Python dependencies...
pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo ERROR: Failed to install dependencies
    pause
    exit /b 1
)
echo [OK] Dependencies installed

REM Create .env file if it doesn't exist
if not exist ".env" (
    echo Creating .env file...
    copy .env.example .env
    echo [OK] .env file created
    echo NOTE: Update .env with your database URL and settings
) else (
    echo [OK] .env file already exists
)

REM Return to root directory
cd ..
echo.

REM Setup Frontend
echo =====================================
echo Setting up Frontend...
echo =====================================
cd frontend

REM Install dependencies
echo Installing Node dependencies...
call npm install
if %errorlevel% neq 0 (
    echo ERROR: Failed to install npm dependencies
    pause
    exit /b 1
)
echo [OK] Dependencies installed

REM Create .env file if it doesn't exist
if not exist ".env" (
    echo Creating .env file...
    copy .env.example .env
    echo [OK] .env file created
) else (
    echo [OK] .env file already exists
)

REM Return to root directory
cd ..
echo.

REM Print instructions
echo =====================================
echo Setup Complete!
echo =====================================
echo.
echo Next steps:
echo.
echo 1. Backend Setup:
echo    - Update backend\.env with your database configuration
echo    - Option A (SQLite - Quick Start):
echo      DATABASE_URL=sqlite:///./test.db
echo    - Option B (PostgreSQL - Production):
echo      DATABASE_URL=postgresql://user:password@localhost:5432/task_manager
echo.
echo 2. Start Backend:
echo    - cd backend
echo    - venv\Scripts\activate
echo    - python -m uvicorn app.main:app --reload
echo    - Backend will run on http://localhost:8000
echo.
echo 3. Start Frontend:
echo    - cd frontend
echo    - npm run dev
echo    - Frontend will run on http://localhost:5173
echo.
echo 4. API Documentation:
echo    - Swagger UI: http://localhost:8000/api/docs
echo    - ReDoc: http://localhost:8000/api/redoc
echo.
echo 5. For Production Deployment:
echo    - See DEPLOYMENT.md for Render setup instructions
echo    - See PRODUCTION_CHECKLIST.md for deployment checklist
echo.
echo =====================================
echo.
pause

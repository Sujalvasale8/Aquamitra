@echo off
REM ========================================
REM Aquamitra - Windows Startup Script
REM ========================================

echo.
echo ========================================
echo   AQUAMITRA - Starting Backend Server
echo ========================================
echo.

REM Check if virtual environment exists
if not exist ".venv\Scripts\activate.bat" (
    echo ERROR: Virtual environment not found!
    echo Please run setup first:
    echo   python -m venv .venv
    echo   .venv\Scripts\activate
    echo   pip install -r requirements.txt
    pause
    exit /b 1
)

REM Activate virtual environment
call .venv\Scripts\activate.bat

REM Check if .env file exists
if not exist ".env" (
    echo WARNING: .env file not found!
    echo Creating .env from .env.example...
    copy .env.example .env
    echo.
    echo Please edit .env file and add your API keys:
    echo   - GROQ_API_KEY
    echo   - GOOGLE_API_KEY
    echo   - HF_TOKEN
    echo.
    echo Then run this script again.
    pause
    exit /b 1
)

echo Virtual environment activated
echo Starting FastAPI backend server...
echo.
echo Backend will run on: http://localhost:8000
echo.
echo ========================================
echo To start the frontend:
echo   1. Open a NEW Command Prompt
echo   2. cd chatbot-ui
echo   3. npm run dev
echo ========================================
echo.

REM Start the backend server
python server.py


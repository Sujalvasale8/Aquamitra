@echo off
REM ========================================
REM Aquamitra - Windows Setup Script
REM ========================================

echo.
echo ========================================
echo   AQUAMITRA - Windows Setup
echo ========================================
echo.

REM Check Python version
echo [Step 1/6] Checking Python version...
python --version 2>nul
if errorlevel 1 (
    echo ERROR: Python not found!
    echo Please install Python 3.11 from: https://www.python.org/downloads/
    pause
    exit /b 1
)

echo.
echo [Step 2/6] Creating virtual environment...
if exist ".venv" (
    echo Virtual environment already exists. Skipping...
) else (
    python -m venv .venv
    echo Virtual environment created successfully!
)

echo.
echo [Step 3/6] Activating virtual environment...
call .venv\Scripts\activate.bat

echo.
echo [Step 4/6] Upgrading pip...
python -m pip install --upgrade pip

echo.
echo [Step 5/6] Installing Python dependencies...
echo This may take 5-10 minutes...
pip install -r requirements.txt

echo.
echo [Step 6/6] Setting up environment file...
if exist ".env" (
    echo .env file already exists. Skipping...
) else (
    copy .env.example .env
    echo .env file created from .env.example
    echo.
    echo IMPORTANT: Please edit .env file and add your API keys:
    echo   - GROQ_API_KEY (Get from: https://console.groq.com/keys)
    echo   - GOOGLE_API_KEY (Get from: https://aistudio.google.com/app/apikey)
    echo   - HF_TOKEN (Get from: https://huggingface.co/settings/tokens)
    echo.
)

echo.
echo ========================================
echo   Backend Setup Complete!
echo ========================================
echo.
echo Next steps:
echo   1. Edit .env file and add your API keys
echo   2. Install frontend dependencies:
echo      cd chatbot-ui
echo      npm install
echo   3. Start the backend: start-windows.bat
echo   4. Start the frontend: cd chatbot-ui ^&^& npm run dev
echo.
pause


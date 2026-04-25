@echo off
setlocal enabledelayedexpansion

echo.
echo ===================================================
echo           IAN GPT Assistant - Setup ^& Run          
echo ===================================================
echo.

:: 1. Check for Python
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Python is not installed or not in PATH.
    echo Please install Python from https://www.python.org/
    pause
    exit /b
)

:: 2. Create virtual environment if it doesn't exist
if not exist ".venv" (
    echo [INFO] Creating virtual environment...
    python -m venv .venv
    if !errorlevel! neq 0 (
        echo [ERROR] Failed to create virtual environment.
        pause
        exit /b
    )
)

:: 3. Activate virtual environment
echo [INFO] Activating virtual environment...
call .venv\Scripts\activate

:: 4. Upgrade pip and build tools
echo [INFO] Updating installation tools...
python -m pip install --upgrade pip setuptools wheel >nul 2>&1

:: 5. Install requirements
echo [INFO] Installing/Checking dependencies...
pip install -r requirements.txt
if !errorlevel! neq 0 (
    echo.
    echo [ERROR] Dependency installation failed.
    echo If the error was about 'pythonnet', you may need Visual Studio Build Tools.
    echo Check the 'artifacts' folder for instructions.
    pause
    exit /b
)

:: 6. Check for .env file
if not exist ".env" (
    echo [WARNING] .env file not found.
    if exist ".env.example" (
        echo [INFO] Creating .env from .env.example...
        copy .env.example .env >nul
        echo [ACTION REQUIRED] Please open the '.env' file and add your OPENROUTER_API_KEY.
        notepad .env
    ) else (
        echo [ERROR] .env.example not found. Please create a .env file manually.
    )
    echo.
    echo After adding your API key, run this script again.
    pause
    exit /b
)

:: 7. Run the GUI
echo [INFO] Starting IAN GPT...
python gui.py
if !errorlevel! neq 0 (
    echo.
    echo [INFO] App closed with exit code !errorlevel!.
)

pause

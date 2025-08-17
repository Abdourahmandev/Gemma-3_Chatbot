@echo off
echo ============================================
echo    Gemma 3 ChatBot - Auto Installer
echo ============================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.8+ from https://python.org
    pause
    exit /b 1
)

REM Check if Ollama is installed
ollama --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Ollama is not installed
    echo.
    echo Please install Ollama first:
    echo 1. Visit https://ollama.ai/download
    echo 2. Download and install Ollama
    echo 3. Run this installer again
    pause
    exit /b 1
)

echo [1/5] Setting up Python environment...
if not exist "venv" (
    python -m venv venv
)

echo [2/5] Activating environment...
call venv\Scripts\activate.bat

echo [3/5] Installing Python packages...
pip install -r requirements.txt

echo [4/5] Checking Ollama service...
ollama list >nul 2>&1
if %errorlevel% neq 0 (
    echo Starting Ollama service...
    start /min ollama serve
    timeout /t 3
)

echo [5/5] Checking for Gemma 3 model...
ollama list | findstr "gemma3" >nul
if %errorlevel% neq 0 (
    echo.
    echo Gemma 3 model not found. Would you like to download it now?
    echo This will download approximately 3.3GB of data.
    set /p download="Download Gemma 3 model? (y/n): "
    if /i "!download!"=="y" (
        echo Downloading Gemma 3 model... This may take several minutes.
        ollama pull gemma3:latest
    ) else (
        echo You can download the model later with: ollama pull gemma3:latest
    )
)

echo.
echo ============================================
echo Installation complete!
echo ============================================
echo.
echo To start the ChatBot:
echo 1. Run: start_chatbot.bat
echo 2. Or double-click the "Start ChatBot" shortcut
echo.
pause

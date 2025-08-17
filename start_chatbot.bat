@echo off
echo Starting Gemma 3 ChatBot...
echo.

REM Activate virtual environment
call venv\Scripts\activate.bat

REM Start Ollama if not running
ollama list >nul 2>&1
if %errorlevel% neq 0 (
    echo Starting Ollama service...
    start /min ollama serve
    timeout /t 5
)

REM Start the Streamlit app
echo Opening ChatBot in your browser...
echo Close this window to stop the ChatBot.
echo.
streamlit run app.py --server.headless true --server.port 8501

pause

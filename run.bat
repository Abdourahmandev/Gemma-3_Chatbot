@echo off
echo Activating virtual environment...
call .\venv\Scripts\Activate.bat

echo Starting Streamlit ChatBot...
echo.
echo Make sure Ollama is running and has the Gemma model installed:
echo   ollama serve
echo   ollama pull gemma3:latest
echo.
echo Starting application...
streamlit run app.py

# build.py - Script to create standalone executable
import PyInstaller.__main__
import os

# Build the standalone executable
PyInstaller.__main__.run([
    '--name=Gemma3-ChatBot',
    '--onefile',
    '--windowed',
    '--add-data=chat_history;chat_history',
    '--hidden-import=streamlit',
    '--hidden-import=ollama',
    '--hidden-import=requests',
    'app.py'
])

print("Build complete! Check the 'dist' folder for Gemma3-ChatBot.exe")

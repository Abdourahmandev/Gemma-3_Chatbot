# Gemma 3 ChatBot with Streamlit and Ollama

A simple chatbot application built with Streamlit that uses the Gemma 3 model via Ollama.

## Features

- Interactive chat interface
- Persistent chat history
- Real-time responses from Gemma 3 model
- Error handling and connection validation
- Clean and intuitive UI

## Prerequisites

- Python 3.8 or higher
- Ollama installed on your system

## Setup Instructions

### 1. Install Ollama

Download and install Ollama from [https://ollama.ai/](https://ollama.ai/)

### 2. Download Gemma 3 Model

Open a terminal and run:
```bash
ollama pull gemma3:latest
```

### 3. Start Ollama Service

```bash
ollama serve
```

### 4. Install Python Dependencies

Create a virtual environment and install dependencies:
```bash
python -m venv venv
venv\Scripts\activate  # On Windows
# source venv/bin/activate  # On macOS/Linux

pip install -r requirements.txt
```

### 5. Run the Application

```bash
streamlit run app.py
```

## Easy Installation Options

### 🚀 Option 1: Auto-Installer (Recommended)
1. Download the entire project folder
2. Double-click `install.bat` 
3. Follow the prompts (it will install everything automatically)
4. Double-click `start_chatbot.bat` to run the app

### 💻 Option 2: Desktop App (Electron)
1. Install Node.js from https://nodejs.org
2. Run: `npm install` then `npm run dist`
3. Install the generated `.exe` file from `dist-electron` folder

### 🐳 Option 3: Docker Container
```bash
docker build -t gemma3-chatbot .
docker run -p 8501:8501 gemma3-chatbot
```

## Usage

1. Open your browser to the URL shown in the terminal (usually http://localhost:8501)
2. Start chatting with the Gemma 3 model!
3. Your chat history will be automatically saved and restored between sessions

## Troubleshooting

- **"Connection refused" error**: Make sure Ollama is running (`ollama serve`)
- **"Model not found" error**: Make sure you've downloaded the Gemma model (`ollama pull gemma3:latest`)
- **Slow responses**: Consider using the smaller 2b model instead of 9b for faster responses

## File Structure

```
Gemma 3/
├── app.py              # Main Streamlit application
├── requirements.txt    # Python dependencies
├── README.md          # This file
└── chat_history/      # Directory for storing chat history files
```

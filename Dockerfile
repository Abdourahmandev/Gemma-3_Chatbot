FROM python:3.11-slim

# Install system dependencies
RUN apt-get update && apt-get install -y \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Install Ollama
RUN curl -fsSL https://ollama.ai/install.sh | sh

# Set working directory
WORKDIR /app

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install -r requirements.txt

# Copy application files
COPY app.py .
COPY chat_history ./chat_history

# Expose port
EXPOSE 8501

# Start script
COPY start-docker.sh .
RUN chmod +x start-docker.sh

CMD ["./start-docker.sh"]

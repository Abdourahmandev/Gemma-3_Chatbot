import streamlit as st
import ollama
import json
import os
from datetime import datetime
from typing import List, Dict
import requests

# Configuration
MODEL_NAME = "gemma3:latest"  # Using the latest Gemma 3 model
CHAT_HISTORY_DIR = "chat_history"
MAX_CONTEXT_LENGTH = 4000  # Maximum tokens to keep in context

class ChatHistoryManager:
    """Manages chat history persistence and loading"""
    
    def __init__(self):
        self.ensure_history_dir()
    
    def ensure_history_dir(self):
        """Ensure the chat history directory exists"""
        if not os.path.exists(CHAT_HISTORY_DIR):
            os.makedirs(CHAT_HISTORY_DIR)
    
    def save_history(self, messages: List[Dict]):
        """Save chat history to a JSON file"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"chat_{timestamp}.json"
        filepath = os.path.join(CHAT_HISTORY_DIR, filename)
        
        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump({
                    'timestamp': datetime.now().isoformat(),
                    'messages': messages
                }, f, indent=2, ensure_ascii=False)
        except Exception as e:
            st.error(f"Failed to save chat history: {str(e)}")
    
    def load_latest_history(self) -> List[Dict]:
        """Load the most recent chat history"""
        try:
            files = [f for f in os.listdir(CHAT_HISTORY_DIR) if f.endswith('.json')]
            if not files:
                return []
            
            latest_file = max(files, key=lambda x: os.path.getctime(os.path.join(CHAT_HISTORY_DIR, x)))
            filepath = os.path.join(CHAT_HISTORY_DIR, latest_file)
            
            with open(filepath, 'r', encoding='utf-8') as f:
                data = json.load(f)
                return data.get('messages', [])
        except Exception as e:
            st.warning(f"Could not load chat history: {str(e)}")
            return []
    
    def clear_history(self):
        """Clear all chat history files"""
        try:
            files = [f for f in os.listdir(CHAT_HISTORY_DIR) if f.endswith('.json')]
            for file in files:
                os.remove(os.path.join(CHAT_HISTORY_DIR, file))
            return True
        except Exception as e:
            st.error(f"Failed to clear history: {str(e)}")
            return False

def check_ollama_connection():
    """Check if Ollama is running and the model is available"""
    try:
        # Check if Ollama is running
        response = requests.get("http://localhost:11434/api/tags", timeout=5)
        if response.status_code == 200:
            models = response.json().get('models', [])
            model_names = [model['name'] for model in models]
            
            # Check if our model is available
            if any(MODEL_NAME in name for name in model_names):
                return True, "Connected to Ollama and model is available"
            else:
                return False, f"Model '{MODEL_NAME}' not found. Available models: {model_names}"
        else:
            return False, "Ollama is not responding"
    except requests.RequestException:
        return False, "Cannot connect to Ollama. Make sure it's running on localhost:11434"

def get_ollama_response(messages: List[Dict]) -> str:
    """Get response from Ollama"""
    try:
        # Prepare messages for Ollama
        formatted_messages = []
        for msg in messages:
            formatted_messages.append({
                "role": msg["role"],
                "content": msg["content"]
            })
        
        # Get response from Ollama
        response = ollama.chat(
            model=MODEL_NAME,
            messages=formatted_messages,
            options={
                "temperature": 0.7,
                "top_p": 0.9,
                "max_tokens": 500,
            }
        )
        
        return response['message']['content']
    
    except Exception as e:
        return f"Error getting response from Ollama: {str(e)}"

def truncate_context(messages: List[Dict], max_length: int = MAX_CONTEXT_LENGTH) -> List[Dict]:
    """Truncate conversation context to prevent token limit issues"""
    if len(messages) <= 2:  # Keep at least system message and one exchange
        return messages
    
    # Estimate token count (rough approximation: 1 token ≈ 4 characters)
    total_chars = sum(len(msg["content"]) for msg in messages)
    
    if total_chars <= max_length * 4:
        return messages
    
    # Keep system message (if any) and recent messages
    truncated = []
    if messages and messages[0]["role"] == "system":
        truncated.append(messages[0])
        remaining_messages = messages[1:]
    else:
        remaining_messages = messages
    
    # Add recent messages until we approach the limit
    current_chars = len(truncated[0]["content"]) if truncated else 0
    
    for msg in reversed(remaining_messages):
        msg_chars = len(msg["content"])
        if current_chars + msg_chars <= max_length * 4:
            truncated.insert(-1 if len(truncated) > 0 else 0, msg)
            current_chars += msg_chars
        else:
            break
    
    return truncated

def main():
    # Page configuration
    st.set_page_config(
        page_title="Gemma 3 ChatBot",
        page_icon="🤖",
        layout="wide"
    )
    
    # Initialize chat history manager
    history_manager = ChatHistoryManager()
    
    # Title and description
    st.title("🤖 Gemma 3 ChatBot")
    st.markdown("Chat with the Gemma 3 model powered by Ollama")
    
    # Sidebar for settings and controls
    with st.sidebar:
        st.header("Settings")
        
        # Connection status
        st.subheader("Connection Status")
        is_connected, status_message = check_ollama_connection()
        
        if is_connected:
            st.success(status_message)
        else:
            st.error(status_message)
            st.markdown("**Troubleshooting:**")
            st.markdown("1. Make sure Ollama is running: `ollama serve`")
            st.markdown(f"2. Make sure the model is installed: `ollama pull {MODEL_NAME}`")
        
        st.divider()
        
        # Chat controls
        st.subheader("Chat Controls")
        
        if st.button("🗑️ Clear Chat History", type="secondary"):
            if history_manager.clear_history():
                st.session_state.messages = []
                st.success("Chat history cleared!")
                st.rerun()
        
        if st.button("📁 Load Previous Chat", type="secondary"):
            loaded_messages = history_manager.load_latest_history()
            if loaded_messages:
                st.session_state.messages = loaded_messages
                st.success("Previous chat loaded!")
                st.rerun()
            else:
                st.info("No previous chat found")
        
        st.divider()
        
        # Model information
        st.subheader("Model Information")
        st.info(f"**Model:** {MODEL_NAME}")
        st.info(f"**Context Window:** {MAX_CONTEXT_LENGTH} tokens")
    
    # Initialize chat history in session state
    if "messages" not in st.session_state:
        st.session_state.messages = []
    
    # Display chat history
    chat_container = st.container()
    
    with chat_container:
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])
                if "timestamp" in message:
                    st.caption(f"Sent at: {message['timestamp']}")
    
    # Chat input
    if prompt := st.chat_input("Type your message here...", disabled=not is_connected):
        # Add user message to chat history
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        user_message = {
            "role": "user", 
            "content": prompt,
            "timestamp": timestamp
        }
        st.session_state.messages.append(user_message)
        
        # Display user message
        with st.chat_message("user"):
            st.markdown(prompt)
            st.caption(f"Sent at: {timestamp}")
        
        # Get bot response
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                # Truncate context if needed
                context_messages = truncate_context(st.session_state.messages)
                
                # Get response from Ollama
                response = get_ollama_response(context_messages)
                
                # Display response
                st.markdown(response)
                
                # Add bot response to chat history
                bot_timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                bot_message = {
                    "role": "assistant",
                    "content": response,
                    "timestamp": bot_timestamp
                }
                st.session_state.messages.append(bot_message)
                
                st.caption(f"Response at: {bot_timestamp}")
        
        # Save chat history after each exchange
        history_manager.save_history(st.session_state.messages)
        
        # Rerun to update the chat display
        st.rerun()
    
    # Footer
    st.markdown("---")
    st.markdown(
        "💡 **Tip:** Your chat history is automatically saved and can be loaded from the sidebar."
    )

if __name__ == "__main__":
    main()

import streamlit as st
import google.generativeai as genai
from datetime import datetime
import pytz

# --- PAGE CONFIGURATION ---
st.set_page_config(
    page_title="My AI Chatbot",
    page_icon="🤖",
    layout="centered"
)

# --- MAIN CHATBOT LOGIC ---
st.title("🤖 My Personal AI Chatbot")

# Get current time in India and format it
try:
    indian_timezone = pytz.timezone("Asia/Kolkata")
    current_indian_time = datetime.now(indian_timezone).strftime("%I:%M %p")
    st.caption(f"Powered by Google Gemini | Current time in India: {current_indian_time}")
except Exception as e:
    st.caption("Powered by Google Gemini")


def initialize_chat():
    """Initializes the model using the API key from secrets."""
    try:
        # Configure the model with the secret API key
        api_key = st.secrets["GOOGLE_API_KEY"]
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-1.5-flash')
        return model.start_chat(history=[])
    except (KeyError, FileNotFoundError):
        st.error("API key not found. Please add the `GOOGLE_API_KEY` to your Streamlit secrets.")
        return None
    except Exception as e:
        st.error(f"An error occurred during initialization: {e}")
        return None

# --- SESSION STATE MANAGEMENT ---
# Initialize chat history and the chat model itself
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "chat" not in st.session_state:
    st.session_state.chat = initialize_chat()


# --- SIDEBAR ---
st.sidebar.title("Configuration")
if st.sidebar.button("Clear Chat History"):
    st.session_state.chat_history = []
    # No need to re-initialize the chat model here unless the key changes
    st.rerun()


# --- DISPLAY CHAT HISTORY ---
# Display previous messages from the chat history
if st.session_state.chat:
    for message in st.session_state.chat_history:
        with st.chat_message(name=message["role"], avatar="🧑‍💻" if message["role"] == "user" else "🤖"):
            st.markdown(message["parts"])
else:
    st.warning("Chatbot is not initialized. Please check your Streamlit secrets configuration.")


# --- USER INPUT HANDLING ---
user_prompt = st.chat_input("Ask me anything...")

if user_prompt and st.session_state.chat:
    # Add user's message to the history and display it
    st.session_state.chat_history.append({"role": "user", "parts": user_prompt})
    with st.chat_message("user", avatar="🧑‍💻"):
        st.markdown(user_prompt)

    # Get the AI's response
    with st.spinner("Thinking..."):
        try:
            response = st.session_state.chat.send_message(user_prompt)
            # Add AI's response to the history and display it
            st.session_state.chat_history.append({"role": "model", "parts": response.text})
            with st.chat_message("model", avatar="🤖"):
                st.markdown(response.text)
        except Exception as e:
            st.error(f"An error occurred while getting the response: {e}")

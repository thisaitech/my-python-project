import streamlit as st
import google.generativeai as genai
import os

# --- PAGE CONFIGURATION ---
# Set the page title and icon for your app
st.set_page_config(
    page_title="My AI Chatbot",
    page_icon="🤖",
    layout="centered" 
)

# --- SIDEBAR FOR API KEY ---
# Create a sidebar for users to enter their API key
st.sidebar.title("Configuration")
st.sidebar.markdown("Enter your Google AI API Key to start chatting.")

# It's best practice to use st.secrets for deployment, but for a local demo,
# we'll use an input field.
api_key = st.sidebar.text_input("Google AI API Key", type="password")

# --- MAIN CHATBOT LOGIC ---
st.title("🤖 My Personal AI Chatbot")
st.caption(f"Powered by Google Gemini | Current Time in India: {st.experimental_get_query_params().get('time', [''])[0]}") # Little dynamic touch

def initialize_chat():
    """Initializes the Generative AI model and chat session."""
    try:
        # Configure the generative AI model with the API key
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-1.5-flash')
        
        # Start a chat session
        return model.start_chat(history=[])
    except Exception as e:
        # Handle potential exceptions like invalid API key
        st.error(f"Failed to initialize the model. Please check your API key. Error: {e}")
        return None

# --- SESSION STATE MANAGEMENT ---
# Initialize chat history in Streamlit's session state if it doesn't exist
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "chat" not in st.session_state:
    st.session_state.chat = None

# If an API key is provided, initialize the chat model
if api_key:
    # Only initialize if it hasn't been done yet
    if not st.session_state.chat:
        st.session_state.chat = initialize_chat()
else:
    # Display a warning if the API key is missing
    st.warning("Please enter your Google AI API Key in the sidebar to begin.")


# --- DISPLAY CHAT HISTORY ---
# Display previous messages from the chat history
if st.session_state.chat:
    for message in st.session_state.chat_history:
        # Use the 'avatar' parameter to set custom icons
        with st.chat_message(name=message["role"], avatar="🧑‍💻" if message["role"] == "user" else "🤖"):
            st.markdown(message["parts"])


# --- USER INPUT HANDLING ---
# Get user input from the chat input box at the bottom of the page
user_prompt = st.chat_input("Ask me anything...")

if user_prompt and st.session_state.chat:
    # 1. Add user's message to the history and display it
    st.session_state.chat_history.append({"role": "user", "parts": user_prompt})
    with st.chat_message("user", avatar="🧑‍💻"):
        st.markdown(user_prompt)

    # 2. Get the AI's response
    with st.spinner("Thinking..."):
        try:
            # Send the prompt to the AI model
            response = st.session_state.chat.send_message(user_prompt)
            
            # 3. Add AI's response to the history and display it
            st.session_state.chat_history.append({"role": "model", "parts": response.text})
            with st.chat_message("model", avatar="🤖"):
                st.markdown(response.text)
        except Exception as e:
            st.error(f"An error occurred while getting the response: {e}")

# A button in the sidebar to clear the chat history
if st.sidebar.button("Clear Chat History"):
    st.session_state.chat_history = []
    st.session_state.chat = initialize_chat() # Restart the chat session
    st.experimental_rerun() # Rerun the app to reflect the changes
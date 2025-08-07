import streamlit as st
import time
from model_handler import generate_response
from modes import MODES  # MODES is now a dict: {"Display": "internal"}

# Configure page
st.set_page_config(page_title="Techtonic AI", page_icon="🤖", layout="wide")

# Initialize session state
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

if "is_loading" not in st.session_state:
    st.session_state.is_loading = False

if "current_mode" not in st.session_state:
    st.session_state.current_mode = list(MODES.keys())[0]

if "show_chat" not in st.session_state:
    st.session_state.show_chat = len(st.session_state.chat_history) > 0

if "suggestion_clicked" not in st.session_state:
    st.session_state.suggestion_clicked = ""

if "trigger_send" not in st.session_state:
    st.session_state.trigger_send = False

# Inject Gemini-inspired CSS
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Google+Sans:wght@400;500;700&display=swap');
    
    /* Global Reset */
    * {
        margin: 0;
        padding: 0;
        box-sizing: border-box;
    }
    
    body, html {
        font-family: 'Google Sans', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
        background-color: #131314;
        color: #e8eaed;
        height: 100vh;
        overflow: hidden;
    }
    
    .stApp {
        background-color: #131314;
        height: 100vh;
    }
    
    /* Hide Streamlit elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .stDeployButton {visibility: hidden;}
    
    /* Hide sidebar */
    .css-1d391kg {
        display: none;
    }
    
    /* Main container */
    .main-container {
        height: 100vh;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        padding: 0 24px;
        max-width: 768px;
        margin: 0 auto;
    }
    
    /* Top bar */
    .top-bar {
        position: fixed;
        top: 0;
        left: 0;
        right: 0;
        height: 64px;
        background-color: #131314;
        display: flex;
        align-items: center;
        justify-content: space-between;
        padding: 0 24px;
        z-index: 100;
        border-bottom: 1px solid #292a2d;
    }
    
    .logo {
        font-size: 22px;
        font-weight: 400;
        color: #e8eaed;
        display: flex;
        align-items: center;
        gap: 8px;
    }
    
    .version {
        font-size: 14px;
        color: #9aa0a6;
        margin-left: 8px;
        display: flex;
        align-items: center;
        gap: 4px;
    }
    
    .top-right {
        display: flex;
        align-items: center;
        gap: 16px;
    }
    
    .pro-badge {
        background-color: #1a73e8;
        color: white;
        padding: 4px 12px;
        border-radius: 16px;
        font-size: 12px;
        font-weight: 500;
    }
    
    .profile-icon {
        width: 32px;
        height: 32px;
        border-radius: 50%;
        background: linear-gradient(45deg, #4285f4, #ea4335, #fbbc04, #34a853);
        display: flex;
        align-items: center;
        justify-content: center;
        color: white;
        font-weight: 500;
        font-size: 14px;
    }
    
    /* Welcome section */
    .welcome-section {
        text-align: center;
        margin-bottom: 48px;
    }
    
    .welcome-title {
        font-size: 56px;
        font-weight: 400;
        background: linear-gradient(45deg, #4285f4, #34a853, #ea4335, #fbbc04);
        background-clip: text;
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 8px;
    }
    
    .welcome-subtitle {
        font-size: 18px;
        color: #9aa0a6;
        font-weight: 400;
    }
    
    /* Suggestion cards */
    .suggestions {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
        gap: 16px;
        margin-bottom: 48px;
        width: 100%;
        max-width: 800px;
    }
    
    .suggestion-card {
        background-color: #1e1f20;
        border: 1px solid #292a2d;
        border-radius: 16px;
        padding: 20px;
        cursor: pointer;
        transition: all 0.2s ease;
        position: relative;
        overflow: hidden;
    }
    
    .suggestion-card:hover {
        background-color: #262729;
        border-color: #3c4043;
        transform: translateY(-2px);
    }
    
    .suggestion-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 1px;
        background: linear-gradient(90deg, transparent, rgba(66, 133, 244, 0.5), transparent);
        opacity: 0;
        transition: opacity 0.2s ease;
    }
    
    .suggestion-card:hover::before {
        opacity: 1;
    }
    
    .suggestion-title {
        font-size: 16px;
        font-weight: 500;
        color: #e8eaed;
        margin-bottom: 8px;
    }
    
    .suggestion-subtitle {
        font-size: 14px;
        color: #9aa0a6;
        line-height: 1.4;
    }
    
    /* Input container */
    .input-container {
        position: fixed;
        bottom: 24px;
        left: 50%;
        transform: translateX(-50%);
        width: calc(100% - 48px);
        max-width: 720px;
        z-index: 50;
    }
    
    .input-wrapper {
        background-color: #1e1f20;
        border: 1px solid #292a2d;
        border-radius: 24px;
        padding: 16px 20px;
        display: flex;
        align-items: flex-end;
        gap: 12px;
        transition: all 0.2s ease;
        box-shadow: 0 4px 16px rgba(0, 0, 0, 0.2);
    }
    
    .input-wrapper:focus-within {
        border-color: #4285f4;
        box-shadow: 0 4px 20px rgba(66, 133, 244, 0.15);
    }
    
    .input-field {
        flex: 1;
        background: transparent;
        border: none;
        outline: none;
        color: #e8eaed;
        font-size: 16px;
        font-family: 'Google Sans', sans-serif;
        resize: none;
        min-height: 24px;
        max-height: 120px;
        overflow-y: auto;
    }
    
    .input-field::placeholder {
        color: #9aa0a6;
    }
    
    .send-button {
        width: 32px;
        height: 32px;
        border-radius: 50%;
        background-color: #4285f4;
        border: none;
        display: flex;
        align-items: center;
        justify-content: center;
        cursor: pointer;
        transition: all 0.2s ease;
        color: white;
        font-size: 16px;
        opacity: 0;
        transform: scale(0.8);
    }
    
    .send-button.visible {
        opacity: 1;
        transform: scale(1);
    }
    
    .send-button:hover {
        background-color: #1a73e8;
        transform: scale(1.05);
    }
    
    /* Chat messages */
    .chat-messages {
        position: fixed;
        top: 64px;
        left: 0;
        right: 0;
        bottom: 120px;
        overflow-y: auto;
        padding: 24px;
        display: none;
    }
    
    .chat-messages.show {
        display: block;
    }
    
    .message {
        max-width: 768px;
        margin: 0 auto 24px;
        animation: fadeInUp 0.5s ease-out;
    }
    
    .message.user {
        text-align: right;
    }
    
    .message-content {
        display: inline-block;
        max-width: 80%;
        padding: 16px 20px;
        border-radius: 18px;
        font-size: 16px;
        line-height: 1.5;
    }
    
    .message.user .message-content {
        background-color: #4285f4;
        color: white;
        border-bottom-right-radius: 6px;
    }
    
    .message.assistant .message-content {
        background-color: #1e1f20;
        color: #e8eaed;
        border: 1px solid #292a2d;
        border-bottom-left-radius: 6px;
        text-align: left;
    }
    
    /* Loading animation */
    .loading {
        display: flex;
        justify-content: center;
        align-items: center;
        padding: 20px;
    }
    
    .loading-dots {
        display: flex;
        gap: 6px;
    }
    
    .loading-dot {
        width: 8px;
        height: 8px;
        border-radius: 50%;
        background-color: #4285f4;
        animation: pulse 1.4s infinite ease-in-out;
    }
    
    .loading-dot:nth-child(1) { animation-delay: -0.32s; }
    .loading-dot:nth-child(2) { animation-delay: -0.16s; }
    .loading-dot:nth-child(3) { animation-delay: 0s; }
    
    /* Animations */
    @keyframes fadeInUp {
        from {
            opacity: 0;
            transform: translateY(20px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    @keyframes pulse {
        0%, 80%, 100% {
            transform: scale(0);
            opacity: 0.5;
        }
        40% {
            transform: scale(1);
            opacity: 1;
        }
    }
    
    /* Hide Streamlit components */
    .stTextArea > div > div > textarea {
        display: none;
    }
    
    .stSelectbox {
        display: none;
    }
    
    .stButton {
        display: none;
    }
    
    .stColumns {
        display: none;
    }
    
    /* Responsive */
    @media (max-width: 768px) {
        .welcome-title {
            font-size: 42px;
        }
        
        .suggestions {
            grid-template-columns: 1fr;
        }
        
        .input-container {
            width: calc(100% - 32px);
        }
        
        .top-bar {
            padding: 0 16px;
        }
        
        .chat-messages {
            padding: 16px;
        }
    }
    </style>
""", unsafe_allow_html=True)

# Create suggestion cards data
suggestions = [
    ("Simulate", "a virtual ecosystem"),
    ("Analyze consequences", "of space exploration"), 
    ("Compare teachings", "of Plato and Aristotle"),
    ("Model spread", "of contagious diseases")
]

# Top bar
st.markdown(f"""
    <div class="top-bar">
        <div class="logo">
            Techtonic AI
            <div class="version">
                2.5 Pro
                <svg width="12" height="12" viewBox="0 0 12 12" fill="currentColor">
                    <path d="M6 1L7.5 4.5L11 4.5L8.25 7L9.5 10.5L6 8.5L2.5 10.5L3.75 7L1 4.5L4.5 4.5L6 1Z"/>
                </svg>
            </div>
        </div>
        <div class="top-right">
            <div class="pro-badge">PRO</div>
            <div class="profile-icon">S</div>
        </div>
    </div>
""", unsafe_allow_html=True)

# Handle suggestion clicks
if st.session_state.suggestion_clicked:
    st.session_state.show_chat = True
    st.session_state.is_loading = True
    st.session_state.chat_history.append((st.session_state.suggestion_clicked, ""))
    st.session_state.suggestion_clicked = ""
    st.rerun()

# Main content area
if not st.session_state.show_chat:
    # Welcome screen
    st.markdown("""
        <div class="main-container">
            <div class="welcome-section">
                <div class="welcome-title">Hello, Saksham</div>
                <div class="welcome-subtitle">Creative Text Engine</div>
            </div>
            
            <div class="suggestions">
    """, unsafe_allow_html=True)
    
    # Create clickable suggestion cards using Streamlit buttons
    col1, col2 = st.columns(2)
    for i, (title, subtitle) in enumerate(suggestions):
        suggestion_text = f"{title} {subtitle}"
        with col1 if i % 2 == 0 else col2:
            if st.button(f"{title}\n{subtitle}", key=f"suggestion_{i}", help=suggestion_text, use_container_width=True):
                st.session_state.suggestion_clicked = suggestion_text
                st.rerun()
    
    st.markdown("</div></div>", unsafe_allow_html=True)
    
    # Add custom styling for suggestion buttons
    st.markdown("""
        <style>
        .stButton > button {
            background-color: #1e1f20 !important;
            border: 1px solid #292a2d !important;
            border-radius: 16px !important;
            padding: 20px !important;
            height: auto !important;
            white-space: pre-line !important;
            text-align: left !important;
            transition: all 0.2s ease !important;
            color: #e8eaed !important;
            font-family: 'Google Sans', sans-serif !important;
        }
        
        .stButton > button:hover {
            background-color: #262729 !important;
            border-color: #3c4043 !important;
            transform: translateY(-2px) !important;
            color: #e8eaed !important;
        }
        
        .stButton > button:focus {
            background-color: #262729 !important;
            border-color: #4285f4 !important;
            color: #e8eaed !important;
            box-shadow: none !important;
        }
        
        .stButton {
            margin-bottom: 16px !important;
        }
        </style>
    """, unsafe_allow_html=True)
    
else:
    # Chat view
    st.markdown(f"""
        <div class="chat-messages show">
    """, unsafe_allow_html=True)
    
    # Display loading if generating
    if st.session_state.is_loading:
        st.markdown("""
            <div class="loading">
                <div class="loading-dots">
                    <div class="loading-dot"></div>
                    <div class="loading-dot"></div>
                    <div class="loading-dot"></div>
                </div>
            </div>
        """, unsafe_allow_html=True)
    
    # Display messages
    for user_msg, bot_reply in st.session_state.chat_history:
        st.markdown(f"""
            <div class="message user">
                <div class="message-content">{user_msg}</div>
            </div>
        """, unsafe_allow_html=True)
        
        if bot_reply:
            st.markdown(f"""
                <div class="message assistant">
                    <div class="message-content">{bot_reply}</div>
                </div>
            """, unsafe_allow_html=True)
    
    st.markdown("</div>", unsafe_allow_html=True)

# Bottom input area - Use Streamlit's native input with custom styling
st.markdown("""
    <div class="input-container">
        <div class="input-wrapper">
""", unsafe_allow_html=True)

# Create input area using Streamlit components
input_col, button_col = st.columns([10, 1])

with input_col:
    user_input = st.text_area(
        "", 
        placeholder="Ask Techtonic AI",
        height=50,
        key="main_input",
        label_visibility="collapsed"
    )

with button_col:
    send_clicked = st.button("Send", key="send_button", use_container_width=True)

st.markdown("""
        </div>
    </div>
""", unsafe_allow_html=True)

# Custom styling for the input components
st.markdown("""
    <style>
    .stTextArea > div > div > textarea {
        background-color: transparent !important;
        border: none !important;
        color: #e8eaed !important;
        font-size: 16px !important;
        font-family: 'Google Sans', sans-serif !important;
        resize: none !important;
        outline: none !important;
        padding: 0 !important;
        margin: 0 !important;
    }
    
    .stTextArea > div > div > textarea::placeholder {
        color: #9aa0a6 !important;
    }
    
    .stTextArea > div {
        border: none !important;
        background: transparent !important;
    }
    
    .stButton > button[data-testid="baseButton-secondary"] {
        background-color: #4285f4 !important;
        border: none !important;
        border-radius: 50% !important;
        width: 32px !important;
        height: 32px !important;
        color: white !important;
        padding: 0 !important;
        min-height: 32px !important;
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
    }
    
    .stButton > button[data-testid="baseButton-secondary"]:hover {
        background-color: #1a73e8 !important;
        transform: scale(1.05) !important;
    }
    
    /* Hide the input container styling when in chat mode */
    .stTextArea {
        margin: 0 !important;
        padding: 0 !important;
    }
    </style>
""", unsafe_allow_html=True)

# Handle form submission
if (send_clicked and user_input.strip()) or st.session_state.trigger_send:
    if user_input.strip() or st.session_state.trigger_send:
        st.session_state.show_chat = True
        st.session_state.is_loading = True
        
        # Add user message
        message_text = user_input.strip() if user_input.strip() else st.session_state.suggestion_clicked
        st.session_state.chat_history.append((message_text, ""))
        st.session_state.trigger_send = False
        st.rerun()

# Generate response if needed
if st.session_state.chat_history and st.session_state.chat_history[-1][1] == "" and not st.session_state.is_loading:
    user_msg = st.session_state.chat_history[-1][0]
    mode = MODES[st.session_state.current_mode]
    
    # Generate response
    reply = generate_response(user_msg, mode)
    
    # Update message
    st.session_state.chat_history[-1] = (user_msg, reply)
    st.session_state.is_loading = False
    st.rerun()

# Add JavaScript for Enter key handling
st.markdown("""
    <script>
    document.addEventListener('DOMContentLoaded', function() {
        const textArea = document.querySelector('textarea[data-testid="stTextArea"]');
        
        if (textArea) {
            textArea.addEventListener('keydown', function(event) {
                if (event.key === 'Enter' && !event.shiftKey) {
                    event.preventDefault();
                    const sendButton = document.querySelector('button[data-testid="baseButton-secondary"]');
                    if (sendButton && this.value.trim()) {
                        sendButton.click();
                    }
                }
            });
        }
    });
    </script>
""", unsafe_allow_html=True)

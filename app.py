import streamlit as st
import time
from model_handler import generate_response
from modes import MODES  # MODES is now a dict: {"Display": "internal"}

# Configure page
st.set_page_config(page_title="Techtonic AI", page_icon="🤖", layout="wide")

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

# Initialize session state
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

if "is_loading" not in st.session_state:
    st.session_state.is_loading = False

if "current_mode" not in st.session_state:
    st.session_state.current_mode = list(MODES.keys())[0]

if "show_chat" not in st.session_state:
    st.session_state.show_chat = len(st.session_state.chat_history) > 0

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
    
    for title, subtitle in suggestions:
        st.markdown(f"""
            <div class="suggestion-card" onclick="fillInput('{title} {subtitle}')">
                <div class="suggestion-title">{title}</div>
                <div class="suggestion-subtitle">{subtitle}</div>
            </div>
        """, unsafe_allow_html=True)
    
    st.markdown("</div></div>", unsafe_allow_html=True)
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

# Bottom input area (simplified without icons)
st.markdown(f"""
    <div class="input-container">
        <div class="input-wrapper">
            <textarea class="input-field" placeholder="Ask Techtonic AI" id="mainInput" onkeydown="handleKeyDown(event)" oninput="toggleSendButton()"></textarea>
            <button class="send-button" id="sendBtn" onclick="sendMessage()">
                <svg width="16" height="16" viewBox="0 0 16 16" fill="currentColor">
                    <path d="M2 2L14 8L2 14V9L10 8L2 7V2Z"/>
                </svg>
            </button>
        </div>
    </div>
""", unsafe_allow_html=True)

# JavaScript for interactions
st.markdown("""
    <script>
    function fillInput(text) {
        document.getElementById('mainInput').value = text;
        toggleSendButton();
    }
    
    function toggleSendButton() {
        const input = document.getElementById('mainInput');
        const sendBtn = document.getElementById('sendBtn');
        
        if (input.value.trim()) {
            sendBtn.classList.add('visible');
        } else {
            sendBtn.classList.remove('visible');
        }
    }
    
    function handleKeyDown(event) {
        if (event.key === 'Enter' && !event.shiftKey) {
            event.preventDefault();
            sendMessage();
        }
    }
    
    function sendMessage() {
        const input = document.getElementById('mainInput');
        const text = input.value.trim();
        
        if (text) {
            // Trigger Streamlit form submission
            const hiddenInput = document.querySelector('textarea[data-testid]');
            if (hiddenInput) {
                hiddenInput.value = text;
                hiddenInput.dispatchEvent(new Event('input', { bubbles: true }));
            }
            
            // Trigger button click
            const hiddenButton = document.querySelector('button[data-testid]');
            if (hiddenButton) {
                hiddenButton.click();
            }
            
            input.value = '';
            toggleSendButton();
        }
    }
    
    // Auto-resize textarea
    const textarea = document.getElementById('mainInput');
    if (textarea) {
        textarea.addEventListener('input', function() {
            this.style.height = 'auto';
            this.style.height = Math.min(this.scrollHeight, 120) + 'px';
        });
    }
    </script>
""", unsafe_allow_html=True)

# Hidden Streamlit components for backend functionality
col1, col2 = st.columns([8, 1])

with col1:
    user_input = st.text_area("", height=1, label_visibility="collapsed", key="hidden_input")

with col2:
    mode_display = st.selectbox("", list(MODES.keys()), key="hidden_mode", label_visibility="collapsed")
    submit = st.button("Send", key="hidden_submit")

# Handle submission
if submit and user_input.strip():
    st.session_state.show_chat = True
    st.session_state.is_loading = True
    
    # Add user message
    st.session_state.chat_history.append((user_input.strip(), ""))
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

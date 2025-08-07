import streamlit as st
import time
from model_handler import generate_response
from modes import MODES  # MODES is now a dict: {"Display": "internal"}

# Configure page
st.set_page_config(page_title="Techtonic AI", page_icon="🤖", layout="wide")

# Inject modern CSS with glassmorphism and animations
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    /* Global Styles */
    * {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
    }
    
    .stApp {
        background: linear-gradient(135deg, #0c0c0f 0%, #1a1a2e 50%, #16213e 100%);
        color: #e1e5e9;
    }
    
    /* Hide Streamlit elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Sidebar Styling */
    .css-1d391kg {
        background: rgba(15, 23, 42, 0.8);
        backdrop-filter: blur(20px);
        border-right: 1px solid rgba(148, 163, 184, 0.1);
    }
    
    /* Main container */
    .main-container {
        display: flex;
        flex-direction: column;
        height: 100vh;
        max-width: 800px;
        margin: 0 auto;
        padding: 0 20px;
    }
    
    /* Header */
    .header {
        text-align: center;
        padding: 20px 0;
        background: rgba(15, 23, 42, 0.6);
        backdrop-filter: blur(20px);
        border-radius: 20px;
        margin: 20px 0;
        border: 1px solid rgba(148, 163, 184, 0.1);
    }
    
    .header h1 {
        background: linear-gradient(135deg, #3b82f6, #8b5cf6, #06b6d4);
        background-clip: text;
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 2.5rem;
        font-weight: 700;
        margin: 0;
        letter-spacing: -0.02em;
    }
    
    .header .subtitle {
        color: #64748b;
        font-size: 0.875rem;
        margin-top: 8px;
        font-weight: 400;
    }
    
    /* Chat Container */
    .chat-container {
        flex: 1;
        overflow-y: auto;
        padding: 20px 0;
        margin-bottom: 120px;
    }
    
    /* Message Styles */
    .user-message, .assistant-message {
        margin: 16px 0;
        padding: 16px 20px;
        border-radius: 18px;
        max-width: 85%;
        position: relative;
        backdrop-filter: blur(10px);
        border: 1px solid rgba(148, 163, 184, 0.1);
        animation: fadeInUp 0.5s ease-out;
    }
    
    .user-message {
        background: rgba(59, 130, 246, 0.15);
        margin-left: auto;
        border-bottom-right-radius: 6px;
    }
    
    .assistant-message {
        background: rgba(15, 23, 42, 0.8);
        margin-right: auto;
        border-bottom-left-radius: 6px;
    }
    
    /* Input Container */
    .input-container {
        position: fixed;
        bottom: 20px;
        left: 50%;
        transform: translateX(-50%);
        width: 90%;
        max-width: 760px;
        z-index: 1000;
    }
    
    .input-box {
        background: rgba(15, 23, 42, 0.9);
        backdrop-filter: blur(20px);
        border: 1px solid rgba(148, 163, 184, 0.2);
        border-radius: 24px;
        padding: 16px 20px;
        display: flex;
        align-items: flex-end;
        gap: 12px;
        transition: all 0.3s ease;
        position: relative;
    }
    
    .input-box:focus-within {
        border: 2px solid;
        border-image: linear-gradient(135deg, #3b82f6, #8b5cf6) 1;
        box-shadow: 0 0 30px rgba(59, 130, 246, 0.3);
    }
    
    .input-textarea {
        flex: 1;
        background: transparent !important;
        border: none !important;
        resize: none !important;
        outline: none !important;
        color: #e1e5e9 !important;
        font-size: 16px !important;
        line-height: 1.5 !important;
        max-height: 120px;
        overflow-y: auto;
        font-family: 'Inter', sans-serif !important;
    }
    
    .input-textarea::placeholder {
        color: #64748b !important;
    }
    
    /* Mode selector and controls */
    .controls {
        display: flex;
        align-items: center;
        gap: 8px;
    }
    
    .mode-toggle {
        position: relative;
        display: inline-block;
    }
    
    .mode-btn {
        background: rgba(59, 130, 246, 0.2);
        border: 1px solid rgba(59, 130, 246, 0.3);
        border-radius: 12px;
        padding: 8px;
        cursor: pointer;
        transition: all 0.3s ease;
        display: flex;
        align-items: center;
        gap: 4px;
    }
    
    .mode-btn:hover {
        background: rgba(59, 130, 246, 0.3);
        transform: translateY(-1px);
    }
    
    .mode-dropdown {
        position: absolute;
        bottom: 100%;
        left: 0;
        background: rgba(15, 23, 42, 0.95);
        backdrop-filter: blur(20px);
        border: 1px solid rgba(148, 163, 184, 0.2);
        border-radius: 12px;
        padding: 8px;
        margin-bottom: 8px;
        min-width: 200px;
        display: none;
        z-index: 1001;
    }
    
    .mode-dropdown.show {
        display: block;
        animation: slideUp 0.3s ease-out;
    }
    
    .mode-option {
        padding: 8px 12px;
        border-radius: 8px;
        cursor: pointer;
        transition: all 0.2s ease;
        font-size: 14px;
    }
    
    .mode-option:hover {
        background: rgba(59, 130, 246, 0.2);
    }
    
    .send-btn {
        background: linear-gradient(135deg, #3b82f6, #1d4ed8) !important;
        border: none !important;
        border-radius: 12px !important;
        padding: 10px !important;
        cursor: pointer !important;
        transition: all 0.3s ease !important;
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
        min-width: 44px !important;
        height: 44px !important;
    }
    
    .send-btn:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 8px 25px rgba(59, 130, 246, 0.4) !important;
    }
    
    .send-btn:active {
        transform: translateY(0) !important;
    }
    
    /* Loading Animation */
    .loading-container {
        display: flex;
        justify-content: center;
        align-items: center;
        padding: 20px;
    }
    
    .loading-bubbles {
        display: flex;
        gap: 8px;
    }
    
    .bubble {
        width: 12px;
        height: 12px;
        background: linear-gradient(135deg, #3b82f6, #8b5cf6);
        border-radius: 50%;
        animation: bounce 1.4s infinite ease-in-out;
    }
    
    .bubble:nth-child(1) { animation-delay: -0.32s; }
    .bubble:nth-child(2) { animation-delay: -0.16s; }
    .bubble:nth-child(3) { animation-delay: 0s; }
    
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
    
    @keyframes slideUp {
        from {
            opacity: 0;
            transform: translateY(10px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    @keyframes bounce {
        0%, 80%, 100% {
            transform: scale(0);
        } 40% {
            transform: scale(1);
        }
    }
    
    /* New Chat Button */
    .new-chat-btn {
        background: rgba(59, 130, 246, 0.1) !important;
        border: 1px solid rgba(59, 130, 246, 0.3) !important;
        color: #3b82f6 !important;
        border-radius: 12px !important;
        padding: 8px 16px !important;
        font-weight: 500 !important;
        transition: all 0.3s ease !important;
    }
    
    .new-chat-btn:hover {
        background: rgba(59, 130, 246, 0.2) !important;
        transform: translateY(-1px) !important;
    }
    
    /* Responsive */
    @media (max-width: 768px) {
        .input-container {
            width: 95%;
        }
        
        .header h1 {
            font-size: 2rem;
        }
        
        .user-message, .assistant-message {
            max-width: 95%;
        }
    }
    
    /* Hide default streamlit components */
    .stTextArea > div > div > textarea {
        background-color: transparent !important;
        border: none !important;
        box-shadow: none !important;
    }
    
    .stSelectbox > div > div {
        background-color: transparent !important;
        border: none !important;
    }
    
    .stButton > button {
        background: transparent !important;
        border: none !important;
        color: inherit !important;
    }
    </style>
""", unsafe_allow_html=True)

# JavaScript for interactions
st.markdown("""
    <script>
    function toggleModeDropdown() {
        const dropdown = document.querySelector('.mode-dropdown');
        dropdown.classList.toggle('show');
    }
    
    function selectMode(mode) {
        document.querySelector('.current-mode').textContent = mode;
        document.querySelector('.mode-dropdown').classList.remove('show');
    }
    
    // Auto-resize textarea
    function autoResize(textarea) {
        textarea.style.height = 'auto';
        textarea.style.height = textarea.scrollHeight + 'px';
    }
    </script>
""", unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.markdown("""
        <div style="text-align: center; padding: 20px 0; border-bottom: 1px solid rgba(148, 163, 184, 0.1);">
            <h2 style="background: linear-gradient(135deg, #3b82f6, #8b5cf6); background-clip: text; -webkit-background-clip: text; -webkit-text-fill-color: transparent; margin: 0;">Techtonic AI</h2>
            <p style="color: #64748b; font-size: 0.75rem; margin: 4px 0 0 0;">Creative Text Engine</p>
        </div>
    """, unsafe_allow_html=True)
    
    if st.button("➕ New Chat", key="new_chat", help="Start a new conversation"):
        st.session_state.chat_history = []
        st.rerun()

# Ensure session state
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

if "is_loading" not in st.session_state:
    st.session_state.is_loading = False

if "current_mode" not in st.session_state:
    st.session_state.current_mode = list(MODES.keys())[0]

# Main header
st.markdown("""
    <div class="header">
        <h1>Techtonic AI</h1>
        <div class="subtitle">Creative Text Engine</div>
    </div>
""", unsafe_allow_html=True)

# Chat container
chat_container = st.container()

with chat_container:
    # Display loading animation if generating
    if st.session_state.is_loading:
        st.markdown("""
            <div class="loading-container">
                <div class="loading-bubbles">
                    <div class="bubble"></div>
                    <div class="bubble"></div>
                    <div class="bubble"></div>
                </div>
            </div>
        """, unsafe_allow_html=True)
        time.sleep(0.1)  # Small delay for animation
    
    # Display chat history
    for i, (user_msg, bot_reply) in enumerate(st.session_state.chat_history):
        # User message
        st.markdown(f"""
            <div class="user-message">
                {user_msg}
            </div>
        """, unsafe_allow_html=True)
        
        # Assistant message with fade-in animation
        st.markdown(f"""
            <div class="assistant-message" style="animation-delay: {i * 0.1}s;">
                {bot_reply}
            </div>
        """, unsafe_allow_html=True)

# Input area at bottom
st.markdown('<div style="height: 120px;"></div>', unsafe_allow_html=True)

# Create columns for input layout
col1, col2 = st.columns([8, 1])

with col1:
    user_input = st.text_area(
        "Message Techtonic AI...", 
        height=80, 
        label_visibility="collapsed",
        key="user_input",
        placeholder="Message Techtonic AI..."
    )

with col2:
    # Mode selector (hidden, will be replaced with custom UI)
    mode_display = st.selectbox(
        "Mode", 
        list(MODES.keys()), 
        index=list(MODES.keys()).index(st.session_state.current_mode),
        label_visibility="collapsed",
        key="mode_select"
    )
    
    # Update current mode
    if mode_display != st.session_state.current_mode:
        st.session_state.current_mode = mode_display
    
    submit = st.button("🚀", key="send_btn", help="Send message")

# Custom input container overlay
mode_options_html = ''.join([
    f'<div class="mode-option" onclick="selectMode(\'{mode}\')">{mode}</div>' 
    for mode in MODES.keys()
])

st.markdown(f"""
    <div class="input-container">
        <div class="input-box">
            <div class="controls">
                <div class="mode-toggle">
                    <div class="mode-btn" onclick="toggleModeDropdown()">
                        <span style="font-size: 18px;">⚡</span>
                        <span class="current-mode" style="font-size: 12px; color: #64748b;">{st.session_state.current_mode}</span>
                    </div>
                    <div class="mode-dropdown">
                        {mode_options_html}
                    </div>
                </div>
            </div>
        </div>
    </div>
""", unsafe_allow_html=True)

# Handle submission
if submit and user_input.strip():
    # Set loading state
    st.session_state.is_loading = True
    
    # Get the mode
    mode = MODES[st.session_state.current_mode]
    
    # Add user message immediately
    st.session_state.chat_history.append((user_input.strip(), ""))
    
    # Rerun to show loading
    st.rerun()

# Generate response if we have an incomplete message
if st.session_state.chat_history and st.session_state.chat_history[-1][1] == "":
    user_msg = st.session_state.chat_history[-1][0]
    mode = MODES[st.session_state.current_mode]
    
    # Generate response
    reply = generate_response(user_msg, mode)
    
    # Update the last message with the response
    st.session_state.chat_history[-1] = (user_msg, reply)
    
    # Clear loading state
    st.session_state.is_loading = False
    
    # Clear input and rerun
    st.session_state.user_input = ""
    st.rerun()

# Auto-scroll to bottom
st.markdown("""
    <script>
    window.scrollTo(0, document.body.scrollHeight);
    </script>
""", unsafe_allow_html=True)

import streamlit as st
from model_handler import generate_response
from modes import MODES  # MODES is a dict: {"Display": "internal"}

# Inject modern dark theme with glassmorphism and animation
st.markdown("""
    <style>
    /* Global styles */
    body, .stApp {
        background: radial-gradient(circle at top left, #1f1f2e, #13131a);
        font-family: 'Segoe UI', sans-serif;
        color: white;
    }

    /* Header styling */
    .block-container > div:nth-child(1) {
        padding-top: 1rem;
    }

    /* Textbox styling */
    textarea {
        background: rgba(255, 255, 255, 0.05) !important;
        color: white !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        border-radius: 15px !important;
        backdrop-filter: blur(10px);
        transition: all 0.3s ease-in-out;
    }

    textarea:focus {
        outline: none !important;
        border: 1.5px solid #10a37f !important;
        box-shadow: 0 0 8px 2px #10a37f99;
    }

    /* Button styling */
    button[kind="primary"] {
        background: rgba(255, 255, 255, 0.1) !important;
        border: none;
        border-radius: 50%;
        height: 3rem;
        width: 3rem;
        font-size: 1.5rem;
        backdrop-filter: blur(12px);
        transition: background 0.3s ease-in-out;
    }

    button[kind="primary"]:hover {
        background: #10a37f !important;
    }

    /* Sidebar title */
    .sidebar-content h1 {
        font-size: 1.8rem;
        margin-bottom: 0.2rem;
    }
    .sidebar-content h2 {
        font-size: 0.9rem;
        opacity: 0.6;
    }

    /* Hide default label */
    label[data-testid="stTextAreaLabel"] {
        display: none;
    }

    /* Chat fade-in animation */
    .element-container:has(.stChatMessage) {
        animation: fadeIn 0.5s ease-in-out;
    }

    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(10px); }
        to { opacity: 1; transform: translateY(0); }
    }

    /* + Icon and mode menu */
    #plus-menu {
        position: fixed;
        bottom: 100px;
        left: 20px;
        background: rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(10px);
        border-radius: 50%;
        width: 3rem;
        height: 3rem;
        font-size: 2rem;
        color: white;
        text-align: center;
        line-height: 3rem;
        cursor: pointer;
        z-index: 999;
        transition: all 0.3s ease-in-out;
    }

    #mode-list {
        position: fixed;
        bottom: 150px;
        left: 20px;
        display: none;
        flex-direction: column;
        gap: 0.3rem;
        z-index: 999;
    }

    #mode-list .mode-btn {
        background: rgba(255, 255, 255, 0.08);
        padding: 0.4rem 0.8rem;
        border-radius: 10px;
        backdrop-filter: blur(8px);
        cursor: pointer;
        transition: all 0.2s;
    }

    #mode-list .mode-btn:hover {
        background: #10a37f;
    }

    @keyframes bounce {
        0%, 100% { transform: translateY(0); }
        50% { transform: translateY(-5px); }
    }

    .loading-bubbles span {
        display: inline-block;
        width: 8px;
        height: 8px;
        margin: 2px;
        background: #10a37f;
        border-radius: 50%;
        animation: bounce 1s infinite;
    }

    .loading-bubbles span:nth-child(2) {
        animation-delay: 0.2s;
    }

    .loading-bubbles span:nth-child(3) {
        animation-delay: 0.4s;
    }
    </style>
""", unsafe_allow_html=True)

# Header
st.sidebar.markdown("""
# Techtonic AI
##### Creative Text Engine
""")

if st.sidebar.button("➕ New Chat"):
    st.session_state.chat_history = []

# Ensure chat history
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Chat Display
st.markdown("### Chat")
for user_msg, bot_reply in st.session_state.chat_history:
    st.chat_message("user").write(user_msg)
    st.chat_message("assistant").write(bot_reply)

# Floating Mode Button UI
st.markdown("""
<div id="plus-menu">+</div>
<div id="mode-list">
""" + ''.join([f'<div class="mode-btn" onclick="setMode(\"{key}\")">{key}</div>' for key in list(MODES.keys())[:4]]) + """
</div>
<script>
    const plusBtn = document.getElementById("plus-menu");
    const modeList = document.getElementById("mode-list");
    let selectedMode = "{list(MODES.keys())[0]}";

    window.setMode = function(modeName) {
        fetch("/?mode=" + modeName);
    }

    plusBtn.onclick = () => {
        modeList.style.display = modeList.style.display === "flex" ? "none" : "flex";
    }
</script>
""", unsafe_allow_html=True)

# Input area pinned at bottom
with st.container():
    col1, col2 = st.columns([10, 1])
    with col1:
        user_input = st.text_area("Enter your text...", height=80, label_visibility="collapsed")
    with col2:
        submit = st.button("➤")

# Response animation & submission
if submit and user_input.strip():
    with st.spinner("\n\n<div class='loading-bubbles'><span></span><span></span><span></span></div>\n\n"):
        reply = generate_response(user_input.strip(), MODES.get(st.query_params.get("mode", list(MODES.keys())[0]), list(MODES.values())[0]))
    st.session_state.chat_history.append((user_input.strip(), reply))
    st.experimental_set_query_params(dummy=str(reply))
    st.rerun()

import streamlit as st
from model_handler import generate_response
from modes import MODES  # {"Translate": "translate", ...}

# Inject custom CSS for layout styling
st.markdown("""
    <style>
    .block-container {
        padding-top: 1rem;
        padding-bottom: 1rem;
    }
    .chat-input-container {
        position: fixed;
        bottom: 0;
        width: 100%;
        background-color: #343541;
        padding: 1rem 1rem 0.5rem 1rem;
        border-top: 1px solid #555;
    }
    .chat-scroll-area {
        max-height: calc(100vh - 170px);
        overflow-y: auto;
        padding-bottom: 8rem;
    }
    textarea, input, select {
        background-color: #40414f !important;
        color: white !important;
        border-radius: 10px !important;
        font-size: 1rem !important;
    }
    button {
        background-color: #10a37f !important;
        color: white !important;
        border-radius: 8px !important;
    }
    button:hover {
        background-color: #0d8c6e !important;
    }
    </style>
""", unsafe_allow_html=True)

# Sidebar with options
st.sidebar.markdown("# 🧠 Creative Text Engine")
if st.sidebar.button("➕ New Chat"):
    st.session_state.chat_history = []

st.sidebar.text_input("🔍 Search chats", key="search")
st.sidebar.button("📤 Share this chat")

# Initialize chat history
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Main chat area
st.markdown("### Chat")
with st.container():
    st.markdown('<div class="chat-scroll-area">', unsafe_allow_html=True)

    for user_msg, bot_reply in st.session_state.chat_history:
        st.chat_message("user").write(user_msg)
        st.chat_message("assistant").write(bot_reply)

    st.markdown('</div>', unsafe_allow_html=True)

# Chat input area at the bottom
with st.container():
    st.markdown('<div class="chat-input-container">', unsafe_allow_html=True)
    with st.form("chat_form", clear_on_submit=True):
        user_input = st.text_area("Enter your message", height=80, label_visibility="collapsed")
        mode_display = st.selectbox("Choose mode", list(MODES.keys()))
        submitted = st.form_submit_button("🚀 Send")

    st.markdown('</div>', unsafe_allow_html=True)

# Handle submission
if submitted and user_input.strip():
    mode = MODES[mode_display]
    reply = generate_response(user_input.strip(), mode)
    st.session_state.chat_history.append((user_input.strip(), reply))
    st.experimental_rerun()

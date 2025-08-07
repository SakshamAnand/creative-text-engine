import streamlit as st
from model_handler import generate_response
from modes import MODES  # MODES is a dict like {"🌍 Translate": "translate"}

# Inject custom CSS
st.markdown("""
    <style>
    body {
        font-family: 'Segoe UI', sans-serif;
        background-color: #202123;
        color: white;
    }
    .stApp {
        background-color: #343541;
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
    .sidebar-title {
        font-size: 1.5rem;
        font-weight: bold;
        padding-bottom: 0.5rem;
    }
    </style>
""", unsafe_allow_html=True)

# --- Sidebar ---
st.sidebar.markdown('<div class="sidebar-title">🧠 Creative Text Engine</div>', unsafe_allow_html=True)

if st.sidebar.button("➕ New Chat"):
    st.session_state.chat_history = []

search_query = st.sidebar.text_input("🔍 Search chats", key="search_chats")

with st.sidebar.expander("➕ Modes", expanded=False):
    selected_display = st.radio("Choose mode", list(MODES.keys()), key="mode_radio")
    selected_mode = MODES[selected_display]

# --- Session State Setup ---
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# --- Main Chat Area ---
st.markdown("### Chat")
for user_msg, bot_reply in st.session_state.chat_history:
    if search_query.lower() in user_msg.lower() or search_query.lower() in bot_reply.lower():
        st.chat_message("user").write(user_msg)
        st.chat_message("assistant").write(bot_reply)

# --- Input Box ---
with st.container():
    col1, col2 = st.columns([6, 1])
    with col1:
        user_input = st.text_area("Enter your text...", height=80, label_visibility="collapsed")
    with col2:
        submit = st.button("🚀")

# --- Handle Submit ---
if submit and user_input.strip():
    bot_reply = generate_response(user_input.strip(), selected_mode)
    st.session_state.chat_history.append((user_input.strip(), bot_reply))
    st.experimental_set_query_params(force_refresh=str(bot_reply))
    st.rerun()

# --- Share Button ---
st.button("📤 Share this chat")

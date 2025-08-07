import streamlit as st
from model_handler import generate_response
from modes import MODES  # MODES is now a dict: {"Display": "internal"}

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
    </style>
""", unsafe_allow_html=True)

# Sidebar
st.sidebar.markdown("# 🧠 Creative Text Engine")
if st.sidebar.button("➕ New Chat"):
    st.session_state.chat_history = []

search = st.sidebar.text_input("🔍 Search chats", key="search")

# Ensure session state
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Main content
st.markdown("### Chat")
for user_msg, bot_reply in st.session_state.chat_history:
    st.chat_message("user").write(user_msg)
    st.chat_message("assistant").write(bot_reply)

# Input area
with st.container():
    col1, col2, col3 = st.columns([4, 2, 1])

    with col1:
        user_input = st.text_area("Enter your text...", height=80, label_visibility="collapsed")

    with col2:
        # Display mode names in dropdown
        mode_display = st.selectbox("Mode", list(MODES.keys()))
        mode = MODES[mode_display]  # Get internal mode value (e.g., "translate")

    with col3:
        submit = st.button("🚀 Generate")

# Handle submission
if submit and user_input.strip():
    reply = generate_response(user_input.strip(), mode)
    st.session_state.chat_history.append((user_input.strip(), reply))

    # Force rerun by clearing input using workaround
    st.experimental_set_query_params(dummy=str(reply))  # Forces rerun safely
    st.rerun()

# Share button
st.button("📤 Share this chat")

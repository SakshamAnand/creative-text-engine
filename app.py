import streamlit as st
import json
import datetime
from model_handler import generate_response
from modes import MODES  # dict like {"Chat": "chat", "Translate": "translate"}

# ------------------ Custom CSS ------------------
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

# ------------------ Session State Init ------------------
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []  # current chat
if "saved_chats" not in st.session_state:
    st.session_state.saved_chats = {}  # {chat_name: [(user, bot), ...]}

# ------------------ Sidebar ------------------
st.sidebar.markdown("# 🧠 Creative Text Engine")

# New chat
if st.sidebar.button("➕ New Chat"):
    if st.session_state.chat_history:
        name = f"Chat {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
        st.session_state.saved_chats[name] = st.session_state.chat_history
    st.session_state.chat_history = []

# Search bar
search_query = st.sidebar.text_input("🔍 Search saved chats")

# Display saved chats
st.sidebar.markdown("### 📜 Saved Chats")
filtered_chats = {name: hist for name, hist in st.session_state.saved_chats.items()
                  if search_query.lower() in name.lower()}
for chat_name in filtered_chats:
    if st.sidebar.button(chat_name):
        st.session_state.chat_history = st.session_state.saved_chats[chat_name]

# Export current chat
if st.sidebar.button("💾 Export Current Chat"):
    if st.session_state.chat_history:
        export_data = json.dumps(st.session_state.chat_history, indent=2)
        st.sidebar.download_button("Download JSON", export_data, file_name="chat_history.json")
    else:
        st.sidebar.warning("No chat to export.")

# Import chat
uploaded_chat = st.sidebar.file_uploader("📂 Import Chat (JSON)", type="json")
if uploaded_chat:
    try:
        imported_history = json.load(uploaded_chat)
        if isinstance(imported_history, list):
            st.session_state.chat_history = imported_history
            st.sidebar.success("Chat imported successfully.")
        else:
            st.sidebar.error("Invalid chat format.")
    except Exception as e:
        st.sidebar.error(f"Error loading file: {e}")

# ------------------ Main Chat Display ------------------
st.markdown("### Chat")
for user_msg, bot_reply in st.session_state.chat_history:
    st.chat_message("user").write(user_msg)
    st.chat_message("assistant").write(bot_reply)

# ------------------ Input Area ------------------
with st.container():
    col1, col2, col3 = st.columns([4, 2, 1])

    with col1:
        user_input = st.text_area("Enter your text...", height=80, label_visibility="collapsed")

    with col2:
        mode_display = st.selectbox("Mode", list(MODES.keys()))
        mode = MODES[mode_display]

    with col3:
        submit = st.button("🚀 Generate")

# ------------------ Handle Submission ------------------
if submit and user_input.strip():
    reply = generate_response(user_input.strip(), mode)
    st.session_state.chat_history.append((user_input.strip(), reply))
    st.experimental_rerun()

# ------------------ Share Current Chat ------------------
if st.button("📤 Share this chat"):
    if st.session_state.chat_history:
        st.code(json.dumps(st.session_state.chat_history, indent=2), language="json")
    else:
        st.warning("No chat to share.")

import streamlit as st
import json
from datetime import datetime
from model_handler import generate_response
from modes import MODES  # MODES is now a dict: {"Display": "internal"}

# ---------- Custom CSS ----------
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

# ---------- Ensure session state ----------
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "search_query" not in st.session_state:
    st.session_state.search_query = ""

# ---------- Sidebar ----------
st.sidebar.markdown("# 🧠 Creative Text Engine")

# New chat button
if st.sidebar.button("➕ New Chat"):
    st.session_state.chat_history = []

# Search chats
st.session_state.search_query = st.sidebar.text_input("🔍 Search chats", value=st.session_state.search_query)

# Export chats
if st.session_state.chat_history:
    export_data = "\n\n".join(
        [f"User: {u}\nBot: {b}" for u, b in st.session_state.chat_history]
    )
    st.sidebar.download_button(
        label="📥 Export Chat",
        data=export_data,
        file_name=f"chat_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
        mime="text/plain"
    )

# Clear chat button
if st.sidebar.button("🗑 Clear Chat"):
    st.session_state.chat_history = []

# ---------- Main Chat Display ----------
st.markdown("### Chat")
filtered_history = st.session_state.chat_history
if st.session_state.search_query:
    filtered_history = [
        (u, b) for u, b in st.session_state.chat_history
        if st.session_state.search_query.lower() in u.lower()
        or st.session_state.search_query.lower() in b.lower()
    ]

for user_msg, bot_reply in filtered_history:
    st.chat_message("user").write(user_msg)
    st.chat_message("assistant").write(bot_reply)

# ---------- Input area ----------
with st.container():
    col1, col2, col3 = st.columns([4, 2, 1])

    with col1:
        user_input = st.text_area("Enter your text...", height=80, label_visibility="collapsed")

    with col2:
        mode_display = st.selectbox("Mode", list(MODES.keys()))
        mode = MODES[mode_display]  # Internal mode value

    with col3:
        submit = st.button("🚀 Generate")

# ---------- Handle submission ----------
if submit and user_input.strip():
    reply = generate_response(user_input.strip(), mode)
    st.session_state.chat_history.append((user_input.strip(), reply))
    st.experimental_set_query_params(dummy=str(reply))  # Force refresh
    st.rerun()

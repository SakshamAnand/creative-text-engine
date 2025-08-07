import streamlit as st
from model_handler import generate_response
from modes import MODES

# Custom CSS injection
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

# Sidebar (left column)
st.sidebar.markdown("# 🧠 Creative Text Engine")
if st.sidebar.button("➕ New Chat"):
    st.session_state.chat_history = []

search = st.sidebar.text_input("🔍 Search chats", key="search")

# Main content area
st.markdown("### Chat")
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Display chat history
for i, (user_msg, bot_reply) in enumerate(st.session_state.chat_history):
    st.chat_message("user").write(user_msg)
    st.chat_message("assistant").write(bot_reply)

# Input section
# Input area
with st.container():
    col1, col2, col3 = st.columns([4, 2, 1])
    with col1:
        st.text_area("Enter your text...", height=80, label_visibility="collapsed", key="user_input")
    with col2:
        mode = st.selectbox("Mode", MODES, index=MODES.index("translate") if "translate" in MODES else 0)
    with col3:
        submit = st.button("🚀 Generate")

# Handle submission
if submit and st.session_state.user_input.strip():
    reply = generate_response(st.session_state.user_input.strip(), mode)

    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    st.session_state.chat_history.append((st.session_state.user_input.strip(), reply))
    st.session_state.user_input = ""  # ✅ now safe!
    st.rerun()



# Share button
st.button("📤 Share this chat")

import streamlit as st
from model_handler import generate_response
from modes import MODES

# Page configuration
st.set_page_config(layout="wide", page_title="Creative Text Engine")

# Inject custom CSS
def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

local_css("style.css")

# Sidebar
with st.sidebar:
    st.markdown("# 🧠 Creative Text Engine")
    if st.button("➕ New Chat"):
        st.session_state.chat_history = []
    st.markdown("---")
    # Search is not implemented in this version, but the input is retained
    st.text_input("🔍 Search chats", key="search")
    st.markdown("---")
    st.markdown("### Modes")
    mode_display = st.radio(
        "Select a mode:",
        list(MODES.keys()),
        label_visibility="collapsed"
    )
    mode = MODES[mode_display]  # Get internal mode value

# Main content
st.title("Welcome to the Creative Text Engine 🚀")
st.markdown("Transform your text with the power of AI. Select a mode from the sidebar, type your text, and see the magic happen!")

# Chat History
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

for user_msg, bot_reply in st.session_state.chat_history:
    st.chat_message("user").write(user_msg)
    st.chat_message("assistant").write(bot_reply)

# Input area
with st.container():
    user_input = st.text_area("Enter your text here...", key="user_input", height=150)
    submit_button = st.button("✨ Generate")

    if submit_button and user_input.strip():
        with st.spinner("🧠 Thinking..."):
            reply = generate_response(user_input.strip(), mode)
            st.session_state.chat_history.append((user_input.strip(), reply))
            # Rerun to display the new message
            st.rerun()

# Share button in the footer (as an example of placement)
st.markdown("---")
st.button("📤 Share this chat")

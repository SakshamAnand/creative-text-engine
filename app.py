import streamlit as st
from modes import MODES

st.set_page_config(page_title="Creative Text Engine", layout="wide")

# --- Sidebar ---
with st.sidebar:
    st.markdown("### 🧠 Creative Text Engine")
    if st.button("➕ New Chat"):
        st.session_state.messages = []
    st.text_input("🔍 Search chats")
    st.button("📤 Share this chat", use_container_width=True)

# --- Chat History ---
if "messages" not in st.session_state:
    st.session_state.messages = []

st.markdown("<h2 style='text-align: center;'>Chat</h2>", unsafe_allow_html=True)

# Display chat messages
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# --- Fixed Chat Input ---
custom_css = """
<style>
.input-container {
    position: fixed;
    bottom: 1.5rem;
    left: 50%;
    transform: translateX(-50%);
    width: 80%;
    background-color: #1e1f23;
    border: 1px solid #333;
    border-radius: 12px;
    padding: 1rem;
    z-index: 1000;
}
textarea {
    border-radius: 8px !important;
    resize: none;
}
</style>
"""
st.markdown(custom_css, unsafe_allow_html=True)

with st.container():
    st.markdown('<div class="input-container">', unsafe_allow_html=True)

    with st.form("chat_input_form", clear_on_submit=True):
        col1, col2 = st.columns([10, 1])
        with col1:
            prompt = st.text_area("Type a message...", key="prompt", label_visibility="collapsed", height=100)
        with col2:
            toggle = st.form_submit_button("➕", use_container_width=True)

        # Show mode select if toggled
        if toggle or "mode_select" not in st.session_state:
            st.session_state.mode_select = not st.session_state.get("mode_select", False)

        selected_mode = "Chat"  # default
        if st.session_state.get("mode_select", False):
            selected_mode = st.selectbox("Select mode", list(MODES.keys()), index=0)

        send = st.form_submit_button("🚀 Send")

        if send and prompt.strip():
            # Append user message
            st.session_state.messages.append({"role": "user", "content": f"{prompt}\n\n(MODE: {selected_mode})"})

            # Append mock assistant reply
            st.session_state.messages.append({"role": "assistant", "content": "🤖 Response will appear here..."})

            st.rerun()

    st.markdown('</div>', unsafe_allow_html=True)

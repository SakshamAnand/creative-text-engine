import streamlit as st
from modes import MODES

st.set_page_config(page_title="Creative Text Engine", layout="wide")

# --- Sidebar ---
with st.sidebar:
    st.markdown("### 🧠 Creative Text Engine")
    st.button("➕ New Chat", use_container_width=True)
    st.text_input("🔍 Search chats")
    st.button("📤 Share this chat", use_container_width=True)

# --- Main Chat Area ---
if "messages" not in st.session_state:
    st.session_state.messages = []

st.markdown("<h1 style='text-align: center;'>Chat</h1>", unsafe_allow_html=True)

# Display all chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# --- Bottom Prompt Area ---
st.markdown("---", unsafe_allow_html=True)
st.markdown("<div style='position:fixed; bottom:30px; left:25%; width:50%; background-color:#0e1117; padding:1rem; border-radius:1rem;'>", unsafe_allow_html=True)

with st.form("chat_form", clear_on_submit=True):
    col1, col2 = st.columns([10, 1])
    with col1:
        prompt = st.text_area(" ", placeholder="Type your message here...", label_visibility="collapsed", height=100)
    with col2:
        show_mode = st.toggle("➕", label_visibility="collapsed")

    if show_mode:
        mode = st.selectbox("Choose mode", list(MODES.keys()))
    else:
        mode = "Chat"  # default

    submitted = st.form_submit_button("🚀 Send")
    if submitted and prompt.strip() != "":
        # Save user message
        st.session_state.messages.append({"role": "user", "content": f"{prompt}\n\n(MODE: {mode})"})

        # Append assistant placeholder
        response = "🤖 Response will appear here (LLM logic not connected)"
        st.session_state.messages.append({"role": "assistant", "content": response})

st.markdown("</div>", unsafe_allow_html=True)

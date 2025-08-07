import streamlit as st
from model_handler import generate_response
from modes import MODES

st.set_page_config(page_title="Techtonic AI", layout="wide")

# Custom CSS for modern glassmorphic UI
st.markdown("""
    <style>
    body {
        background: #1a1a1a;
        font-family: 'Segoe UI', sans-serif;
    }
    .stApp {
        background: #1a1a1a;
    }
    .glass-box {
        background: rgba(255, 255, 255, 0.05);
        backdrop-filter: blur(15px);
        -webkit-backdrop-filter: blur(15px);
        border-radius: 20px;
        padding: 1rem;
        border: 1px solid rgba(255, 255, 255, 0.1);
        box-shadow: 0 4px 30px rgba(0, 0, 0, 0.1);
    }
    textarea, input, select {
        background-color: rgba(255, 255, 255, 0.1) !important;
        color: white !important;
        border: none !important;
        border-radius: 12px !important;
        font-size: 1rem !important;
        padding: 1rem !important;
    }
    .text-box-gradient:focus-within {
        border: 2px solid transparent;
        background-image: linear-gradient(#1a1a1a, #1a1a1a),
                          linear-gradient(to right, #00f260, #0575e6);
        background-origin: border-box;
        background-clip: padding-box, border-box;
        border-radius: 14px;
    }
    button {
        background-color: rgba(255, 255, 255, 0.1) !important;
        color: white !important;
        border-radius: 12px !important;
        padding: 0.6rem 1rem;
    }
    button:hover {
        background-color: rgba(255, 255, 255, 0.2) !important;
    }
    .send-btn {
        font-size: 1.5rem;
    }
    .fade-in {
        animation: fadeIn 1s ease-in-out;
    }
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(10px); }
        to { opacity: 1; transform: translateY(0); }
    }
    .bounce-loader {
        display: flex;
        justify-content: center;
        align-items: center;
        gap: 5px;
        height: 30px;
    }
    .bounce-loader div {
        width: 10px;
        height: 10px;
        background-color: white;
        border-radius: 50%;
        animation: bounce 0.6s infinite alternate;
    }
    .bounce-loader div:nth-child(2) {
        animation-delay: 0.2s;
    }
    .bounce-loader div:nth-child(3) {
        animation-delay: 0.4s;
    }
    @keyframes bounce {
        to { transform: translateY(-100%); }
    }
    .mode-popup {
        position: absolute;
        bottom: 60px;
        left: 10px;
        z-index: 10;
        background: rgba(255,255,255,0.1);
        backdrop-filter: blur(10px);
        border-radius: 12px;
        padding: 10px;
        display: flex;
        flex-direction: column;
    }
    </style>
""", unsafe_allow_html=True)

# Sidebar (logo area)
st.sidebar.markdown("<h1 style='color:white;'>Techtonic AI</h1><p style='color:gray;'>Creative Text Engine</p>", unsafe_allow_html=True)
if st.sidebar.button("➕ New Chat"):
    st.session_state.chat_history = []

# Ensure session state
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "loading" not in st.session_state:
    st.session_state.loading = False

# Chat display
for user_msg, bot_reply in st.session_state.chat_history:
    st.chat_message("user").markdown(user_msg)
    st.chat_message("assistant").markdown(f"<div class='fade-in'>{bot_reply}</div>", unsafe_allow_html=True)

# Input container
with st.container():
    st.markdown("""
        <div style="position: fixed; bottom: 0; left: 0; width: 100%; padding: 1rem; background: #1a1a1a; z-index: 9999;">
            <div style="display: flex; align-items: center; gap: 10px;">
                <div class="text-box-gradient" style="flex-grow: 1;">
                    <form action="" method="post">
                        <textarea name="user_input" placeholder="Type your message..." style="width:100%; height: 70px;"></textarea>
                        <input type="hidden" name="mode" value="default"/>
                    </form>
                </div>
                <div style="position: relative;">
                    <div style="position: absolute; bottom: 70px; left: 0;">
                        <div class="mode-popup">
                            <p style='margin:0; color:white;'>Modes:</p>
                            {''.join([f"<button onclick=\"document.querySelector('[name=\'mode\']').value='{MODES[m]}'\">{m}</button>" for m in MODES])}
                        </div>
                    </div>
                    <button class="send-btn" onclick="document.forms[0].submit();">➤</button>
                </div>
            </div>
        </div>
    """, unsafe_allow_html=True)

# Real logic handling
user_input = st.experimental_get_query_params().get("user_input", [""])[0]
mode = st.experimental_get_query_params().get("mode", [list(MODES.values())[0]])[0]

if user_input.strip():
    st.session_state.loading = True
    with st.spinner("\n<div class='bounce-loader'><div></div><div></div><div></div></div>\n"):
        reply = generate_response(user_input.strip(), mode)
    st.session_state.chat_history.append((user_input.strip(), reply))
    st.session_state.loading = False
    st.experimental_set_query_params(user_input="", mode=mode)
    st.rerun()

# Loading animation
if st.session_state.loading:
    st.markdown("<div class='bounce-loader'><div></div><div></div><div></div></div>", unsafe_allow_html=True)

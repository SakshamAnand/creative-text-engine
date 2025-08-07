import streamlit as st
import time
from model_handler import generate_response
from modes import MODES

# Page configuration
st.set_page_config(layout="wide", page_title="Techtonic AI")

# --- Asset Loading ---
def load_asset(file_name):
    with open(file_name, "r") as f:
        return f.read()

# Inject custom CSS
st.markdown(f'<style>{load_asset("style.css")}</style>', unsafe_allow_html=True)

# --- UI Rendering ---

# Header
st.markdown("""
    <div class="header">
        <h1>Techtonic AI</h1>
        <p>creative text engine</p>
    </div>
""", unsafe_allow_html=True)

# Initialize chat history
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "loading" not in st.session_state:
    st.session_state.loading = False
if "mode" not in st.session_state:
    st.session_state.mode = "Chat" # Default mode

# Display chat history
for message in st.session_state.chat_history:
    with st.chat_message(message["role"]):
        st.markdown(f'<div class="chat-message-content">{message["content"]}</div>', unsafe_allow_html=True)

# --- Input Form ---
# This form is a bit of a hack to process input, the actual UI is below
with st.form(key='chat_form'):
    user_input = st.text_input("user_input", label_visibility="collapsed", key="user_input_actual")
    submitted = st.form_submit_button(label='Submit')

    if submitted and user_input:
        # Append user message
        st.session_state.chat_history.append({"role": "user", "content": user_input})
        st.session_state.loading = True
        st.rerun()

# --- Loading and Response ---
if st.session_state.loading:
    # Display loading animation
    st.markdown(load_asset('loading_animation.html'), unsafe_allow_html=True)

    # Generate response
    mode_internal = MODES.get(st.session_state.mode, "chat")
    response = generate_response(st.session_state.chat_history[-1]["content"], mode_internal)

    # Append bot message
    st.session_state.chat_history.append({"role": "assistant", "content": response})
    st.session_state.loading = False
    st.rerun()

# --- Custom Input Bar at the bottom ---
st.markdown("""
<div class="input-bar-container">
    <div class="input-bar">
        <div class="mode-selector">
            <div class="plus-icon">+</div>
            <div class="modes">
                <div class="mode-item">Chat</div>
                <div class="mode-item">Translate</div>
                <div class="mode-item">Poemify</div>
                <div class="mode-item">Songify</div>
                <div class="mode-item">Shakespearise</div>
                <div class="mode-item">Casualify</div>
                <div class="mode-item">Formalify</div>
                <div class="mode-item">Rephrase</div>
            </div>
        </div>
        <textarea id="user-input" placeholder="Message Techtonic AI..." oninput="this.parentNode.dataset.value = this.value"></textarea>
        <div id="send-button">
            <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="22" y1="2" x2="11" y2="13"></line><polygon points="22 2 15 22 11 13 2 9 22 2"></polygon></svg>
        </div>
    </div>
</div>

<script>
// This script links the custom textarea to the hidden Streamlit input and handles submission
const textarea = document.getElementById('user-input');
const sendButton = document.getElementById('send-button');
const streamlitInput = window.parent.document.querySelector('input[aria-label="user_input"]');
const streamlitSubmitButton = window.parent.document.querySelector('button[kind="form_submit"]');
const modeItems = document.querySelectorAll('.mode-item');

textarea.addEventListener('input', (e) => {
    streamlitInput.value = e.target.value;
    // This is a necessary hack to make Streamlit recognize the input change
    const event = new Event('input', { bubbles: true });
    streamlitInput.dispatchEvent(event);
});

sendButton.addEventListener('click', () => {
    streamlitSubmitButton.click();
});

textarea.addEventListener('keydown', (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
        e.preventDefault();
        streamlitSubmitButton.click();
    }
});

modeItems.forEach(item => {
    item.addEventListener('click', () => {
        // You'll need to handle setting the mode in session state. This is a bit tricky.
        // For now, it will just visually select it. A more robust solution might need components.
        console.log("Mode selected:", item.textContent);
        alert("Mode selected: " + item.textContent + ". This is a visual demo. The actual mode is set in the sidebar for now.");
    });
});
</script>
""", unsafe_allow_html=True)

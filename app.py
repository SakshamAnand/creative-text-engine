import streamlit as st

# Set up the Streamlit page
st.set_page_config(page_title="Creative Text Engine", page_icon="🧠", layout="centered")

# Custom CSS for styling
st.markdown("""
    <style>
        .chatbox {
            background-color: #1e1e1e;
            padding: 1.5rem;
            border-radius: 1rem;
            color: white;
            font-family: 'Segoe UI', sans-serif;
            margin-top: 1rem;
        }
        .mode-button {
            margin: 0.25rem;
        }
        textarea {
            font-size: 1rem !important;
        }
    </style>
""", unsafe_allow_html=True)

# Title and Caption
st.title("🧠 Creative Text Engine")
st.caption("A ChatGPT-style GenAI translator and transformer")

# Text Input Area
user_input = st.text_area("Enter your text", height=200)

# Mode Buttons
st.markdown("### Select Mode")

col1, col2, col3 = st.columns(3)

# Use Streamlit buttons to capture mode selection
selected_mode = None
with col1:
    if st.button("🌍 Translate", use_container_width=True):
        selected_mode = "translate"
    if st.button("🪶 Poemify", use_container_width=True):
        selected_mode = "poemify"
with col2:
    if st.button("🎵 Songify", use_container_width=True):
        selected_mode = "songify"
    if st.button("🔁 Rephrase", use_container_width=True):
        selected_mode = "rephrase"
with col3:
    if st.button("🎭 Shakespeare", use_container_width=True):
        selected_mode = "shakespeare"
    if st.button("✍️ Formal/Casual", use_container_width=True):
        selected_mode = "tone_shift"

# Generate and display output
if user_input and selected_mode:
    with st.spinner(f"Generating output in {selected_mode} mode..."):
        # Placeholder output logic (replace this with actual LLM response)
        mock_response = f"[{selected_mode.upper()} MODE OUTPUT]\n\nThis is a simulated response for: \n\n\"{user_input}\""
        
        # Output
        st.markdown("#### Output")
        st.markdown(f"<div class='chatbox'>{mock_response}</div>", unsafe_allow_html=True)

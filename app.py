import gradio as gr
from model_handler import generate_response
from modes import MODES

with gr.Blocks(css="style.css", theme=gr.themes.Base()) as demo:
    with gr.Row():
        with gr.Column(scale=0.2):
            gr.Markdown("# 🧠 Creative Text Engine")
            new_chat = gr.Button("➕ New Chat")
            chat_search = gr.Textbox(placeholder="🔍 Search chats", label="Search")
        with gr.Column(scale=0.8):
            chatbot = gr.Chatbot(label="Chat", show_label=False)
            with gr.Row():
                user_input = gr.Textbox(placeholder="Enter your text...", lines=2, scale=4)
                mode_dropdown = gr.Dropdown(choices=MODES, value="translate", label="Mode", scale=2)
                submit_btn = gr.Button("🚀 Generate", scale=1)
            share_btn = gr.Button("📤 Share this chat")

    def handle_generate(message, mode, history):
        if not message:
            return history
        reply = generate_response(message, mode)
        history.append((message, reply))
        return history

    submit_btn.click(
        handle_generate,
        inputs=[user_input, mode_dropdown, chatbot],
        outputs=[chatbot]
    )

    new_chat.click(lambda: [], None, chatbot)

demo.launch()

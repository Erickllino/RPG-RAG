import gradio as gr
from agent.src.llm.client import infer_model

from agent.src.tools.session_assistant.assistant import chat




def create_tab():
    with gr.Tab("Session Assistant"):
        gr.Markdown("## Session Assistant\n> Ask anything during your session. RAG lore context will be injected once the vector store is built.")
        chatbot = gr.Chatbot(height=450)
        with gr.Row():
            msg = gr.Textbox(placeholder="Ask something...", show_label=False, scale=5)
            send_btn = gr.Button("Send", variant="primary", scale=1)
        clear_btn = gr.Button("Clear", variant="secondary")

        send_btn.click(fn=chat, inputs=[msg, chatbot], outputs=[msg, chatbot])
        msg.submit(fn=chat, inputs=[msg, chatbot], outputs=[msg, chatbot])
        clear_btn.click(fn=lambda: ([], ""), outputs=[chatbot, msg])

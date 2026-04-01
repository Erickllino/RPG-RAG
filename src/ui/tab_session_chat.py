import gradio as gr
from src.llm.client import infer_model

SYSTEM_PROMPT = (
    "You are a helpful RPG session assistant for the Ekalia campaign. "
    "Answer questions about lore, rules, NPCs, and help the game master during live sessions. "
    "Be concise and useful at the table."
)


def chat(message, history):
    if not message.strip():
        return "", history

    messages = [{"role": "system", "content": SYSTEM_PROMPT}]
    for m in history:
        messages.append({"role": m["role"], "content": m["content"]})

    content, _ = infer_model(message, messages=messages)
    history.append({"role": "user", "content": message})
    history.append({"role": "assistant", "content": content})
    return "", history


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

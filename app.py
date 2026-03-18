# ponta de entrada do gradio

from src.llm.client import infer_model
import gradio as gr

def main_menu():
    # Aqui escolhe entre os botoes de
    # 1 - Prepare
    # 2 - Playing

    # Em prepare:
    # Session audio
    # Lore writer

    # Em playing:
    # Session Assistent
    # NPC_Gen
    # Quest_Gen
    
    
    return



def chat(user_input, history):
    print(history)
    messages = []
    if history:
        for m in history:
            messages.append({"role": m["role"], "content": m["content"]})
    content, _ = infer_model(user_input, messages=messages)
    return content




if __name__ == "__main__":

    
    demo = gr.ChatInterface(fn=chat)

    demo.launch()

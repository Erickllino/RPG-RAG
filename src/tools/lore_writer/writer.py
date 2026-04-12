from src.llm.client import infer_model

import vector_store.retriver 

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
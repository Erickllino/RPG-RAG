try:
    from dotenv import load_dotenv
    load_dotenv(override=True)
except ImportError:
    pass

import os
from groq import Groq

# Debug: print to confirm key is loaded


def infer_model(msg, messages = None):
    #api_key = os.environ.get('GROQ_API_KEY')
    from dotenv import load_dotenv
    load_dotenv(override=True)
    client = Groq()
    
    if messages is None:
        messages = [{"role":"system", "content": "You are a helpful RPG session assistant for the Ekalia campaign. Answer questions about lore, rules, NPCs, and help the game master during live sessions. Be concise and useful at the table."}]
    

    messages.append({"role":"user", "content": msg})

        
    chat_completion = client.chat.completions.create(
        messages=messages,
        model="groq/compound",
    )

    return chat_completion.choices[0].message.content, messages





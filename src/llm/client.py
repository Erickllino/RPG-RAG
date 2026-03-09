try:
    from dotenv import load_dotenv
    load_dotenv(override=True)
except ImportError:
    pass

import os
from groq import Groq

# Debug: print to confirm key is loaded
api_key = os.environ.get('GROQ_API_KEY')

def infer_model(msg, messages = []):
    client = Groq(api_key=api_key)
    

    messages.append({"role":"user", "content": msg})

        
    chat_completion = client.chat.completions.create(
        messages=messages,
        model="groq/compound",
    )

    return chat_completion.choices[0].message.content, messages





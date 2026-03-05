from dotenv import load_dotenv
from pathlib import Path
load_dotenv(override=True)

import os
from groq import Groq

# Debug: print to confirm key is loaded
api_key = os.environ.get('GROQ_API_KEY')

def infer_model(msg, massages = []):
    client = Groq(api_key=api_key)
    

    massages.append({"role":"user", "content": msg})

        
    chat_completion = client.chat.completions.create(
        messages=massages,
        model="groq/compound",
    )

    return chat_completion, messages 

msg = ""
messages = []
while(True):
    msg = input("\nescreva: \n")
    if msg == "quit":
        break
    out, messages = infer_model(msg, messages)
    print(out.choices[0].message.content)





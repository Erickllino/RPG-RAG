

SYSTEM_PROMPT = (
    "You are a helpful RPG session assistant for the Ekalia campaign. "
    "Answer questions about lore, rules, NPCs, and help the game master during live sessions. "
    "Be concise and useful at the table."
)


from langchain.tools import tool

import os

@tool
def get_data(query: str) -> dict:
    """Busca informações de lore do RPG a partir de uma query em linguagem natural.
    
    Use esta tool quando o usuário perguntar sobre personagens, locais,
    eventos ou qualquer elemento narrativo do mundo do jogo.
    """
    from pathlib import Path
    PATH = Path(__file__).resolve().parents[2] 
    DATA_DIR = PATH / "Data" / "Ekalia"   
    data = {
        "File Name": [],
        "Context": [],
        "Content": [],
    }

    for file_path in DATA_DIR.rglob("*.md"):
        content = file_path.read_text(encoding="utf-8")

        data["File Name"].append(file_path.name)
        data["Content"].append(content)

        # Context = relative path inside Ekalia
        context = file_path.parent.relative_to(DATA_DIR)
        data["Context"].append(str(context))

        print(f"Read file: {context}/{file_path.name} ({len(content)})")

    return data






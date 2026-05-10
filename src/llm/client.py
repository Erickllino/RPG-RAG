try:
    from dotenv import load_dotenv
    load_dotenv(override=True)
except ImportError:
    pass


from dataclasses import dataclass
from enum import StrEnum
                                                                                                                                                                                    
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage
from langchain_groq import ChatGroq


class Role(StrEnum):
    """
    Papel funcional do LLM. Cada papel mapeia pra um modelo + temperatura
    no _MODEL_CONFIG. Tools pedem por papel, não por modelo.
    """
    CREATIVE = "creative"   # missões, lore — gosta de variedade
    FAST = "fast"           # session_assistant ao vivo, summarizer — baixa latência
    # PRECISE = "precise"   # se um dia precisar (tool calling estruturado)


@dataclass(frozen=True)                                                                                                                                                               
class ModelSpec:       
    model: str  
    temperature: float                                                                                                                                                                
                    
_MODEL_CONFIG: dict[Role, ModelSpec] = {                                                                                                                                              
    Role.CREATIVE: ModelSpec("llama-3.3-70b-versatile", 0.8),
    Role.FAST:     ModelSpec("groq/compound",    0.3),
}     


def get_llm(role: Role = Role.FAST) -> ChatGroq:                                                                                                                                                  
                                                                                                               
    spec = _MODEL_CONFIG[role]   # 1. lookup do spec                                                                                                                                  
                                                                                                                                                                                    
    return ChatGroq(             # 2. construir o ChatGroq                                                                                                                            
        model=spec.model,               #    do spec                                                                                                                                         
        temperature=spec.temperature,         #    do spec                                                                                                                                         
        max_retries=2)
           #    constante — discutimos aba)         




# ── Compat shim ────────────────────────────────────────────────
# DEPRECATED: mantém o contrato antigo (dict OpenAI in/out) pra que
# tools/UI legadas continuem funcionando enquanto migram pra LCEL.
# Remover assim que todas as tools usarem chains de prompts.py.

_ROLE_TO_MESSAGE = {
    "system": SystemMessage,
    "user": HumanMessage,
    "assistant": AIMessage,
}


def infer_model(
    msg: str,
    messages: list[dict] | None = None,
) -> tuple[str, list[dict]]:
    """Shim de compatibilidade com o infer_model antigo (Groq SDK puro)."""
    if messages is None:
        messages = [{
            "role": "system",
            "content": (
                "You are a helpful RPG session assistant for the Ekalia campaign. "
                "Answer questions about lore, rules, NPCs, and help the game master "
                "during live sessions. Be concise and useful at the table."
            ),
        }]

    messages.append({"role": "user", "content": msg})

    lc_messages = [_ROLE_TO_MESSAGE[m["role"]](content=m["content"]) for m in messages]
    response = get_llm(Role.FAST).invoke(lc_messages)

    messages.append({"role": "assistant", "content": response.content})
    return response.content, messages


if __name__ == "__main__":
    # Smoke test: confirma que ChatGroq instancia e responde.
    llm = get_llm(Role.CREATIVE)
    response = llm.invoke("Diga 'oi' em uma palavra. Depois me diga uma palavra aleatória que não seja 'oi'.")
    print(response.content)
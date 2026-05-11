try:
    from dotenv import load_dotenv
    load_dotenv(override=True)
except ImportError:
    pass


import os
from dataclasses import dataclass
from enum import StrEnum

from langchain_core.language_models import BaseChatModel
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage
from langchain_groq import ChatGroq
from langchain_openai import ChatOpenAI


class Role(StrEnum):
    """
    Papel funcional do LLM. Cada papel mapeia pra um modelo + temperatura
    no _MODEL_CONFIG. Tools pedem por papel, não por modelo.
    """
    CREATIVE = "creative"   # missões, lore — gosta de variedade
    FAST = "fast"           # session_assistant ao vivo, summarizer — baixa latência
    LOCAL = "local"         # vLLM local — testes e (futuramente) modelos fine-tuned


@dataclass(frozen=True)
class ModelSpec:
    model: str
    temperature: float


_MODEL_CONFIG: dict[Role, ModelSpec] = {
    Role.CREATIVE: ModelSpec("llama-3.3-70b-versatile", 0.8),
    Role.FAST:     ModelSpec("groq/compound",           0.3),
    Role.LOCAL:    ModelSpec(
        os.getenv("VLLM_MODEL", "Qwen/Qwen2.5-7B-Instruct-AWQ"),
        0.3,
    ),
}


def get_llm(role: Role = Role.FAST) -> BaseChatModel:
    spec = _MODEL_CONFIG[role]

    if role is Role.LOCAL:
        # vLLM expõe API OpenAI-compatible — basta apontar ChatOpenAI pro endpoint local.
        return ChatOpenAI(
            model=spec.model,
            temperature=spec.temperature,
            base_url=os.getenv("VLLM_BASE_URL", "http://localhost:8000/v1"),
            api_key=os.getenv("VLLM_API_KEY", "EMPTY"),
            max_retries=2,
        )

    return ChatGroq(
        model=spec.model,
        temperature=spec.temperature,
        max_retries=2,
    )


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
    local: bool = False,
) -> tuple[str, list[dict]]:
    """Shim de compatibilidade com o infer_model antigo (Groq SDK puro)."""

    role = Role.LOCAL
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
    response = get_llm(role).invoke(lc_messages)

    messages.append({"role": "assistant", "content": response.content})
    return response.content, messages


if __name__ == "__main__":
    import sys

    role = Role.LOCAL if "--local" in sys.argv else Role.CREATIVE
    print(f"Smoke test com role={role.value}")
    llm = get_llm(role)
    spec = _MODEL_CONFIG[role]
    messages = [
        SystemMessage(content="You are a helpful assistant for testing LLM responses."),
    ]
    while True:

        user_input = input("\nVocê: ")

        if user_input.lower() in ["sair", "exit", "quit"]:
            break

        messages.append(HumanMessage(content=user_input))   
        
        response = llm.invoke(messages)
        print(f"\n{spec.model}: {response.content}")


        messages.append(AIMessage(content=response.content))

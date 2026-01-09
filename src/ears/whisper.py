
LLM_MODEL = "deepseek-r1:latest"  # ou "llama3"
# da pra trocar pelo modelo local usando vllm

def transcribe_audio_to_text(audio_path: str) -> str:
    """
    Transcreve um arquivo de áudio para texto usando Whisper.

    Args:
        audio_path: O caminho para o arquivo de áudio.

    Returns:
        A transcrição do áudio como uma string.
    """
    import whisper

    model = whisper.load_model("large")
    result = model.transcribe(audio_path)
    return result["text"]

def summarize_session_text(session_text: str) -> str:
    """
    Resume o texto da sessão usando um modelo LLM.

    Args:
        session_text: O texto completo da sessão.

    Returns:
        Um resumo do texto da sessão.
    """
    from langchain_ollama import OllamaLLM

    llm = OllamaLLM(
        model=LLM_MODEL,  # ou "llama3"
        temperature=1.0,  # Aumenta a criatividade e reduz filtros
        top_p=0.95,  # Aumenta a diversidade de respostas
        top_k=40,  # Permite mais tokens candidatos
        num_ctx=4096  # Contexto maior
    )
    prompt = f"Resuma oque aconteceu na seguinte sessão de RPG:\n\n{session_text}\n\nResumo:"
    summary = llm.invoke(prompt)
    return summary
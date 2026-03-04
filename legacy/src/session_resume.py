import whisper
import openai
from utils.api_key import PYANNOTE_API_KEY


LLM_MODEL = "deepseek-r1:latest"  # ou "llama3"
# da pra trocar pelo modelo local usando vllm

def assign_speaker(segment, diarization):
    for turn, _, speaker in diarization.itertracks(yield_label=True):
        if turn.start <= segment["start"] <= turn.end:
            return speaker
    return "Unknown"


def transcribe_audio_to_text(audio_path: str) -> str:
    """
    Transcreve um arquivo de áudio para texto usando Whisper.

    Args:
        audio_path: O caminho para o arquivo de áudio.

    Returns:
        A transcrição do áudio como uma string.
    """
    

    model = whisper.load_model("large", device="cuda")
    result = model.transcribe(audio_path,verbose=True)

    segments = result["segments"]

    from pyannote.audio import Pipeline

    pipeline = Pipeline.from_pretrained(
    "pyannote/speaker-diarization",
    use_auth_token=PYANNOTE_API_KEY
    )

    diarization = pipeline(audio_path)


    for seg in segments:
        speaker = assign_speaker(seg, diarization)
        print(f"{speaker}: {seg['text']}")

    print(result)
    return segments

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



transcribe_audio_to_text("Data/Audios/c4e1.mp4")
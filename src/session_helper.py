import os
import json


LLM_MODEL = "deepseek-r1:latest"  # ou "llama3"
OUTPUT_IMAGE_DIR = "output_images"


# Pega os dados das campanhas: Jogadores, Numero de sessoes, Logs
def get_all_campaings():
    # Placeholder: Retorna uma lista de campanhas
    with open(os.path.join("Data", "Campaings", "campaings.json"), "r") as file:
        return json.load(file)
    return 

def add_or_remove_player_to_campaing(campaing_id, player_data):
    # Placeholder: Adiciona um jogador a uma campanha específica
    return

def log_session(campaing_id, session_number, session_data):
    # Placeholder: Loga os dados de uma sessão para uma campanha específica
    return



#Pega o audio da sessão e transforma em texto via whisper
#Envia o texto para um LLM que entende que é uma sessão de RPG e resume
#Adiciona o resumo ao log da campanha

def transcribe_audio_to_text(audio_path: str) -> str:
    """
    Transcreve um arquivo de áudio para texto usando Whisper.

    Args:
        audio_path: O caminho para o arquivo de áudio.

    Returns:
        A transcrição do áudio como uma string.
    """
    import whisper

    model = whisper.load_model("base")
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

    llm = OllamaLLM(model=LLM_MODEL)  # ou "llama3"
    prompt = f"Resuma a seguinte sessão de RPG:\n\n{session_text}\n\nResumo:"
    summary = llm.invoke(prompt)
    return summary


if __name__ == "__main__":
    
    # Adicionar Menu principal interativo com TKinter
    # - Listar campanhas
    # - Adicionar/Remover jogadores da campanha
    # - Selecionar campanha -> Logar sessão
    # 
    # - Ver resumo da campanha

    campaings = get_all_campaings()

    for campaing in campaings:
        print(f"ID: {campaing['id']}, Nome: {campaing['name']}")

    campaing_id = input("\nDigite o ID da campanha: ")

    for campaing in campaings:
        if campaing_id == campaing_id:
            print(f"Campanha encontrada: {campaing['name']}")
            print("Jogadores:")
            for player in campaing['players']:
                print(f"- {player['Nome']} ({player['Raça']} {player['Classe']})")
            break
            
        else:
            print("Campanha não encontrada.")

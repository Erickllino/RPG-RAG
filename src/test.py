import os
import json
import tkinter as tk
from tkinter import messagebox, filedialog, ttk
from langchain_ollama import OllamaLLM


LLM_MODEL = "deepseek-r1:latest"
DATA_DIR = os.path.join("Data", "Campaings")
CAMPAINGS_FILE = os.path.join(DATA_DIR, "campaings.json")


# --- Funções auxiliares ---

def get_all_campaings():
    if not os.path.exists(CAMPAINGS_FILE):
        messagebox.showerror("Erro", f"Arquivo não encontrado: {CAMPAINGS_FILE}")
        return []
    with open(CAMPAINGS_FILE, "r", encoding="utf-8") as file:
        return json.load(file)


def transcribe_audio_to_text(audio_path: str) -> str:
    import whisper
    model = whisper.load_model("base")
    result = model.transcribe(audio_path)
    return result["text"]


def summarize_session_text(session_text: str) -> str:
    llm = OllamaLLM(
        model=LLM_MODEL,
        temperature=1.0,  # Aumenta a criatividade e reduz filtros
        top_p=0.95,  # Aumenta a diversidade de respostas
        top_k=40,  # Permite mais tokens candidatos
        num_ctx=4096  # Contexto maior
    )
    prompt = f"Resuma a seguinte sessão de RPG:\n\n{session_text}\n\nResumo:"
    summary = llm.invoke(prompt)
    return summary


# --- Interface Tkinter ---

class RPGSessionApp:
    def __init__(self, root):
        self.root = root
        self.root.title("RPG Session Helper")
        self.root.geometry("600x400")
        self.root.resizable(False, False)

        self.campaigns = get_all_campaings()
        self.selected_campaign = None

        self.create_widgets()

    def create_widgets(self):
        title = tk.Label(self.root, text="Campanhas Ativas", font=("Arial", 16, "bold"))
        title.pack(pady=10)

        # Lista de campanhas
        self.campaign_list = tk.Listbox(self.root, height=8, width=50)
        self.campaign_list.pack(pady=10)
        for c in self.campaigns:
            self.campaign_list.insert(tk.END, f"{c['id']} - {c['name']}")

        select_btn = tk.Button(self.root, text="Selecionar Campanha", command=self.select_campaign)
        select_btn.pack(pady=5)

        self.players_label = tk.Label(self.root, text="", font=("Arial", 12))
        self.players_label.pack(pady=10)

        self.transcribe_btn = tk.Button(self.root, text="Transcrever e Resumir Sessão", command=self.transcribe_and_summarize)
        self.transcribe_btn.pack(pady=10)
        self.transcribe_btn.config(state=tk.DISABLED)

    def select_campaign(self):
        selection = self.campaign_list.curselection()
        if not selection:
            messagebox.showwarning("Aviso", "Selecione uma campanha primeiro.")
            return

        index = selection[0]
        self.selected_campaign = self.campaigns[index]
        players_text = "Jogadores:\n" + "\n".join(
            [f"- {p['Nome']} ({p['Raça']} {p['Classe']})" for p in self.selected_campaign.get("players", [])]
        )
        self.players_label.config(text=players_text)
        self.transcribe_btn.config(state=tk.NORMAL)

    def transcribe_and_summarize(self):
        if not self.selected_campaign:
            messagebox.showwarning("Aviso", "Selecione uma campanha primeiro.")
            return

        audio_path = filedialog.askopenfilename(
            title="Selecione o arquivo de áudio da sessão",
            filetypes=[("Arquivos de áudio", "*.mp3 *.wav *.m4a *.flac")]
        )

        if not audio_path:
            return

        messagebox.showinfo("Processando", "Transcrevendo áudio... isso pode demorar alguns minutos.")
        text = transcribe_audio_to_text(audio_path)
        summary = summarize_session_text(text)

        # check which session to save
        output_path = os.path.join(DATA_DIR, f"{self.selected_campaign['id']}/s{self.selected_campaign['Sessoes']}.txt")
        self.selected_campaign['Sessoes'] += 1
        with open(CAMPAINGS_FILE, "w", encoding="utf-8") as f:
            json.dump(self.campaigns, f, indent=4, ensure_ascii=False)
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(summary)

        messagebox.showinfo("Resumo Gerado", f"Resumo salvo em:\n{output_path}")


if __name__ == "__main__":
    root = tk.Tk()
    app = RPGSessionApp(root)
    root.mainloop()

import os
import json
import ears.whisper as whisper

"""
# TODO:
    1. Trocar Tkinter por pyside6

"""


import tkinter as tk
from tkinter import filedialog, messagebox


OUTPUT_IMAGE_DIR = "output_images"


class sessionHelper():
    def __init__(self, root ):
        
        self.root = root
        
        self.root.geometry("600x400")
        self.root.title("RPG Session Helper")

        self.campaings = self.get_all_campaings()
        self.main_menu()


    # Pega os dados das campanhas: Jogadores, Numero de sessoes, Logs
    def get_all_campaings(self):
        # Placeholder: Retorna uma lista de campanhas
        with open(os.path.join("Data", "Campaings", "campaings.json"), "r") as file:
            return json.load(file)
        return 

    def add_or_remove_player_to_campaing(self, campaing_id, player_data):
        # Placeholder: Adiciona um jogador a uma campanha específica
        return

    def main_menu(self):

        b1 = tk.Button(self.root, text = "Gerar Algo", command=self.GENERATE_MENU)
        b1.pack(pady=10)

        b2 = tk.Button(self.root, text="Gerenciar Campanhas", command=self.SELECT_CAMPAING_MENU)
        b2.pack(pady=10)


    
    
    def GENERATE_MENU(self):
        pass
    # Menu principal
    def SELECT_CAMPAING_MENU(self):

        # Clear the screen
        for widget in self.root.winfo_children():
            widget.destroy()
        
        title = tk.Label(self.root, text="Campanhas Ativas", font=("Arial", 16, "bold"))
        title.pack(pady=10)

        # Lista de campanhas
        self.campaign_list = tk.Listbox(self.root, height=8, width=50)
        self.campaign_list.pack(pady=10)
        for c in self.campaings:
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
        self.selected_campaign = self.campaings[index]
        players_text = "Jogadores:\n" + "\n".join(
            [f"- {p['Nome']} ({p['Raça']} {p['Classe']})" for p in self.selected_campaign.get("players", [])]
        )
        self.players_label.config(text=players_text)
        self.transcribe_btn.config(state=tk.NORMAL)

    def log_session(self, campaing_id, session_number, session_data):
        # Placeholder: Loga os dados de uma sessão para uma campanha específica
        return

    def transcribe_and_summarize(self):
        

        audio_path = filedialog.askopenfilename(title="Selecione o arquivo de áudio da sessão")
        if not audio_path:
            return

        try:
            session_text = whisper.transcribe_audio_to_text(audio_path)
            summary = whisper.summarize_session_text(session_text)
            messagebox.showinfo("Resumo da Sessão", summary)
        except Exception as e:
            messagebox.showerror("Erro", f"Ocorreu um erro: {str(e)}")



if __name__ == "__main__":
    import tkinter as tk
    from tkinter import simpledialog

    # Adicionar Menu principal interativo com TKinter
    # - Listar campanhas
    # - Adicionar/Remover jogadores da campanha
    # - Selecionar campanha -> Logar sessão
    # 
    # - Ver resumo da campanha

    root = tk.Tk()
    sh = sessionHelper(root)
    root.mainloop()
    # Listar campanhas disponíveis
    for campaing in sh.campaings:
        print(f"ID: {campaing['id']}, Nome: {campaing['name']}")
    # Selecionar campanha



# RPG-RAG

Um kit pessoal para organizar **lore/campanhas de RPG** e usar **LLMs locais** pra ajudar durante e depois das sessões.

O repositório hoje tem 3 “pilares” principais:

1. **Session Helper (Tkinter)**: seleciona uma campanha, transcreve um áudio e gera um resumo via Ollama.
2. **UI protótipo (PyQt6)**: um menu básico para futuramente unir geração + pós-sessão.
3. **PDF reader (PyMuPDF)**: extrai texto de PDFs e detecta imagens (com placeholder para descrever as imagens).

> Status: o projeto está em desenvolvimento e algumas partes ainda são rascunhos (ex.: `src/brain.py`, `src/get_data.py`, geradores em `src/gen/`).

## Funcionalidades

- **Campanhas**: carrega campanhas em `Data/Campaings/campaings.json`.
- **Transcrição**: usa Whisper para transcrever arquivo de áudio (ex.: MP3).
- **Resumo**: usa um LLM via **Ollama** pra resumir a sessão.
- **Extração de PDF**: pega texto e imagens e salva imagens extraídas.

## Estrutura do projeto

- `Data/`
	- `Campaings/`: campanhas e sessões
	- `Ekalia/`: lore/mundo em `.txt` (obsidian-friendly)
	- `Audios/`: exemplos de áudio
- `src/`
	- `main.py`: app Tkinter (Session Helper)
	- `main2.py`: protótipo PyQt6
	- `ears/whisper.py`: transcrição e resumo
	- `pdf_reader/pdf_agent.py`: extrator de PDF (texto + imagens)
	- `brain.py`: experimentos com agentes/LLM (atenção: contém prompts inadequados e não representa o objetivo final)
	- `get_data.py`: experimento para ler dados e jogar em dataframe (precisa de ajustes)
- `models/`: modelos locais (ex.: qwen)

## Pré-requisitos

- Python 3.10+ (recomendado)
- (Opcional) GPU/CUDA para Whisper acelerar — funciona em CPU também.
- **Ollama instalado e rodando** (para o resumo): https://ollama.com

## Instalação

Crie um ambiente virtual e instale dependências:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Como rodar

### 1) Session Helper (Tkinter)

Abre uma UI simples para:

- listar campanhas
- selecionar campanha
- escolher um arquivo de áudio
- transcrever e gerar resumo

```bash
python src/main.py
```

**Observações**

- O arquivo de campanhas precisa existir em `Data/Campaings/campaings.json`.
- O resumo usa Ollama via LangChain. Ajuste o modelo em `src/ears/whisper.py` (variável `LLM_MODEL`).

### 2) Protótipo de UI (PyQt6)

Interface base com navegação de telas.

```bash
python src/main2.py
```

### 3) Extrator de PDF

Processa um PDF e salva imagens encontradas em `extracted_images/`.

```bash
python src/pdf_reader/pdf_agent.py
```

Por padrão o script tenta ler `DH.pdf` na raiz. Se não existir, edite `test_pdf_path` no final do arquivo.

## Notas importantes / TODOs

- `src/brain.py` contém experimentos com agentes e prompts de teste. Use como referência de experimentação, não como “produção”.
- `src/get_data.py` tem um bug (tenta imprimir `context['file_path']` mas a chave criada é `file name`).
- Os geradores em `src/gen/` estão vazios no momento.
- `src/main.py` tem um TODO antigo: “Trocar Tkinter por PySide6”. Hoje há um protótipo em PyQt6 (`main2.py`).

## Troubleshooting

### Whisper muito lento

- Em CPU, o Whisper (principalmente `large`) pode demorar bastante.
- Você pode trocar o modelo em `src/ears/whisper.py` (ex.: `base`, `small`, `medium`, `large`).

### Ollama não responde

- Garanta que o daemon do Ollama está rodando.
- Garanta que o modelo configurado em `LLM_MODEL` existe (ex.: `ollama pull deepseek-r1:latest`).

## Licença

Se você quiser, posso adicionar uma licença explícita (MIT/Apache-2.0/etc). Por enquanto, o repositório não declara licença aqui no README.

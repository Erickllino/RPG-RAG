---
title: RPG-RAG
emoji: 🎲
colorFrom: purple
colorTo: blue
sdk: gradio
sdk_version: "6.9.0"
python_version: "3.12"
app_file: app.py
pinned: false
---


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

## LLM Local com vLLM (opcional)

O projeto suporta rodar um LLM local via [vLLM](https://github.com/vllm-project/vllm)
como alternativa à API da Groq. Útil pra desenvolvimento offline, custos zero
e (futuramente) servir modelos fine-tuned.

### Por que um venv separado

vLLM tem requisitos rígidos de torch/CUDA que conflitam com Whisper e
`langchain-huggingface` no venv principal. A solução padrão é isolar o vLLM
em seu próprio ambiente — o projeto principal só conversa com ele via HTTP.

```
.venv/         ← venv principal (Whisper, FAISS, embeddings, gradio…)
.venv-vllm/    ← venv isolado, só com vllm + suas deps CUDA
```

### Setup (uma vez)

Pré-requisito: GPU NVIDIA com pelo menos 16GB VRAM (testado em RTX 5060 Ti).

```bash
uv venv .venv-vllm --python 3.12
uv pip install --python .venv-vllm/bin/python vllm --torch-backend=auto
```

A flag `--torch-backend=auto` deixa o uv detectar a versão do CUDA pelo
`nvidia-smi` e baixar o wheel compatível. Em GPUs Blackwell (RTX 50xx) com
driver recente isso é o stack CUDA 13.

### Subindo o servidor

```bash
python vllm/run_local.py
```

O script:
- Aponta pro binário em `.venv-vllm/bin/vllm`
- Configura `LD_LIBRARY_PATH` pra encontrar os `.so` de CUDA do venv isolado
- Sobe um servidor **OpenAI-compatible** em `http://localhost:8000/v1`
- Modelo padrão: `Qwen/Qwen2.5-7B-Instruct-AWQ` (4-bit, cabe folgado em 16GB)

Primeira execução baixa o modelo (~5GB) em `vllm/Models/` (ignorado pelo git).

### Usando no código

`src/llm/client.py` expõe três papéis (`Role`):

```python
from src.llm.client import get_llm, Role

llm = get_llm(Role.FAST)      # → Groq llama-3.1-8b-instant (padrão)
llm = get_llm(Role.CREATIVE)  # → Groq llama-3.3-70b-versatile
llm = get_llm(Role.LOCAL)     # → vLLM local (Qwen2.5-7B-AWQ)
```

`Role.LOCAL` usa `ChatOpenAI` apontando pro endpoint local — não precisa de
nenhum SDK específico do vLLM.

### Variáveis de ambiente (opcionais)

Todas têm default sensato; só sobrescreva no `.env` se precisar mudar:

| Variável | Default | Para quê |
| --- | --- | --- |
| `VLLM_BASE_URL` | `http://localhost:8000/v1` | URL do servidor local |
| `VLLM_MODEL` | `Qwen/Qwen2.5-7B-Instruct-AWQ` | Modelo servido pelo vLLM |
| `VLLM_API_KEY` | `EMPTY` | Token (vLLM aceita qualquer string por padrão) |

### Smoke test

Com o servidor rodando em outro terminal:

```bash
python -m src.llm.client --local
```

Deve imprimir uma resposta do Qwen local. Sem `--local`, usa Groq (`Role.CREATIVE`)
— bom pra confirmar que o fallback continua funcionando.

---

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

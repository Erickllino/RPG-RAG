# 🗺️ Plano de Reestruturação — RPG-RAG para Hugging Face

## 📋 Diagnóstico do projeto atual

O repositório atual foi projetado para **uso local**, com dependências que **não funcionam no Hugging Face Spaces**:

| Componente atual | Problema para HF deploy |
|---|---|
| `Tkinter` / `PyQt6` | Interfaces desktop — sem suporte em ambiente web |
| `Ollama` (LLM local) | Exige daemon rodando localmente |
| `Whisper` local (arquivo MP3) | Upload de áudio precisa de outro mecanismo |
| `PyMuPDF` (leitura de PDF) | Pode ser mantido, mas precisa de adaptação |
| `src/brain.py`, `src/get_data.py` | Rascunhos/experimentos — não devem ir para produção |
| `Data/` com arquivos locais | Dados precisam ser embarcados no repo ou carregados via upload |

---

## 🎯 Objetivo do deploy no Hugging Face

Criar uma **interface web** (via Gradio) onde o usuário pode:

1. Fazer upload de PDFs de lore/campanha ou colar texto
2. Fazer perguntas sobre o conteúdo (RAG)
3. Receber respostas do LLM com base nos documentos carregados

---

## 🗂️ Nova estrutura de projeto proposta

```
RPG-RAG/
│
├── app.py                    ← Ponto de entrada do HF Space (Gradio)
├── requirements.txt          ← Dependências atualizadas (sem Ollama/Tkinter/PyQt6)
├── README.md                 ← README principal (mantido/atualizado)
├── .gitignore
│
├── src/
│   ├── rag/
│   │   ├── __init__.py
│   │   ├── loader.py         ← Carrega PDFs, TXTs, strings (substitui pdf_agent.py)
│   │   ├── embedder.py       ← Gera embeddings e monta vector store (FAISS ou Chroma)
│   │   └── retriever.py      ← Busca trechos relevantes para a pergunta
│   │
│   ├── llm/
│   │   ├── __init__.py
│   │   └── chain.py          ← Monta a chain RAG com LLM de API (HF Inference ou OpenAI)
│   │
│   └── ui/
│       ├── __init__.py
│       └── gradio_app.py     ← Componentes e lógica da interface Gradio
│
├── data/
│   └── example_lore/         ← Lore de exemplo para demo (textos .txt)
│       └── ekalia_sample.txt
│
└── notebooks/                ← (opcional) experimentos e protótipos
    ├── rag_experiment.ipynb
    └── pdf_extraction.ipynb
```

---

## 🔧 Mudanças necessárias arquivo por arquivo

### Remover / Arquivar
- `src/main.py` — interface Tkinter, não compatível com HF
- `src/main2.py` — protótipo PyQt6, não compatível com HF
- `src/brain.py` — experimento com prompts inadequados, não vai para produção
- `src/get_data.py` — tem bugs conhecidos, mover para `notebooks/`
- `src/gen/` — geradores vazios, remover ou mover para notebooks

### Adaptar / Migrar
- `src/ears/whisper.py` → pode ser migrado para `src/rag/loader.py` com suporte a upload de áudio via Gradio (opcional, fase 2)
- `src/pdf_reader/pdf_agent.py` → migrar lógica de extração para `src/rag/loader.py`
- `Data/Ekalia/` → mover conteúdo de exemplo para `data/example_lore/`

### Criar do zero
- `app.py` — entry point Gradio para o HF Space
- `src/rag/embedder.py` — embeddings com `sentence-transformers` (gratuito, roda no HF)
- `src/rag/retriever.py` — busca vetorial com FAISS
- `src/llm/chain.py` — integração com LLM via API (ex: `HuggingFaceHub`, `groq`, ou `openai`)

---

## 📦 Novo `requirements.txt`

```txt
gradio>=4.0
langchain>=0.2
langchain-community>=0.2
sentence-transformers>=2.5
faiss-cpu>=1.7
pymupdf>=1.23           # leitura de PDFs (PyMuPDF)
python-dotenv>=1.0

# Escolha UM provedor de LLM (descomente o que for usar):
# openai>=1.0           # via OpenAI API
# groq>=0.5             # via Groq API (rápido e gratuito com limite)
# huggingface-hub>=0.20 # via HF Inference API
```

> ⚠️ **Remover**: `pyqt6`, `tkinter` (built-in), `ollama`, `openai-whisper`

---

## 🔑 Variáveis de ambiente (Secrets no HF Space)

No painel do HF Space → **Settings → Repository secrets**, adicione:

| Variável | Descrição |
|---|---|
| `OPENAI_API_KEY` | Se usar OpenAI como LLM |
| `GROQ_API_KEY` | Se usar Groq como LLM (recomendado: grátis) |
| `HF_TOKEN` | Se usar HF Inference API como LLM |

---

## 🚀 Ordem de execução recomendada

1. **Criar `app.py`** com interface Gradio básica (upload de PDF + chat)
2. **Implementar `src/rag/loader.py`** — extração de texto de PDFs e TXTs
3. **Implementar `src/rag/embedder.py`** — embeddings + FAISS index
4. **Implementar `src/rag/retriever.py`** — busca semântica
5. **Implementar `src/llm/chain.py`** — prompt + LLM + resposta
6. **Conectar tudo em `src/ui/gradio_app.py`**
7. **Atualizar `requirements.txt`**
8. **Testar localmente** com `python app.py`
9. **Push para HF Space** via git

---

## 💡 Recomendação de LLM para HF Space

| Opção | Custo | Qualidade | Setup |
|---|---|---|---|
| **Groq API** (llama3, mixtral) | Gratuito (com limite) | ⭐⭐⭐⭐ | Fácil |
| HF Inference API | Gratuito (lento) | ⭐⭐⭐ | Fácil |
| OpenAI (gpt-4o-mini) | Pago | ⭐⭐⭐⭐⭐ | Fácil |
| Ollama | Gratuito | ⭐⭐⭐⭐ | ❌ Não funciona no HF |

> **Recomendação**: comece com **Groq** (llama-3.1-8b-instant) — é gratuito, rápido e fácil de configurar.

---

## 📝 Notas finais

- O `Data/Campaings/campaings.json` pode ser mantido como dado de exemplo no repositório
- A pasta `models/` (modelos locais qwen) **não deve ir para o HF** — é pesada e não é usada na versão web
- Adicione `models/` e `Data/Audios/` ao `.gitignore` se ainda não estiverem

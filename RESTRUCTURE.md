# 🗺️ Plano de Reestruturação — RPG-RAG para Hugging Face

## 🎯 Visão geral

Uma única aplicação Gradio (um Space no HF) com **6 ferramentas em abas separadas**, todas compartilhando um único vector store FAISS. As ferramentas se comunicam tanto de forma independente (acessando os mesmos dados) quanto em pipeline sequencial (ex: áudio da sessão → resumo → contexto do assistente de sessão).

---

## 🗂️ Estrutura de projeto proposta

```
RPG-RAG/
│
├── app.py                        ← Entry point: monta as abas Gradio e inicializa o vector store
├── requirements.txt
├── README.md
├── .gitignore
│
├── data/
│   ├── lore/                     ← Arquivos .md com a lore do mundo (input do vector store)
│   │   └── ekalia/               ← Exemplo: mundo Ekalia
│   ├── sessions/                 ← Resumos de sessões gerados pela ferramenta de áudio
│   │   └── summaries/            ← .txt ou .md gerados automaticamente
│   └── vector_store/             ← FAISS index persistido (gerado, não commitado no git)
│       ├── lore.index
│       └── sessions.index
│
├── src/
│   │
│   ├── vector_store/             ← Núcleo compartilhado por todas as ferramentas
│   │   ├── __init__.py
│   │   ├── builder.py            ← Lê os .md e constrói/atualiza o FAISS index
│   │   ├── retriever.py          ← Interface de busca semântica usada por todas as tools
│   │   └── embedder.py           ← Modelo de embedding (sentence-transformers)
│   │
│   ├── tools/                    ← Uma subpasta por ferramenta
│   │   │
│   │   ├── session_audio/        ← FERRAMENTA 2: Áudio de sessão → resumo
│   │   │   ├── __init__.py
│   │   │   ├── transcriber.py    ← Whisper (via API ou local leve)
│   │   │   ├── summarizer.py     ← Groq: resume a transcrição
│   │   │   └── indexer.py        ← Adiciona o resumo ao vector store de sessões
│   │   │
│   │   ├── npc_generator/        ← FERRAMENTA 3: Gerador de NPC
│   │   │   ├── __init__.py
│   │   │   └── generator.py      ← Groq + retriever (lore + sessões) → NPC
│   │   │
│   │   ├── quest_generator/      ← FERRAMENTA 4: Gerador de missões
│   │   │   ├── __init__.py
│   │   │   └── generator.py      ← Groq + retriever (lore + sessões) → missão
│   │   │
│   │   ├── session_assistant/    ← FERRAMENTA 5: Assistente de sessão ao vivo
│   │   │   ├── __init__.py
│   │   │   └── assistant.py      ← Groq + retriever (lore + sessões) → chat
│   │   │
│   │   └── lore_writer/          ← FERRAMENTA 6: Escritor de lore
│   │       ├── __init__.py
│   │       └── writer.py         ← Groq + retriever (lore) → novo conteúdo de lore
│   │
│   ├── llm/
│   │   ├── __init__.py
│   │   └── groq_client.py        ← Cliente Groq centralizado (todas as tools usam esse)
│   │
│   └── ui/
│       ├── __init__.py
│       ├── tab_vector_store.py   ← Aba 1: gerenciar e rebuild o vector store
│       ├── tab_session_audio.py  ← Aba 2: upload de áudio → transcrição + resumo
│       ├── tab_npc.py            ← Aba 3: gerador de NPC
│       ├── tab_quest.py          ← Aba 4: gerador de missões
│       ├── tab_session_chat.py   ← Aba 5: assistente de sessão (chat)
│       └── tab_lore_writer.py    ← Aba 6: escritor de lore (chat)
│
└── notebooks/                    ← Experimentos e rascunhos do projeto original
    ├── rag_experiment.ipynb
    └── pdf_extraction.ipynb
```

---

## 🔗 Fluxo de dados entre as ferramentas

```
data/lore/*.md
      │
      ▼
[builder.py] ───────────────────────FAISS lore.index
                                            │
      ┌─────────────────────────────────────┼───────────────────────┐
      │                |                    │                       │
      ▼                ▼                    │                       ▼
[quest_generator][npc_generator]            │                 [lore_writer]
      │                │                    │                       │
      │                └────────────────────┐                       ▼
      └───────────────────────────>[session_assistant]         (novo .md)                    
                            ▲                                       │ 
[session_audio] ─── FAISS sessions.index                            │
áudio → transcrição                                                 ▼
      → resumo                                                  data/lore/ (opcional)
      → indexado
                         
                
```

---

## ⚙️ Vector Store — detalhe importante

O FAISS será dividido em **dois indexes separados**, mas acessados pela mesma interface:

| Index            | Fonte                          | Atualizado por                           |
| ---------------- | ------------------------------ | ---------------------------------------- |
| `lore.index`     | `data/lore/*.md`               | Manualmente via aba "Vector Store"       |
| `sessions.index` | `data/sessions/summaries/*.md` | Automaticamente pela ferramenta de áudio |

O `retriever.py` aceita um parâmetro `source` para buscar em um ou nos dois indexes ao mesmo tempo.

---

## 🤖 LLM — Groq centralizado

Todas as ferramentas usam `src/llm/groq_client.py`. Modelos sugeridos:

| Ferramenta           | Modelo Groq sugerido      | Motivo                   |
| -------------------- | ------------------------- | ------------------------ |
| Resumo de sessão     | `llama-3.1-8b-instant`    | Rápido, texto longo      |
| Gerador de NPC       | `llama-3.3-70b-versatile` | Mais criativo            |
| Gerador de missões   | `llama-3.3-70b-versatile` | Mais criativo            |
| Assistente de sessão | `llama-3.1-8b-instant`    | Baixa latência (ao vivo) |
| Escritor de lore     | `llama-3.3-70b-versatile` | Qualidade de escrita     |

---

## 📦 `requirements.txt`

```txt
gradio>=4.0
langchain>=0.2
langchain-community>=0.2
langchain-groq>=0.1
sentence-transformers>=2.5
faiss-cpu>=1.7
groq>=0.5
openai-whisper>=20231117     # transcrição de áudio (modelo tiny/base para HF)
python-dotenv>=1.0
pymupdf>=1.23                # se quiser manter suporte a PDF futuramente
```

---

## 🔑 Secrets no HF Space

| Variável       | Uso                      |
| -------------- | ------------------------ |
| `GROQ_API_KEY` | Todas as ferramentas LLM |

---

## 🚀 Ordem de implementação recomendada

1. `src/llm/groq_client.py` — base de tudo
2. `src/vector_store/` — builder + embedder + retriever
3. `src/tools/session_audio/` — pipeline de áudio (ferramenta 2)
4. `src/tools/npc_generator/` — gerador de NPC (ferramenta 3)
5. `src/tools/quest_generator/` — gerador de missões (ferramenta 4)
6. `src/tools/session_assistant/` — assistente de sessão (ferramenta 5)
7. `src/tools/lore_writer/` — escritor de lore (ferramenta 6)
8. `src/ui/` — todas as abas Gradio
9. `app.py` — junta tudo
10. Deploy no HF Space

---

## 🗑️ O que remover do projeto atual

| Arquivo/Pasta  | Motivo                                  |
| -------------- | --------------------------------------- |
| `src/main.py`  | Interface Tkinter — não funciona no HF  |
| `src/main2.py` | Protótipo PyQt6 — não funciona no HF    |
| `src/brain.py` | Experimento com prompts inadequados     |
| `src/gen/`     | Geradores vazios                        |
| `models/`      | Modelos locais pesados — não usar no HF |
| `Data/Audios/` | Áudios locais — não commitar            |

## ✅ O que migrar/aproveitar

| Arquivo atual                 | Destino novo                                              |
| ----------------------------- | --------------------------------------------------------- |
| `src/pdf_reader/pdf_agent.py` | Lógica base para `src/vector_store/builder.py`            |
| `src/ears/whisper.py`         | Lógica base para `src/tools/session_audio/transcriber.py` |
| `Data/Ekalia/*.txt`           | Converter para `.md` e mover para `data/lore/ekalia/`     |
| `src/get_data.py`             | `notebooks/` (com bug documentado)                        |
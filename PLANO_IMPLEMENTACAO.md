# 📚 Plano de Implementação — RPG-RAG

> **Propósito:** Este documento é o roteiro didático de implementação do projeto.
> Diferente do `RESTRUCTURE.md` (que descreve a *arquitetura final*), aqui está
> o **passo a passo de aprendizado e implementação**, com checklist por etapa.

---

## 🎯 Objetivos do projeto

1. **Aprender LangChain 1.x** com qualidade de código profissional.
2. **Construir um RAG completo** sobre lore de RPG (mundo Ekalia).
3. **Deploy num Hugging Face Space** com 6 ferramentas em abas Gradio.
4. **Material defensável em entrevista** — saber justificar cada decisão técnica.

---

## 🧱 Stack escolhida

| Camada | Tecnologia | Por quê |
| --- | --- | --- |
| LLM | Groq (`llama-3.3-70b-versatile`, `llama-3.1-8b-instant`) | Gratuito, baixa latência |
| Wrapper LLM | `langchain-groq` (LangChain 1.x) | Plugável no ecossistema LCEL |
| Composição | **LCEL** (`prompt \| llm \| parser`) | Padrão atual em produção |
| Embeddings | `HuggingFaceEmbeddings` (multilíngue) | Local, gratuito, pt-BR |
| Vector store | FAISS (via `langchain-community`) | Local, leve, persistível |
| UI | Gradio | HF Space-friendly |
| Áudio | Whisper (local ou API) | Transcrição de sessões |

**Decisão consciente:** *não* usamos LangGraph nesta primeira versão. Todas as
tools são fluxos determinísticos — LCEL é suficiente. Se um dia aparecer um
agente com loop/branch/estado complexo, aí sim entra LangGraph.

---

## 🪜 Ordem de implementação

A ordem importa: cada etapa desbloqueia a próxima.

### Etapa 1 — `src/llm/client.py` ✅ CONCLUÍDA
- [x] Bloco 1: imports + `load_dotenv` + esqueleto
- [x] Bloco 2: `Role` enum (StrEnum)
- [x] Bloco 3: `_MODEL_CONFIG` (dataclass `ModelSpec` + dict)
- [x] Bloco 4: `get_llm(role) -> ChatGroq` factory
- [x] Smoke test: `python -m src.llm.client` retornando resposta
- [x] **Shim temporário** `infer_model()` adicionado pra compat com tools legadas

#### 🧹 Pendências de limpeza (quando voltar a este arquivo)
- [ ] Remover comentários de esqueleto que sobraram dentro de `get_llm()`
- [ ] Confirmar troca do modelo `FAST` de `groq/compound` → `llama-3.1-8b-instant` (mais rápido, maior TPM, mesma free tier)
- [ ] Decidir se `role` mantém default `Role.FAST` ou vira obrigatório (recomendação: obrigatório)
- [ ] Quando todas as 4 tools migrarem pra chains LCEL → **deletar o `infer_model` shim**

### Etapa 2 — `src/llm/prompts.py` 🚧 PRÓXIMA
- [ ] Bloco 1: imports + `SESSION_ASSISTANT_PROMPT`
- [ ] Bloco 2: `NPC_GENERATOR_PROMPT` (com variável `{lore}`)
- [ ] Bloco 3: `QUEST_GENERATOR_PROMPT` + `LORE_WRITER_PROMPT`
- [ ] Bloco 4: `SESSION_SUMMARIZER_PROMPT`
- [ ] Convenção de variáveis: `{lore}`, `{question}`, `{history}`, `{request}`

### Etapa 3 — `src/vector_store/`
- [ ] `embedder.py`: factory `get_embeddings()` (modelo multilíngue)
- [ ] `builder.py`: pipeline discovery → load → split → embed → save
  - [ ] `discover_files(data_dir)`
  - [ ] `load_documents(paths)` — com metadados
  - [ ] `split_documents(docs)` — Recursive ou MarkdownHeader
  - [ ] `build_index(chunks, embeddings) -> FAISS`
  - [ ] `build_and_save(data_dir, index_dir)` — orquestrador
- [ ] `retriever.py`: `get_retriever(source="lore"|"sessions"|"all")`

### Etapa 4 — Tools (uma de cada vez, em pipeline LCEL)
- [ ] `session_audio/` (transcriber → summarizer → indexer)
- [ ] `npc_generator/` (RAG + LLM CREATIVE → NPC)
- [ ] `quest_generator/` (RAG + LLM CREATIVE → missão)
- [ ] `session_assistant/` (RAG + LLM FAST + `RunnableWithMessageHistory`)
- [ ] `lore_writer/` (RAG + LLM CREATIVE → novo .md)

### Etapa 5 — UI Gradio
- [ ] `app.py`: monta abas, inicializa retriever compartilhado
- [ ] Uma `tab_*.py` por tool

### Etapa 6 — Deploy
- [ ] Validação local
- [ ] Hugging Face Space (Secrets: `GROQ_API_KEY`)

---

## 📖 Detalhamento — Etapa 1: `client.py`

### Conceitos novos por bloco

| Bloco | Conceito chave | Por que é importante |
| --- | --- | --- |
| 1 — imports | `load_dotenv` antes de qualquer import que leia env | Ordem de execução em Python |
| 2 — `Role` | `StrEnum` (Python 3.11+) | Tipo seguro, serializa como string |
| 3 — `_MODEL_CONFIG` | `@dataclass(frozen=True)` | Type-safety vs dict solto |
| 4 — `get_llm` | Factory function pattern | Centraliza criação, separa "papel" de "modelo" |

### Anatomia final esperada

```python
"""Cliente LLM centralizado."""

# 1. dotenv (cuidado com ordem)
# 2. enum (StrEnum)
# 3. dataclass
# 4. ChatGroq

class Role(StrEnum):
    CREATIVE = "creative"
    FAST = "fast"

@dataclass(frozen=True)
class ModelSpec:
    model: str
    temperature: float

_MODEL_CONFIG: dict[Role, ModelSpec] = { ... }

def get_llm(role: Role) -> ChatGroq:
    spec = _MODEL_CONFIG[role]
    return ChatGroq(model=spec.model, temperature=spec.temperature, ...)
```

### Pontos de defesa em entrevista

- *"Por que factory e não classe?"* → ChatGroq já é a classe, encapsular sem motivo é code smell. Estado vive na UI/chain, não no client.
- *"Por que StrEnum?"* → Serialização natural pra logs/JSON, type-safe.
- *"Por que separar Role e modelo?"* → Trocar de modelo/provider vira 1 linha. Tools não acoplam a vendor.

---

## 📖 Detalhamento — Etapa 2: `prompts.py`

### Estrutura proposta

```python
from langchain_core.prompts import ChatPromptTemplate

NPC_GENERATOR_PROMPT = ChatPromptTemplate.from_messages([
    ("system", "Você é um GM criando NPCs para o mundo {world}..."),
    ("human", "Crie um NPC com base na lore:\n\n{lore}\n\nPedido: {request}"),
])

SESSION_ASSISTANT_PROMPT = ChatPromptTemplate.from_messages([
    ("system", "Você é um assistente de sessão de RPG..."),
    ("placeholder", "{history}"),
    ("human", "{question}"),
])
# ...etc
```

### Princípios

1. **Um arquivo só** com todos os prompts (centralização).
2. Constantes em `UPPER_SNAKE_CASE`.
3. Variáveis de template em **inglês** (`{lore}`, `{question}`) por convenção.
4. Conteúdo do prompt em **português** (é a língua do mundo Ekalia).

---

## 📖 Detalhamento — Etapa 3: `vector_store/`

### Pipeline conceitual do `builder.py`

```
DATA_DIR (Data/Ekalia)
   │  rglob("*.md")
   ▼
discover_files()  →  list[Path]
   │
   ▼
load_documents()  →  list[Document]   (page_content + metadata)
   │
   ▼
split_documents() →  list[Document]   (chunks de ~500 chars)
   │
   ▼
build_index()     →  FAISS object
   │
   ▼
save_local(INDEX_DIR)
```

### Decisões pendentes (definir antes de codar)

- [ ] Trocar embedding pra `paraphrase-multilingual-MiniLM-L12-v2`?
- [ ] Splitter: `RecursiveCharacterTextSplitter` (didático) ou `MarkdownHeaderTextSplitter` (melhor pro domínio)?
- [ ] Builder gera 1 índice (`lore`) ou 2 (`lore` + `sessions`)?
- [ ] Como tratar `calendar.json`? (vira documento? metadado? ignora?)

---

## 🚫 O que evitar (armadilhas conhecidas)

1. **Re-instanciar `ChatGroq` a cada chamada** — desperdício, mantenha factory.
2. **Re-embeddar a cada importação** — builder roda 1×; retriever só carrega.
3. **Embedding diferente entre build e query** — vetores em espaços diferentes = busca quebrada.
4. **`AgentExecutor` / `LLMChain` clássicos** — *deprecated* na 1.0. Usar LCEL.
5. **Hardcode no escopo do módulo** — todo código executável dentro de `if __name__ == "__main__":` ou função.
6. **Esquecer metadata nos Documents** — sem `source`, RAG não cita fonte.

---

## 🎓 O que vai pro currículo

- "Construí RAG end-to-end com LangChain 1.x e LCEL."
- "Vector store FAISS persistido com embeddings multilíngues HuggingFace."
- "Factory pattern e dataclass para gerenciamento de configuração de LLM."
- "Pipeline de áudio: Whisper → resumo via Groq → indexação automática."
- "6 ferramentas em pipeline desacoplado, deploy em Hugging Face Spaces."

---

## 📝 Histórico de decisões (ADR-lite)

| Data | Decisão | Motivo |
| --- | --- | --- |
| 2026-05-10 | Usar LangChain 1.x (não 0.3) | API estável, padrão atual de mercado |
| 2026-05-10 | LCEL como composição (não LangGraph) | Tools são determinísticas, sem loops |
| 2026-05-10 | Factory function (não classe) pro LLM client | Estado vive em camadas superiores |
| 2026-05-10 | `StrEnum` para `Role` | Python 3.12+, type-safe, serializável |
| 2026-05-10 | Shim `infer_model()` em `client.py` | Compat com tools legadas; remover após migração LCEL |

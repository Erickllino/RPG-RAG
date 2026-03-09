"""
Configurações do Vector Store
"""

import os
from pathlib import Path

# ── Paths ──────────────────────────────────────────────────────────────────────
ROOT_DIR = Path(__file__).resolve().parents[2]          # raiz do projeto
DATA_DIR = ROOT_DIR / "Data" / "Ekalia"                 # .md de lore
INDEX_DIR = ROOT_DIR / "Data" / "vector_store_index"   # onde salvar o índice FAISS

# ── Embedding Model (HuggingFace, local, gratuito) ────────────────────────────
EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"
# Alternativa multilíngue (melhor para pt-BR):
# EMBEDDING_MODEL = "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"

# ── Chunking ──────────────────────────────────────────────────────────────────
CHUNK_SIZE = 500        # caracteres por chunk
CHUNK_OVERLAP = 50      # sobreposição entre chunks

# ── Groq LLM ──────────────────────────────────────────────────────────────────
GROQ_MODEL = "groq/compound"           # modelo padrão (rápido e gratuito)
# Alternativas: "llama3-70b-8192", "mixtral-8x7b-32768", "gemma2-9b-it", "groq/compound"
GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")   # definir como variável de ambiente

# ── RAG ───────────────────────────────────────────────────────────────────────
TOP_K = 5   # número de chunks retornados na busca

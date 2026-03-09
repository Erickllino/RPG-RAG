
from langchain_community.document_loaders import TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings

from .configs import DATA_DIR, INDEX_DIR, EMBEDDING_MODEL, CHUNK_SIZE, CHUNK_OVERLAP


from pathlib import Path




## get all docs

def get_data():
    data = {
        "File Name": [],
        "Context": [],
        "Content": [],
    }

    for file_path in DATA_DIR.rglob("*.txt"):
        content = file_path.read_text(encoding="utf-8")

        data["File Name"].append(file_path.name)
        data["Content"].append(content)

        # Context = relative path inside Ekalia
        context = file_path.parent.relative_to(DATA_DIR)
        data["Context"].append(str(context))

        print(f"Read file: {context}/{file_path.name} ({len(content)})")

    return data


def build_embeddings() -> HuggingFaceEmbeddings:
    """Instancia o modelo de embeddings HuggingFace."""
    print(f"[builder] Carregando modelo de embeddings: {EMBEDDING_MODEL}")
    return HuggingFaceEmbeddings(
        model_name=EMBEDDING_MODEL,
        model_kwargs={"device": "cpu"},
        encode_kwargs={"normalize_embeddings": True},
    )




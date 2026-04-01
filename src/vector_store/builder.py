from pathlib import Path

from .configs import DATA_DIR, INDEX_DIR, EMBEDDING_MODEL, CHUNK_SIZE, CHUNK_OVERLAP




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


def build_embeddings():
    """Instancia o modelo de embeddings HuggingFace."""
    raise NotImplementedError



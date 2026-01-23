from pathlib import Path


# project root (RPG-RAG/)
PROJECT_ROOT = Path(__file__).resolve().parents[2]

# Data/Ekalia
DATA_DIR = PROJECT_ROOT / "Data" / "Ekalia"


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

import subprocess
from langchain.tools import tool

@tool
def listar_arquivos() -> str:
    """Lista arquivos da pasta atual."""

    resultado = subprocess.run(
        ["ls"],
        capture_output=True,
        text=True
    )

    return resultado.stdout
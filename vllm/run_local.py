"""
Sobe um servidor vLLM local com API compatível com OpenAI.

Por que um venv separado?
-------------------------
vLLM tem requisitos rígidos de torch/CUDA que conflitam com Whisper,
langchain-huggingface e outras libs ML do projeto principal. A prática
padrão é isolar vLLM em seu próprio venv (.venv-vllm) e falar com ele
só via HTTP — assim o venv principal não sofre.

Setup (uma vez)
---------------
    uv venv .venv-vllm --python 3.12
    uv pip install --python .venv-vllm/bin/python vllm --torch-backend=cu128

Uso
---
    python vllm/run_local.py

A API fica em http://localhost:8000/v1 (formato OpenAI).
O cliente em src/llm/client.py já aponta pra cá quando usa Role.LOCAL.
"""

import os
import subprocess
import sys
from pathlib import Path


SCRIPT_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = SCRIPT_DIR.parent
VLLM_VENV = PROJECT_ROOT / ".venv-vllm"
VLLM_BIN = VLLM_VENV / "bin" / "vllm"


# ── Configuração ────────────────────────────────────────────────
# Modelo AWQ (4-bit) cabe folgado em 16GB VRAM e deixa muito espaço pra KV cache.
MODEL = "Qwen/Qwen2.5-7B-Instruct-AWQ"

HOST = "127.0.0.1"
PORT = 8000

# Qwen2.5 suporta até 32K, mas KV cache cresce com o contexto.
# Em 16GB VRAM, 8192 deixa margem confortável pro RAG (queries + chunks + resposta).
MAX_MODEL_LEN = 8192

# Fração da VRAM que o vLLM pode usar. Deixamos ~15% pro desktop/OS.
GPU_MEMORY_UTILIZATION = 0.85


def _vllm_site_packages() -> Path:
    """Localiza site-packages do .venv-vllm (versão minor do Python pode variar)."""
    candidates = sorted((VLLM_VENV / "lib").glob("python*/site-packages"))
    if not candidates:
        raise FileNotFoundError(f"site-packages não encontrado em {VLLM_VENV}/lib")
    return candidates[0]


def _build_ld_library_path() -> str:
    """
    Pacotes nvidia-* (cu12/cu13) instalam .so em site-packages/nvidia/<lib>/lib/,
    fora do search path padrão do dlopen. Sem isso o vLLM falha com
    'libcudart.so.X: cannot open shared object file'.
    """
    nvidia_root = _vllm_site_packages() / "nvidia"
    nvidia_libs = sorted(str(p) for p in nvidia_root.glob("*/lib") if p.is_dir())
    existing = os.environ.get("LD_LIBRARY_PATH", "")
    parts = nvidia_libs + ([existing] if existing else [])
    return os.pathsep.join(parts)


def _check_setup() -> str | None:
    """Retorna mensagem de erro se o setup do venv estiver faltando."""
    if not VLLM_VENV.is_dir():
        return (
            f"Venv do vLLM não encontrado em {VLLM_VENV}.\n"
            "Setup (uma vez):\n"
            "    uv venv .venv-vllm --python 3.12\n"
            "    uv pip install --python .venv-vllm/bin/python vllm --torch-backend=cu128"
        )
    if not VLLM_BIN.is_file():
        return (
            f"Binário 'vllm' não encontrado em {VLLM_BIN}.\n"
            "Instale com:\n"
            "    uv pip install --python .venv-vllm/bin/python vllm --torch-backend=cu128"
        )
    return None


def main() -> int:
    if err := _check_setup():
        print(err)
        return 1

    cmd = [
        str(VLLM_BIN), "serve", MODEL,
        "--host", HOST,
        "--port", str(PORT),
        "--max-model-len", str(MAX_MODEL_LEN),
        "--gpu-memory-utilization", str(GPU_MEMORY_UTILIZATION),
        "--dtype", "auto",
        "--download-dir", str(SCRIPT_DIR / "Models"),
        "--enable-auto-tool-choice",
        "--tool-call-parser", "hermes",
    ]

    env = {**os.environ, "LD_LIBRARY_PATH": _build_ld_library_path()}

    print(f"Usando vLLM de: {VLLM_VENV}")
    print("Comando:")
    print("  " + " ".join(cmd))
    print()

    try:
        return subprocess.run(cmd, env=env, check=False).returncode
    except KeyboardInterrupt:
        print("\nServidor encerrado.")
        return 0


if __name__ == "__main__":
    sys.exit(main())

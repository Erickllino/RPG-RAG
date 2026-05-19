import gradio as gr
from agent.src.vector_store.configs import INDEX_DIR


def _index_exists() -> bool:
    return (INDEX_DIR / "index.faiss").exists()


def _status_message() -> str:
    if _index_exists():
        return "Index found at: " + str(INDEX_DIR)
    return "No index found. Click 'Build Index' to create one."


def build_index_action():
    try:
        from src.vector_store.builder import get_data, build_index
    except ImportError as e:
        yield f"Missing dependency: {e}"
        return

    yield "Loading files...\n"
    docs = get_data()
    yield f"Loaded {len(docs)} files.\n\nChunking and embedding (this may take a while)...\n"
    build_index()
    yield f"Done! Index saved to:\n{INDEX_DIR}"


def test_search_action(query: str):
    if not query.strip():
        return "Type a query above first."
    if not _index_exists():
        return "Index not found. Build it first."

    try:
        from src.vector_store.builder import load_index
    except ImportError as e:
        return f"Missing dependency: {e}"

    vs = load_index()
    results = vs.similarity_search(query, k=5)

    lines = []
    for i, doc in enumerate(results, 1):
        source = doc.metadata.get("source", "?")
        context = doc.metadata.get("context", "")
        lines.append(f"### Result {i} — `{context}/{source}`\n{doc.page_content}")

    return "\n\n---\n\n".join(lines)


def create_tab():
    with gr.Tab("Vector Store"):
        gr.Markdown("## Vector Store\nBuild the FAISS index from your lore files, then test retrieval.")

        status = gr.Textbox(
            label="Status",
            value=_status_message,
            interactive=False,
            lines=1,
        )

        build_btn = gr.Button("Build Index", variant="primary")
        log = gr.Textbox(label="Log", lines=8, interactive=False)

        build_btn.click(fn=build_index_action, outputs=log)

        gr.Markdown("---\n### Test Retrieval")
        query_box = gr.Textbox(label="Query", placeholder="e.g. Quais guildas existem em Ploya?")
        search_btn = gr.Button("Search")
        results_box = gr.Markdown()

        search_btn.click(fn=test_search_action, inputs=query_box, outputs=results_box)

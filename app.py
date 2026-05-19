import gradio as gr

from agent.src.ui.tab_vector_store import create_tab as tab_vector_store
from agent.src.ui.tab_session_audio import create_tab as tab_session_audio
from agent.src.ui.tab_lore_writer import create_tab as tab_lore_writer
from agent.src.ui.tab_session_chat import create_tab as tab_session_chat
from agent.src.ui.tab_npc import create_tab as tab_npc
from agent.src.ui.tab_quest import create_tab as tab_quest

CSS = """
/* Hide the root-level tab navigation bar */
#root-tabs > .tab-nav { display: none !important; }

/* ── Main menu ─────────────────────────────────────────────── */
#main-title {
    text-align: center;
    font-size: 2.5rem !important;
    font-weight: 700;
    letter-spacing: 0.05em;
}
#main-subtitle {
    text-align: center;
    opacity: 0.6;
    font-size: 1rem;
}
#btn-prepare, #btn-playing {
    min-width: 200px !important;
    min-height: 80px !important;
    font-size: 1.2rem !important;
    border-radius: 12px !important;
}

/* ── Back buttons ───────────────────────────────────────────── */
#btn-back-prepare, #btn-back-playing {
    max-width: 100px !important;
}
"""

theme = gr.themes.Origin(
    primary_hue="amber",
    secondary_hue="orange",
    neutral_hue="stone",
)

my_theme = gr.Theme.from_hub("hmb/spark")


import argparse

parser = argparse.ArgumentParser(
                    prog='RPG-RAG',
                    description='What the program does',
                    epilog='Text at the bottom of help')

parser.add_argument('--local', action='store_true', help='Go directly to the Prepare tab')




with gr.Blocks(title="RPG-RAG") as demo:

    with gr.Tabs(selected=0, elem_id="root-tabs") as root_tabs:

        # ── Main menu ──────────────────────────────────────────────────────────
        with gr.Tab("Menu", id=0):
            gr.Markdown("# RPG-RAG", elem_id="main-title")
            gr.Markdown("Your AI toolkit for the Ekalia campaign.", elem_id="main-subtitle")
            gr.Markdown("")
            with gr.Row():
                prepare_btn = gr.Button("⚙️  Prepare", variant="primary", elem_id="btn-prepare")
                playing_btn = gr.Button("⚔️  Playing", variant="primary", elem_id="btn-playing")
            gr.Markdown("")

        # ── Prepare ────────────────────────────────────────────────────────────
        with gr.Tab("Prepare", id=1):
            with gr.Row():
                gr.Markdown("## ⚙️ Prepare")
                back_prepare = gr.Button("← Back", elem_id="btn-back-prepare", scale=0)
            with gr.Tabs():
                tab_vector_store()
                tab_session_audio()
                tab_lore_writer()

        # ── Playing ────────────────────────────────────────────────────────────
        with gr.Tab("Playing", id=2):
            with gr.Row():
                gr.Markdown("## ⚔️ Playing")
                back_playing = gr.Button("← Back", elem_id="btn-back-playing", scale=0)
            with gr.Tabs():
                tab_session_chat()
                tab_npc()
                tab_quest()

    # ── Navigation ──────────────────────────────────────────────────────────
    prepare_btn.click(fn=lambda: gr.update(selected=1), outputs=root_tabs)
    playing_btn.click(fn=lambda: gr.update(selected=2), outputs=root_tabs)
    back_prepare.click(fn=lambda: gr.update(selected=0), outputs=root_tabs)
    back_playing.click(fn=lambda: gr.update(selected=0), outputs=root_tabs)


if __name__ == "__main__":

    if parser.parse_args().local:
        print("TEST")
    demo.launch(theme=my_theme, css=CSS)

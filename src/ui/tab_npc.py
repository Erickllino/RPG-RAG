import gradio as gr
from src.llm.client import infer_model

SYSTEM_PROMPT = (
    "You are a creative RPG game master assistant for the Ekalia campaign. "
    "Generate detailed, flavourful NPCs that fit the world's tone. "
    "Include name, appearance, personality, role, a secret, and a plot hook. "
    "Write in English unless asked otherwise."
)


def generate_npc(location: str, role: str, traits: str):
    if not location and not role:
        return "Fill in at least a location or role."

    prompt_parts = ["Generate an NPC"]
    if location:
        prompt_parts.append(f"from {location}")
    if role:
        prompt_parts.append(f"who is a {role}")
    if traits:
        prompt_parts.append(f"with the following traits: {traits}")
    prompt = " ".join(prompt_parts) + "."

    content, _ = infer_model(prompt, messages=[{"role": "system", "content": SYSTEM_PROMPT}])
    return content


def create_tab():
    with gr.Tab("NPC Generator"):
        gr.Markdown("## NPC Generator\n> Generate NPCs consistent with the Ekalia lore.")
        with gr.Row():
            location = gr.Textbox(label="Location", placeholder="e.g. Glückslott, Costas Piratas")
            role = gr.Textbox(label="Role / Type", placeholder="e.g. merchant, guard captain, spy")
        traits = gr.Textbox(label="Extra traits (optional)", placeholder="e.g. nervous, hides a scar, fond of birds")
        generate_btn = gr.Button("Generate NPC", variant="primary")
        output = gr.Markdown()

        generate_btn.click(fn=generate_npc, inputs=[location, role, traits], outputs=output)

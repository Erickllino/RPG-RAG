import gradio as gr
from agent.src.llm.client import infer_model

SYSTEM_PROMPT = (
    "You are a creative RPG game master assistant for the Ekalia campaign. "
    "Generate detailed, engaging quests that fit the world's tone. "
    "Include a title, hook, objective, key NPCs, obstacles, and a reward. "
    "Write in English unless asked otherwise."
)


def generate_quest(location: str, context: str, quest_type: str):
    if not location and not context:
        return "Fill in at least a location or context."

    prompt_parts = ["Generate a quest"]
    if quest_type:
        prompt_parts.append(f"of type '{quest_type}'")
    if location:
        prompt_parts.append(f"set in {location}")
    if context:
        prompt_parts.append(f"with this context: {context}")
    prompt = " ".join(prompt_parts) + "."

    content, _ = infer_model(prompt, messages=[{"role": "system", "content": SYSTEM_PROMPT}])
    return content


def create_tab():
    with gr.Tab("Quest Generator"):
        gr.Markdown("## Quest Generator\n> Generate missions and quests grounded in your lore.")
        with gr.Row():
            location = gr.Textbox(label="Location", placeholder="e.g. Terras Vivas, a pirate port")
            quest_type = gr.Dropdown(
                label="Type",
                choices=["Fetch", "Escort", "Investigation", "Heist", "Rescue", "Exploration", "Political"],
                value=None,
                allow_custom_value=True,
            )
        context = gr.Textbox(
            label="Context / Party situation",
            placeholder="e.g. The party just arrived at the city and needs gold",
            lines=2,
        )
        generate_btn = gr.Button("Generate Quest", variant="primary")
        output = gr.Markdown()

        generate_btn.click(fn=generate_quest, inputs=[location, context, quest_type], outputs=output)

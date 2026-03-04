# ponta de entrada do gradio


import gradio as gr

def my_function(user_input):
    return "You said: " + user_input

demo = gr.Interface(
    fn=my_function,       # the function to call
    inputs="text",        # what the user types
    outputs="text",       # what gets shown back
)

demo.launch()
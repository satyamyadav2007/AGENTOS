import gradio as gr
import requests

# ............. CONFIG .............
BACKEND_URL = "http://127.0.0.1:8000/run"

def greet(name):
    return "Hello " + name + "!!"

# Gradio Setup
demo = gr.Interface(
    fn=greet, 
    inputs=gr.Textbox(label="Apna naam enter karein"), 
    outputs=gr.Textbox(label="Result"),
    title="🤖 AgentOS"
)

if __name__ == "__main__":
    demo.launch(share=True)
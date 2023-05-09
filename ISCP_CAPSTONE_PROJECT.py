# Author : SIVA S K, AP21110010068

# import openai
import os
import json
import gradio as gr

from huggingface_hub.inference_api import InferenceApi
API_TOKEN = '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'
inference = InferenceApi(repo_id="microsoft/DialoGPT-medium", token=API_TOKEN)


os.remove('history.json')


def add_text(history, text):
    history = history + [(text, None)]
    return history, ""

def add_file(history, file):
    history = history + [((file.name,), None)]
    return history

def bot(history):
    print(history)
    print(history[-1][0])
    response = inference(history[-1][0])
    print(str(response))
    global outfile
    outfile = open("history.json","a")
    data = json.dumps(response,indent=6)
    print(data)
    outfile.write(data)
    if response['conversation']['past_user_inputs'][0] == "exit":

        outfile.close()
        print("Exiting")
        demo.close()
        exit()
    try:
        history[-1][1] = response['generated_text']
    except:
        history[-1][1] = "error occured! "+response['error']

    return history

with gr.Blocks() as demo:
    chatbot = gr.Chatbot([], elem_id="chatbot").style(height=750)

    with gr.Row():
        with gr.Column(scale=0.85):
            txt = gr.Textbox(
                show_label=False,
                placeholder="Enter text and press enter, or upload an image",
            ).style(container=False)
        with gr.Column(scale=0.15, min_width=0):
            btn = gr.UploadButton("📁", file_types=["image", "video", "audio"])


    txt.submit(add_text, [chatbot, txt], [chatbot, txt]).then(
            bot, chatbot, chatbot
    )
    btn.upload(add_file, [chatbot, btn], [chatbot]).then(
            bot, chatbot, chatbot
    )

demo.launch()


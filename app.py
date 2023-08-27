# %%
import os
import gradio as gr


# %%
from EdgeGPT.EdgeUtils import Query, Cookie
import asyncio, json
from pathlib import Path
from rich.pretty import pprint
from EdgeGPT.EdgeGPT import Chatbot, ConversationStyle

Cookie.dir_path = Path(r"./bing_cookies/")
pprint(Cookie.files())


bot: Chatbot = Chatbot(cookies=json.loads(Cookie.files()[0].read_text()))

# %%
def chatgpt_clone(input, history):
    history = history or []
    output = asyncio.run(bot.ask(
        input, conversation_style=ConversationStyle.creative, simplify_response=True))
    pprint(output)
    history.append((input, output["text"]))
    return history, history

# %%
block = gr.Blocks()
prompt = ""
# %%
with block:
    gr.Markdown(
    """<h1><center>Build Your Own Idiot</center></h1>
    """
    )
    chatbot = gr.Chatbot()
    message = gr.Textbox(placeholder=prompt)
    state = gr.State()
    submit = gr.Button("SEND")
    submit.click(chatgpt_clone, inputs=[message, state], outputs=[chatbot, state])

# %%
block.close()
block.launch(debug=True)



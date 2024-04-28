import os
import shutil

from app_modules.overwrites import postprocess
from app_modules.presets import *
from clc.langchain_application import LangChainApplication

class LangChainCFG:
    llm_model_name = '/data2/share/Qwen1.5-7B-chat' 
    n_gpus=1


config = LangChainCFG()
application = LangChainApplication(config)

def get_file_list():
    if not os.path.exists("docs"):
        return []
    return [f for f in os.listdir("docs")]


def clear_session():
    return '', None


def predict(input,
            large_language_model,
            history=None):
    print("******************input",input)
    print("******************history",history)
    if history == None:
        history = []
        application.llm_service.set_history(history)

    search_text = ''
    result = application.get_llm_answer(query=input)
    # 下面的代码上传微调模型后再打开
    # application.llm_service.load_model(config.llm_model_name ,large_language_model)
    history.append((input, result))
    return '', history, history, search_text

with open("assets/custom.css", "r", encoding="utf-8") as f:
    customCSS = f.read()
with gr.Blocks(css=customCSS, theme=small_and_beautiful_theme) as demo:
    gr.Markdown("""<h1><center> 中医LLM问答 (Group_14)</center></h1>
        <center><font size=3>
        </center></font>
        """)
    state = gr.State()


    with gr.Column():
        # with gr.Column():
        with gr.Row():
            large_language_model = gr.Dropdown(
                [
                    "Qwen1.5-7B-chat",
                    "Qwen1.5-7B-chatMed"
                ],
                label="large language model",
                value="Qwen1.5-7B-chat")
            
        with gr.Column(scale=2):
            with gr.Row():
                chatbot = gr.Chatbot(label="对话history", height=800)
            with gr.Row():
                message = gr.Textbox(label='请输入问题')
            with gr.Row():
                clear_history = gr.Button("清除历史对话")
                send = gr.Button("发送")
            with gr.Row():
                gr.Markdown("""提醒：<br>
                                        有任何使用问题[Github Issue区](https://github.com/rui23/LLM-Project)进行反馈. <br>
                                        """)

       

        # 发送按钮 提交
        send.click(predict,
                   inputs=[
                       message,
                       large_language_model,
                       state
                   ],
                   outputs=[message, chatbot, state])

        # 清空历史对话按钮 提交
        clear_history.click(fn=clear_session,
                            inputs=[],
                            outputs=[chatbot, state],
                            queue=False)

        # 输入框 回车
        message.submit(predict,
                       inputs=[
                           message,
                           large_language_model,
                           state
                       ],
                       outputs=[message, chatbot, state])

demo.queue().launch(
    server_name='0.0.0.0',
    server_port=8888,
    share=False,
    # share=True,
    show_error=True,
    debug=True,
    # enable_queue=True,
    inbrowser=True,
)

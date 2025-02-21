# import gradio as gr
# from chatbot.chatbot_backend import ChatBot
# from utils.ui_settings import UISettings
# from agent_graph.db_schema_extractor import save_schema_to_file

# with gr.Blocks() as demo:
#     with gr.Tabs():
#         with gr.TabItem("DETER Amazônia - Agouti Robot"):
#             # First ROW
#             with gr.Row() as row_one:
#                 chatbot = gr.Chatbot(
#                     [],
#                     value="Agouti Robot",
#                     elem_id="chatbot",
#                     bubble_full_width=False,
#                     height=500,
#                     avatar_images=(
#                         ("images/logo_deter_amazonia.jpg"), "images/agouti_logo.png"),
#                 )
#                 chatbot.like(UISettings.feedback, None, None)
#             # SECOND ROW
#             with gr.Row():
#                 input_txt = gr.Textbox(
#                     lines=3,
#                     scale=8,
#                     placeholder="Digite um texto e pressione ENTER, ou envie um PDF",
#                     container=False,
#                 )
#             # Third ROW
#             with gr.Row() as row_two:
#                 text_submit_btn = gr.Button(value="Enviar texto")
#                 clear_button = gr.ClearButton([input_txt, chatbot], value="Limpar texto")
#                 upload_button = gr.UploadButton(label="Upload PDF") # Falta implementar as funções
#             # Process
#             txt_msg = input_txt.submit(fn=ChatBot.respond,
#                                        inputs=[chatbot, input_txt],
#                                        outputs=[input_txt,
#                                                 chatbot],
#                                        queue=False).then(lambda: gr.Textbox(interactive=True),
#                                                          None, [input_txt], queue=False)

#             txt_msg = text_submit_btn.click(fn=ChatBot.respond,
#                                             inputs=[chatbot, input_txt],
#                                             outputs=[input_txt,
#                                                      chatbot],
#                                             queue=False).then(lambda: gr.Textbox(interactive=True),
#                                                               None, [input_txt], queue=False)

# # Salvar o esquema do banco em arquivo JSON ao iniciar o app
# print("Extraindo e salvando esquema do banco de dados...")
# save_schema_to_file()
# print("Esquema salvo em src/memory/db_schema.json")

# if __name__ == "__main__":
#     demo.launch(share=True)

import gradio as gr
from chatbot.chatbot_backend import ChatBot
from utils.ui_settings import UISettings
from agent_graph.db_schema_extractor import save_schema_to_file

with gr.Blocks() as demo:
    with gr.Tabs():
        with gr.TabItem("DETER Amazônia - Agouti Robot"):
            # First ROW
            with gr.Row() as row_one:
                chatbot = gr.Chatbot(
                    [],
                    value="Agouti Robot",
                    elem_id="chatbot",
                    bubble_full_width=False,
                    height=500,
                    avatar_images=(
                        ("images/logo_deter_amazonia.jpg"), "images/agouti_logo.png"),
                )
                chatbot.like(UISettings.feedback, None, None)

            # SECOND ROW
            with gr.Row():
                input_txt = gr.Textbox(
                    lines=3,
                    scale=8,
                    placeholder="Digite um texto e pressione ENTER, ou envie um PDF",
                    container=False,
                )

            # THIRD ROW
            with gr.Row() as row_two:
                text_submit_btn = gr.Button(value="Enviar texto")
                clear_button = gr.ClearButton([input_txt, chatbot], value="Limpar texto")
                upload_button = gr.UploadButton(label="Upload PDF")  # Falta implementar as funções

            # Processar envio ao pressionar ENTER
            input_txt.submit(
                fn=ChatBot.respond,
                inputs=[chatbot, input_txt],
                outputs=[input_txt, chatbot],
                queue=False
            ).then(lambda: gr.Textbox(interactive=True), None, [input_txt], queue=False)

            # Processar envio pelo botão
            text_submit_btn.click(
                fn=ChatBot.respond,
                inputs=[chatbot, input_txt],
                outputs=[input_txt, chatbot],
                queue=False
            ).then(lambda: gr.Textbox(interactive=True), None, [input_txt], queue=False)

# Salvar o esquema do banco em arquivo JSON ao iniciar o app
print("Extraindo e salvando esquema do banco de dados...")
save_schema_to_file()
print("Esquema salvo em memory/db_schema.json")

if __name__ == "__main__":
    demo.launch(share=True)

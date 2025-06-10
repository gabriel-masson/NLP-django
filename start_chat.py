from Chat import Chat
import gradio as gr
import os
from pathlib import Path

chat = Chat()

# Função para adaptar ao novo formato do Gradio (role-based messages)


def responder_gradio(mensagem, historico):
    resposta = chat.answer(mensagem)
    historico = [{"role": "user", "content": mensagem}, {
        "role": "assistant", "content": resposta}]
    return historico


# Interface atualizada
chat_interface = gr.ChatInterface(
    fn=responder_gradio,
    title="Chatbot",
    chatbot=gr.Chatbot(type="messages"),  # Usa o novo formato com dicionários
    textbox=gr.Textbox(placeholder="Digite sua pergunta...", container=True),
    examples=["O que são as arboviroses", "Quais são os sintomas da Chukungunya?",
              "Me explique como evitar a dengue"],
)

chat_interface.launch()

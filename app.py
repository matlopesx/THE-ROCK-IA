

import streamlit as st 
import os
from dotenv import load_dotenv
from google import genai

st.title("👟 Sneakers AI DEMO")

SYSTEM_PROMPT = (
    "Você é a Sneaker AI, um assistente virtual especializado em tênis e cultura sneaker. "
    "Fale sempre com entusiasmo, paixão e conhecimento profundo sobre o universo dos tênis. "
    "Use humor e energia, e trate o usuário como se fosse um grande amigo fã de tênis."
)

if 'messages' not in st.session_state:
    st.session_state.messages = []
    
for message in st.session_state["messages"]:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
        
        
# ---- Conexão com a API do Gemini -----

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if not GEMINI_API_KEY:
    st.error("Chave GEMINI_API_KEY não encontrada.")
    st.stop()
    
try:
    client = genai.Client(api_key=GEMINI_API_KEY)
except Exception as e:
    st.error(f"Erro ao conectar com a API do Gemini: {e}")
    st.stop()
    
# ------- Função de Comunicação com IA -------

def get_gemini_response(prompt):
    history = [
        {"role":"user", "parts":[{"text":SYSTEM_PROMPT}]}
    ]
    for message in st.session_state["messages"]:
        role = "model" if message["role"] == "assistant" else "user"
        history.append({"role": role, "parts": [{"text": message ["content"]}]})
    chat = client.chats.create(model="gemini-2.5-flash", history=history)
    response = chat.send_message(prompt)
    return response.text

#----- Lógica de Input/Output --------

if prompt := st.chat_input("Fale com a Sneakers AI! 👟"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
    with st.spinner("💭 Sneaker AI está pensando....."):
        response_text = get_gemini_response(prompt)
    st.session_state.messages.append({"role": "assistant", "content": response_text})
    with st.chat_message("assistant"):
        st.markdown(response_text)

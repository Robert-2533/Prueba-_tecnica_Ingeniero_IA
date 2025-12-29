import logging
import os

import requests
import streamlit as st

logger = logging.getLogger("uvicorn")

AGENT_API_URL = os.environ.get("AGENT_API_URL")
logger.info(f"AGENT_API_URL: {AGENT_API_URL}")
# Configuración de la página
st.set_page_config(page_title="Manejador de eventos", page_icon="🤖")
st.title("📅 Gestor de Agenda")

logger.info("UI started")
# 1. Inicializar el historial de chat en la sesión
if "messages" not in st.session_state:
    st.session_state.messages = []


# 2. Función para llamar al pipeline de LangChain (URL)
def call_langchain_pipeline(prompt):
    url = AGENT_API_URL
    payload = {"input": prompt}
    try:
        response = requests.post(url, json=payload)
        response.raise_for_status()
        data = response.json()
        return data.get("message", "No recibí respuesta del servidor.")
    except Exception as e:
        return f"Error de conexión: {str(e)}"


for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("¿En qué puedo ayudarte?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Pensando..."):
            full_response = call_langchain_pipeline(prompt)
            st.markdown(full_response)

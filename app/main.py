import json
from typing import Any
import requests
import streamlit as st
import copy
from config import chatbot_config

########################################################################################################################

api_address = chatbot_config["api_address"]

########################################################################################################################

st.set_page_config(page_title=chatbot_config["page_title"],
                   page_icon=chatbot_config["page_icon"],
                   layout="wide",
                   initial_sidebar_state="auto",
                   menu_items=None)

if "messages" not in st.session_state:
    st.session_state.messages = copy.deepcopy(chatbot_config["messages"])

if "ai_avatar_url" not in st.session_state:
    st.session_state.ai_avatar_url = chatbot_config["ai_avatar_url"]

if "user_avatar_url" not in st.session_state:
    st.session_state.user_avatar_url = chatbot_config["user_avatar_url"]

########################################################################################################################

def is_complete_utf8(data: bytes) -> bool:
    """Verifica se `data` rappresenta una sequenza UTF-8 completa."""
    try:
        data.decode("utf-8")
        return True
    except UnicodeDecodeError:
        return False

def main():
    for message in st.session_state.messages:
        if message["role"] == "user":
            with st.chat_message(message["role"], avatar=st.session_state.user_avatar_url):
                st.markdown(message["content"])
        else:
            with st.chat_message(message["role"], avatar=st.session_state.ai_avatar_url):
                st.markdown(message["content"])

    if prompt := st.chat_input("Say something"):
        st.session_state.messages.append({"role": "user", "content": prompt})

        #####################################################################
        if len(st.session_state.messages) > 10:
            st.session_state.messages = st.session_state.messages[-10:]
        #####################################################################

        with st.chat_message("user", avatar=st.session_state.user_avatar_url):
            st.markdown(prompt)

        with st.chat_message("assistant", avatar=st.session_state.ai_avatar_url):
            message_placeholder = st.empty()
            s = requests.Session()
            full_response = ""
            url = f"{api_address}/agent/stream_events_chain"
            payload = {
                "chain_id": "agent_with_tools_gpt-4",
                "query": {
                    "input": prompt,
                    "chat_history": st.session_state.messages
                },
                "inference_kwargs": {},
            }

            non_decoded_chunk = b''
            with s.post(url, json=payload, headers=None, stream=True) as resp:
                for chunk in resp.iter_content():
                    print(chunk)
                    if chunk:
                        # Aggiungi il chunk alla sequenza da decodificare
                        non_decoded_chunk += chunk

                        # Decodifica solo quando i byte formano una sequenza UTF-8 completa
                        if is_complete_utf8(non_decoded_chunk):
                            decoded_chunk = non_decoded_chunk.decode("utf-8")
                            full_response += decoded_chunk
                            message_placeholder.markdown(full_response + "▌", unsafe_allow_html=True)
                            non_decoded_chunk = b''  # Svuota il buffer

            message_placeholder.markdown(full_response)
        st.session_state.messages.append({"role": "assistant", "content": full_response})

########################################################################################################################

main()

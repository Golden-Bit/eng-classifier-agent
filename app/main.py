import json
import os
import base64
from typing import Any
import requests
import streamlit as st
import copy
from config import chatbot_config
from utilities.tools.mongodb import MongoDBToolKitManager

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


def process_documents(item):
    """
    Processa i documenti all'interno dell'item.
    Se i documenti hanno contenuto base64, decodifica e salva il file permanentemente nella directory 'downloaded_docs'.
    Sostituisce il contenuto base64 con il percorso del file.
    """
    # Crea la directory 'downloaded_docs' se non esiste
    os.makedirs('downloaded_docs', exist_ok=True)

    if 'Documents' in item and isinstance(item['Documents'], list):
        for document in item['Documents']:
            if 'AssociatedFiles' in document and isinstance(document['AssociatedFiles'], list):
                for file in document['AssociatedFiles']:
                    if 'ContentBase64' in file and file['ContentBase64']:
                        # Decodifica il contenuto base64 e salva il file
                        content_base64 = file['ContentBase64']
                        file_name = file['Name']
                        decoded_bytes = base64.b64decode(content_base64)

                        # Sanifica il nome del file per prevenire traversal directory
                        file_name = os.path.basename(file_name)
                        file_path = os.path.abspath(os.path.join('downloaded_docs', file_name))

                        # Salva il file permanentemente
                        with open(file_path, 'wb') as f:
                            f.write(decoded_bytes)

                        # Rimuovi il contenuto base64 e sostituisci con il percorso del file
                        file['ContentBase64'] = file_path
                    else:
                        # Se non c'è contenuto base64, imposta ContentBase64 a None
                        file['ContentBase64'] = None
    return item


def upload_in_mongo(file_content: str, collection_name: str):
    """Carica il contenuto JSON nel MongoDB nella collezione specificata."""
    mongodb_toolkit = MongoDBToolKitManager(
        connection_string="mongodb://localhost:27017",
        default_database="item_classification_db_3",
        default_collection=collection_name,
    )

    # Converti la stringa JSON in un oggetto JSON valido
    data = json.loads(file_content)

    # Se stiamo caricando items, processa i documenti
    if collection_name == "items":
        if isinstance(data, list):
            # Se è una lista di items
            processed_items = []
            for item in data:
                processed_item = process_documents(item)
                processed_items.append(processed_item)
            data = processed_items
        else:
            # Singolo item
            data = process_documents(data)

    # Converti di nuovo a stringa JSON per l'inserimento
    dumped_data = json.dumps(data)

    mongodb_toolkit.write_to_mongo(
        database_name="item_classification_db_3",
        collection_name=collection_name,
        data=dumped_data,
    )


def main():
    # Sidebar per il caricamento dei file
    st.sidebar.title("Carica Dati")
    decisional_tree_file = st.sidebar.file_uploader("Carica Decisional Tree JSON", type="json")
    items_file = st.sidebar.file_uploader("Carica Items JSON", type="json")

    if st.sidebar.button("Carica su MongoDB"):
        if decisional_tree_file is not None:
            file_content = decisional_tree_file.read().decode('utf-8')
            upload_in_mongo(file_content, collection_name="decisional_tree")
            st.sidebar.success("Decisional tree caricato con successo.")

        if items_file is not None:
            file_content = items_file.read().decode('utf-8')
            upload_in_mongo(file_content, collection_name="items")
            st.sidebar.success("Items caricati con successo.")

        if decisional_tree_file is None and items_file is None:
            st.sidebar.warning("Per favore, carica almeno un file prima di cliccare su 'Carica su MongoDB'.")

    # Interfaccia principale della chat
    for message in st.session_state.messages:
        if message["role"] == "user":
            with st.chat_message(message["role"], avatar=st.session_state.user_avatar_url):
                st.markdown(message["content"])
        else:
            with st.chat_message(message["role"], avatar=st.session_state.ai_avatar_url):
                st.markdown(message["content"])

    if prompt := st.chat_input("Scrivi qualcosa"):
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

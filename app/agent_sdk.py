# Definire l'URL dell'API
import json
from typing import List

import requests


def execute_agent(input_query: str, chat_history: List[List[str]] = []):
    api_url = "http://127.0.0.1:8092/agent/stream_events_chain"

    # Definire il payload della richiesta
    payload = {
        "chain_id": "example_chain",
        "query": {
            "input": input_query,
            "chat_history": chat_history
        },
        "inference_kwargs": {}
    }

    # Eseguire la richiesta POST all'API
    try:
        response = requests.post(api_url, json=payload)
        response.raise_for_status()  # Solleva un'eccezione per codici di errore HTTP
        #data = response.json()  # Decodifica la risposta JSON
        data = response.__dict__['_content'].decode()
        print("Risultato dell'API:")
        print(data)
        return data
        #print(json.dumps(data, indent=2))  # Stampa il risultato formattato
    except requests.exceptions.RequestException as e:
        print(f"Errore nella chiamata all'API: {e}")
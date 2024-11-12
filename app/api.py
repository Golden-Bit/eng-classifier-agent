"""
Questo modulo implementa un'API FastAPI per gestire un albero decisionale e una serie di items,
con funzionalità per caricare, eliminare e recuperare i dati dal database MongoDB.
Inoltre, fornisce endpoint per classificare items e impostare attributi,
sebbene la logica sia ancora da implementare.

Struttura del modulo:
- Modelli Pydantic per la validazione degli input.
- Funzioni per processare documenti e BOM (Bill of Materials).
- Funzioni per interagire con MongoDB tramite un toolkit specifico.
- Endpoint per caricare, eliminare e recuperare dati.
- Endpoint placeholder per la classificazione e l'impostazione di attributi.
"""

from fastapi import FastAPI, HTTPException, APIRouter, Query
from pydantic import BaseModel
from typing import List, Dict, Any
import json
import os
import base64
from typing import Any
import requests
import streamlit as st
import copy
from config import chatbot_config
from utilities.tools.mongodb import MongoDBToolKitManager

app = FastAPI()
router = APIRouter()

# Modelli Pydantic per la validazione degli input
class DecisionalTreeContent(BaseModel):
    """
    Modello per il contenuto dell'albero decisionale.

    Attributi:
    - data: Lista di dizionari che rappresentano l'albero decisionale.
    """
    data: List[Dict[str, Any]]  # L'albero decisionale è una lista di dizionari

class ItemsContent(BaseModel):
    """
    Modello per il contenuto degli items.

    Attributi:
    - data: Lista di dizionari che rappresentano gli items.
    """
    data: List[Dict[str, Any]]  # Gli items sono anche una lista di dizionari

class HistoryItem(BaseModel):
    """
    Modello per un singolo elemento della cronologia.

    Attributi:
    - nodeClassId: Identificatore del nodo di classificazione.
    - description: Descrizione associata al nodo.
    """
    nodeClassId: str
    description: str

class ClassificationRequest(BaseModel):
    """
    Modello per una richiesta di classificazione di un item.

    Attributi:
    - idOggetto: Identificatore dell'oggetto da classificare.
    - nodiClassificazione: Lista di nodi di classificazione.
    - history: Lista di elementi di cronologia (HistoryItem).
    """
    idOggetto: str
    nodiClassificazione: List[str]
    history: List[HistoryItem]

class SetAttributesRequest(BaseModel):
    """
    Modello per una richiesta di impostazione degli attributi di un item.

    Attributi:
    - idOggetto: Identificatore dell'oggetto.
    - idNodo: Identificatore del nodo.
    - history: Lista di elementi di cronologia (HistoryItem).
    """
    idOggetto: str
    idNodo: str
    history: List[HistoryItem]

########################################################################################################################

api_address = chatbot_config["api_address"]

def is_complete_utf8(data: bytes) -> bool:
    """
    Verifica se `data` rappresenta una sequenza UTF-8 completa.

    Parametri:
    - data: Bytes da verificare.

    Ritorna:
    - bool: True se la sequenza è completa, False altrimenti.
    """
    try:
        data.decode("utf-8")
        return True
    except UnicodeDecodeError:
        return False

def process_documents(item):
    """
    Processa i documenti all'interno dell'item.

    Se i documenti hanno contenuto base64, decodifica e salva il file permanentemente
    nella directory 'downloaded_docs'. Sostituisce il contenuto base64 con il percorso del file.

    Parametri:
    - item: Dizionario che rappresenta l'item.

    Ritorna:
    - item: Dizionario aggiornato con i percorsi dei file al posto del contenuto base64.
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

def process_bom(item):
    """
    Processa la BOM (Bill of Materials) dell'item per sostituirla con informazioni generali.

    Calcola la profondità massima e il numero totale di componenti nella BOM,
    e sostituisce la BOM originale con queste informazioni.

    Parametri:
    - item: Dizionario che rappresenta l'item.

    Ritorna:
    - item: Dizionario aggiornato con il sommario della BOM.
    """
    if 'BOM' in item and item['BOM']:
        bom = item['BOM']
        # Calcola informazioni generali sulla BOM
        max_depth = calculate_max_depth(bom)
        total_components = count_total_components(bom)
        # Crea un nuovo dizionario con le informazioni generali
        bom_summary = {
            'MaxDepth': max_depth,
            'TotalComponents': total_components
        }
        # Sostituisci la BOM originale con il sommario
        item['BOM'] = bom_summary
    return item

def calculate_max_depth(bom_component, current_depth=1):
    """
    Calcola la profondità massima della BOM ricorsivamente.

    Parametri:
    - bom_component: Dizionario che rappresenta il componente corrente della BOM.
    - current_depth: Profondità corrente nel calcolo (default=1).

    Ritorna:
    - int: Profondità massima trovata nella BOM.
    """
    if 'ChildComponents' in bom_component and bom_component['ChildComponents']:
        depths = [calculate_max_depth(child, current_depth + 1) for child in bom_component['ChildComponents']]
        return max(depths)
    else:
        return current_depth

def count_total_components(bom_component):
    """
    Conta il numero totale di componenti nella BOM ricorsivamente.

    Parametri:
    - bom_component: Dizionario che rappresenta il componente corrente della BOM.

    Ritorna:
    - int: Numero totale di componenti nella BOM.
    """
    total = 1  # Conta il componente corrente
    if 'ChildComponents' in bom_component and bom_component['ChildComponents']:
        for child in bom_component['ChildComponents']:
            total += count_total_components(child)
    return total

def upload_in_mongo(file_content: str, collection_name: str):
    """
    Carica il contenuto JSON nel MongoDB nella collezione specificata.

    Se stiamo caricando items, processa i documenti e la BOM.

    Parametri:
    - file_content: Stringa JSON del contenuto da caricare.
    - collection_name: Nome della collezione MongoDB.

    Effetti Collaterali:
    - Scrive i dati nel database MongoDB.
    """
    mongodb_toolkit = MongoDBToolKitManager(
        connection_string="mongodb://localhost:27017",
        default_database="item_classification_db_3",
        default_collection=collection_name,
    )

    # Converti la stringa JSON in un oggetto JSON valido
    data = json.loads(file_content)

    # Se stiamo caricando items, processa i documenti e la BOM
    if collection_name == "items":
        if isinstance(data, list):
            # Se è una lista di items
            processed_items = []
            for item in data:
                processed_item = process_documents(item)
                processed_item = process_bom(processed_item)
                processed_items.append(processed_item)
            data = processed_items
        else:
            # Singolo item
            data = process_documents(data)
            data = process_bom(data)

    # Converti di nuovo a stringa JSON per l'inserimento
    dumped_data = json.dumps(data)

    mongodb_toolkit.write_to_mongo(
        database_name="item_classification_db_3",
        collection_name=collection_name,
        data=dumped_data,
    )

def delete_all_documents(collection_name: str):
    """
    Elimina tutti i documenti dalla collezione specificata nel database 'item_classification_db_3'.

    Parametri:
    - collection_name: Nome della collezione da svuotare.

    Effetti Collaterali:
    - Rimuove tutti i documenti dalla collezione specificata.
    - Visualizza un messaggio di successo nella sidebar di Streamlit.
    """
    mongodb_toolkit = MongoDBToolKitManager(
        connection_string="mongodb://localhost:27017",
        default_database="item_classification_db_3",
        default_collection=collection_name,
    )

    # Usa una query vuota per eliminare tutti i documenti
    mongodb_toolkit.delete_from_mongo(
        database_name="item_classification_db_3",
        collection_name=collection_name,
        query="{}"
    )
    st.sidebar.success(f"Tutti gli elementi nella collezione '{collection_name}' sono stati eliminati.")

# Endpoint per caricare l'albero decisionale
@router.post("/aieng/classification/item/upload_decisional_tree")
async def upload_decisional_tree(request: DecisionalTreeContent):
    """
    Endpoint per caricare un albero decisionale nel database.

    Parametri:
    - request: Oggetto DecisionalTreeContent contenente i dati dell'albero.

    Ritorna:
    - dict: Messaggio di conferma dell'avvenuto caricamento.

    Eccezioni:
    - HTTPException 400: Se non viene fornito alcun contenuto.
    """
    decisional_tree_content = request.data

    if decisional_tree_content:
        # Elimina i documenti esistenti e carica i nuovi dati
        delete_all_documents("decisional_tree")
        upload_in_mongo(json.dumps(decisional_tree_content, indent=2), collection_name="decisional_tree")
        print("Decisional tree uploaded successfully.")
        return {"message": "Decisional tree uploaded successfully."}
    else:
        raise HTTPException(status_code=400, detail="No decisional tree content provided.")

# Endpoint per caricare gli items
@router.post("/aieng/classification/item/upload_items")
async def upload_items(request: ItemsContent):
    """
    Endpoint per caricare items nel database.

    Parametri:
    - request: Oggetto ItemsContent contenente i dati degli items.

    Ritorna:
    - dict: Messaggio di conferma dell'avvenuto caricamento.

    Eccezioni:
    - HTTPException 400: Se non viene fornito alcun contenuto.
    """
    items_content = request.data

    if items_content:
        # Elimina i documenti esistenti e carica i nuovi dati
        delete_all_documents("items")
        upload_in_mongo(json.dumps(items_content, indent=2), collection_name="items")
        print("Items uploaded successfully.")
        return {"message": "Items uploaded successfully."}
    else:
        raise HTTPException(status_code=400, detail="No items content provided.")

# Endpoint per recuperare il contenuto di una collezione
@router.get("/aieng/classification/item/get_collection_contents")
async def get_collection_contents(
    collection_name: str = Query(..., description="Nome della collezione da recuperare"),
    query: str = Query("{}", description="Filtro opzionale per la query MongoDB come stringa JSON")
):
    """
    Recupera il contenuto della collezione specificata, applicando un filtro opzionale.

    Parametri:
    - collection_name: Nome della collezione ('decisional_tree' o 'items').
    - query: Stringa JSON rappresentante il filtro della query MongoDB.

    Ritorna:
    - List[Dict[str, Any]]: Lista di documenti dalla collezione.

    Eccezioni:
    - HTTPException 400: Se il nome della collezione non è permesso o la query non è valida.
    - HTTPException 500: Se c'è un errore nel recupero dei dati.
    """
    # Valida il nome della collezione
    allowed_collections = ["decisional_tree", "items"]
    if collection_name not in allowed_collections:
        raise HTTPException(status_code=400, detail=f"Collection '{collection_name}' is not allowed.")

    try:
        # Parsea la stringa di query in un dizionario
        query_dict = json.loads(query)
    except json.JSONDecodeError as e:
        raise HTTPException(status_code=400, detail=f"Invalid query JSON: {e}")

    mongodb_toolkit = MongoDBToolKitManager(
        connection_string="mongodb://localhost:27017",
        default_database="item_classification_db_3",
        default_collection=collection_name,
    )

    try:
        data = mongodb_toolkit.read_from_mongo(
            database_name="item_classification_db_3",
            collection_name=collection_name,
            query=query,
            output_format="object"
        )
        # Converti ObjectId in stringa se necessario
        for doc in data:
            if '_id' in doc:
                doc['_id'] = str(doc['_id'])
        return data
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to retrieve data from collection '{collection_name}': {e}")

# Endpoint per classificare un item (logica da implementare)
@router.post("/aieng/classification/item/classify")
async def classify_item(request: ClassificationRequest):
    """
    Endpoint per classificare un item in base ai dati forniti.

    Parametri:
    - request: Oggetto ClassificationRequest contenente i dati per la classificazione.

    Ritorna:
    - List[Dict[str, Any]]: Lista di risultati di classificazione (placeholder).

    Note:
    - La logica di classificazione è ancora da implementare.
    """
    # Placeholder logic; la logica reale deve essere implementata
    return [
        {
            "idNodo": "id1",
            "score": 0.6,
            "reason": "bla bla bla"
        },
        {
            "idNodo": "id2",
            "score": 0.3,
            "reason": "bla bla bla"
        },
        {
            "idNodo": "id3",
            "score": 0.1,
            "reason": "bla bla bla"
        }
    ]

# Endpoint per impostare attributi di un item (logica da implementare)
@router.post("/aieng/classification/item/attributes")
async def set_attributes(request: SetAttributesRequest):
    """
    Endpoint per impostare gli attributi di un item in base ai dati forniti.

    Parametri:
    - request: Oggetto SetAttributesRequest contenente i dati per impostare gli attributi.

    Ritorna:
    - dict: Dizionario contenente gli attributi valorizzati (placeholder).

    Note:
    - La logica per impostare gli attributi è ancora da implementare.
    """
    # Placeholder logic; la logica reale deve essere implementata
    return {
        "attributiValorizzati": [
            {
                "nomeAttributo": "nome1",
                "valore": "valore1",
            },
            {
                "nomeAttributo": "nome2",
                "valore": "valore2",
            }
        ]
    }

# Includi il router nell'app FastAPI
app.include_router(router)

if __name__ == "__main__":
    import uvicorn

    # Avvia l'applicazione FastAPI su localhost alla porta 8091
    uvicorn.run(app, host="0.0.0.0", port=8091)

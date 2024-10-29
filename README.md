# Documento di Progetto per la Progettazione Logica di un Agente Multi-Strumento Basato su LLM per la Classificazione di Item

## Indice

1. [Introduzione](#1-introduzione)
2. [Obiettivi del Progetto](#2-obiettivi-del-progetto)
3. [Architettura del Sistema](#3-architettura-del-sistema)
    - [3.1. Componenti Principali](#31-componenti-principali)
    - [3.2. Flusso di Lavoro Generale](#32-flusso-di-lavoro-generale)
4. [Implementazione Pratica](#4-implementazione-pratica)
    - [4.1. Prerequisiti](#41-prerequisiti)
    - [4.2. Configurazione del Progetto](#42-configurazione-del-progetto)
    - [4.3. Configurazione di MongoDB](#43-configurazione-di-mongodb)
    - [4.4. Avvio del Backend (API)](#44-avvio-del-backend-api)
    - [4.5. Configurazione e Avvio dell'Agente](#45-configurazione-e-avvio-dellagente)
    - [4.6. Avvio dell'Interfaccia Utente (UI) con Streamlit](#46-avvio-dellinterfaccia-utente-ui-con-streamlit)
    - [4.7. Utilizzo](#47-utilizzo)
5. [Strutture Dati](#5-strutture-dati)
    - [5.1. Schema JSON degli Item](#51-schema-json-degli-item)
    - [5.2. Schema dei Nodi dell'Albero Decisionale](#52-schema-dei-nodi-dellalbero-decisionale)
6. [Utilizzo degli Strumenti di Interazione con MongoDB](#6-utilizzo-degli-strumenti-di-interazione-con-mongodb)
    - [6.1. `write_to_mongo`](#61-writetomongo)
    - [6.2. `read_from_mongo`](#62-readfrommongo)
    - [6.3. `delete_from_mongo`](#63-deletefrommongo)
    - [6.4. `update_in_mongo`](#64-updateinmongo)
7. [Esecuzione delle Regole e Output JSON](#7-esecuzione-delle-regole-e-output-json)
    - [7.1. Formato dell'Output JSON](#71-formato-delloutput-json)
    - [7.2. Applicazione delle Regole tramite LLM](#72-applicazione-delle-regole-tramite-llm)
    - [7.3. Navigazione nell'Albero Decisionale](#73-navigazione-nellalbero-decisionale)
8. [Output Attesi](#8-output-attesi)
    - [8.1. Risultato della Classificazione](#81-risultato-della-classificazione)
    - [8.2. Giustificazione delle Scelte](#82-giustificazione-delle-scelte)
9. [Troubleshooting](#9-troubleshooting)
10. [Conclusione](#10-conclusione)
11. [Prossimi Passi](#11-prossimi-passi)

---

## 1. Introduzione

Questo documento descrive l'implementazione pratica di un sistema basato su Large Language Model (LLM) utilizzando LangChain. Il sistema prevede un agente multi-strumento in grado di classificare oggetti denominati *item* secondo uno schema di regole applicate a un albero decisionale. Gli *item* seguono uno schema JSON dettagliato, e l'agente naviga tra i nodi dell'albero, applicando le regole di classificazione e restituendo sia il risultato che una giustificazione delle scelte effettuate. I dati sono gestiti tramite un database MongoDB, e l'interfaccia utente è realizzata con Streamlit.

## 2. Obiettivi del Progetto

- **Sviluppare un agente intelligente** capace di classificare gli *item* secondo regole definite.
- **Integrare un LLM tramite LangChain** per l'applicazione iniziale delle regole, con output strutturato in JSON.
- **Permettere l'espansione futura** verso l'uso di algoritmi esperti per l'esecuzione delle regole.
- **Fornire strumenti all'agente** per navigare efficientemente nei campi JSON, eseguire codice Python e manipolare file.
- **Garantire un output dettagliato**, includendo sia la classificazione risultante che la giustificazione delle decisioni prese, in formato JSON strutturato.

## 3. Architettura del Sistema

### 3.1. Componenti Principali

- **Agente LLM Multi-Strumento**: Il cuore del sistema, responsabile dell'elaborazione e della classificazione degli *item*.
- **Interfaccia LangChain**: Utilizzata per interagire con il modello LLM e orchestrare le operazioni dell'agente.
- **Albero Decisionale**: Struttura che definisce i nodi, le regole e le relazioni per la classificazione.
- **Database degli Item (MongoDB)**: Collezione di *item* da classificare, conformi allo schema JSON fornito.
- **Backend API (FastAPI)**: Gestisce le richieste di classificazione e interagisce con l'agente.
- **Interfaccia Utente (Streamlit)**: Frontend per interagire con l'agente, inviare *item* e visualizzare i risultati.

### 3.2. Flusso di Lavoro Generale

1. **Input dell'Item**: L'utente fornisce un *item* tramite l'interfaccia Streamlit.
2. **Salvataggio dell'Item**: L'item viene salvato nella collezione `items` di MongoDB utilizzando lo strumento `write_to_mongo`.
3. **Invio alla API**: L'interfaccia Streamlit invia una richiesta di classificazione alla API FastAPI.
4. **Classificazione tramite Agente**:
    - L'agente carica l'albero decisionale dalla collezione `decisional_tree_v2`.
    - Naviga attraverso i nodi dell'albero applicando le regole.
    - Utilizza LLM per applicare le regole e genera un output JSON strutturato.
5. **Salvataggio dei Risultati**: I risultati della classificazione vengono salvati nella collezione `classification_results_{ID}`.
6. **Visualizzazione dei Risultati**: L'interfaccia Streamlit visualizza i risultati e le giustificazioni all'utente.

## 4. Implementazione Pratica

### 4.1. Prerequisiti

- **Ambiente Python**: Versione 3.8 o superiore.
- **MongoDB**: Installato e in esecuzione.
- **FastAPI**: Framework per la creazione del backend API.
- **Streamlit**: Framework per la creazione dell'interfaccia utente.
- **LangChain**: Libreria per l'integrazione con LLM.
- **Altri pacchetti Python**: Vedi `requirements.txt`.

### 4.2. Configurazione del Progetto

1. **Clonare il Repository**

    ```bash
    git clone https://github.com/tuo-username/tuo-progetto.git
    cd tuo-progetto
    ```

2. **Creare e Attivare un Ambiente Virtuale**

    ```bash
    python3 -m venv venv
    source venv/bin/activate  # Su Windows: venv\Scripts\activate
    ```

3. **Installare le Dipendenze**

    ```bash
    pip install -r requirements.txt
    ```

4. **Configurare le Variabili d'Ambiente**

    Crea un file `.env` nella radice del progetto e aggiungi le seguenti variabili:

    ```env
    API_KEY=tuo_api_key_openai
    API_ADDRESS=http://127.0.0.1:8100
    ```

### 4.3. Configurazione di MongoDB

1. **Avviare MongoDB**

    Assicurati che MongoDB sia in esecuzione. Puoi avviarlo tramite:

    ```bash
    mongod --dbpath /percorso/al/tuo/db
    ```

2. **Creare il Database e le Collezioni**

    Puoi utilizzare la shell `mongo` o un client come MongoDB Compass per creare il database `item_classification_db` e le collezioni `items` e `decisional_tree_v2`.

### 4.4. Avvio del Backend (API)

1. **Navigare nella Cartella del Backend**

    ```bash
    cd backend
    ```

2. **Avviare il Server FastAPI**

    ```bash
    uvicorn agent_api:app --host 0.0.0.0 --port 8100
    ```

    Il server sarà accessibile all'indirizzo `http://127.0.0.1:8100`.

### 4.5. Configurazione e Avvio dell'Agente

1. **Navigare nella Cartella dell'Agente**

    ```bash
    cd agent
    ```

2. **Verificare e Configurare lo Script `agent_getter.py`**

    Assicurati che il file `agent_getter.py` sia configurato correttamente con le informazioni necessarie per connettersi a MongoDB e all'LLM. Verifica che l'URL di MongoDB e le credenziali dell'API OpenAI siano corretti.

3. **Avviare l'Agente**

    ```bash
    python agent_getter.py
    ```

    Questo script inizializza l'agente con i tool necessari per interagire con MongoDB e l'LLM.

### 4.6. Avvio dell'Interfaccia Utente (UI) con Streamlit

1. **Navigare nella Cartella della UI**

    ```bash
    cd ui
    ```

2. **Avviare l'Applicazione Streamlit**

    ```bash
    streamlit run main.py
    ```

    L'interfaccia utente sarà accessibile all'indirizzo indicato nel terminale, solitamente `http://localhost:8501`.

### 4.7. Utilizzo

Una volta avviati tutti i componenti, segui questi passaggi per utilizzare il sistema:

1. **Aprire l'Interfaccia Utente**

    Apri il tuo browser e naviga all'indirizzo `http://localhost:8501` per accedere all'interfaccia Streamlit.

2. **Inserire un Item da Classificare**

    - Nella casella di input della chat, inserisci i dettagli dell'*item* che desideri classificare.
    - Premi invio per inviare l'item all'agente.

3. **Visualizzare i Risultati della Classificazione**

    - L'agente elaborerà l'*item* applicando le regole definite nell'albero decisionale.
    - I risultati della classificazione, insieme alle giustificazioni, saranno visualizzati nell'interfaccia utente.
    - I risultati saranno anche salvati nella collezione `classification_results_{ID}` di MongoDB per futura consultazione.

4. **Monitorare lo Stato del Sistema**

    - Puoi monitorare i log del backend API e dell'agente per verificare il corretto funzionamento e diagnosticare eventuali problemi.
    - Assicurati che tutti i servizi siano in esecuzione senza errori.

## 5. Strutture Dati

### 5.1. Schema JSON degli Item

Gli *item* seguono uno schema JSON dettagliato, che include:

- **Proprietà principali**: `Id`, `ItemId`, `Name`, `Description`, `Revision`, `ObjectType`, `Attributes`, `CreatedDate`, `LastModifiedDate`, `Status`.
- **Attributi personalizzati**: Una lista di attributi definiti dall'utente.
- **Relazioni**: `BOM`, `Forms`, `WhereUsed`, `Documents`.

#### Esempio di Item

```json
{
  "Item": {
    "Id": "12345",
    "ItemId": "A1B2C3",
    "Name": "Modulo Esempio",
    "Description": "Descrizione dettagliata del modulo.",
    "Revision": "1.0",
    "ObjectType": "TypeA",
    "Attributes": [
      {
        "InternalName": "color",
        "DisplayName": "Colore",
        "AttributeType": "String",
        "Value": "Rosso"
      }
    ],
    "CreatedDate": "2024-04-27T12:34:56Z",
    "LastModifiedDate": "2024-04-28T12:34:56Z",
    "Status": "active"
  },
  "BOM": { /* Dettagli della Distinta Base */ },
  "Forms": [ /* Elenco dei moduli associati */ ],
  "WhereUsed": [ /* Elenco degli articoli in cui l'item è utilizzato */ ],
  "Documents": [ /* Elenco dei documenti associati */ ]
}
```

### 5.2. Schema dei Nodi dell'Albero Decisionale

Ogni nodo dell'albero decisionale ha la seguente struttura:

- **ClassId**: Identificatore unico della classe.
- **Name**: Nome della classe.
- **Description**: Descrizione della classe.
- **Rules**: Regole da applicare al nodo.
- **ParentId/ParentClassId/ParentName**: Informazioni sul nodo genitore.
- **Level**: Livello del nodo nell'albero.
- **Attributes**: Attributi rilevanti per la classificazione.
- **EntryRule**: Regola di ingresso al nodo.
- **AttributeValuationRule**: Regole per la valutazione degli attributi.
- **childRef**: Riferimenti ai nodi figli.

#### Esempio di Nodo dell'Albero Decisionale

```json
{
  "ClassId": "MGT0101",
  "Name": "Modulo di Design",
  "Description": "Classe per i moduli di design",
  "Rules": "Regole specifiche per la classe di design",
  "ParentId": null,
  "ParentClassId": null,
  "ParentName": null,
  "Level": 1,
  "Attributes": [
    {
      "Id": "attr1",
      "AttributeId": "color",
      "Name": "Color",
      "KeyLovId": "lov1",
      "OptionValues": [
        { "Key": "red", "Value": "Rosso" },
        { "Key": "blue", "Value": "Blu" }
      ]
    }
  ],
  "EntryRule": "La sottostringa dall'ItemId deve essere '90960'",
  "AttributeValuationRule": [
    "color == 'red'",
    "size > 10"
  ],
  "childRef": ["MGT0102", "MGT0103"]
}
```

## 6. Utilizzo degli Strumenti di Interazione con MongoDB

Nel backend, sono definiti i seguenti strumenti per interagire con il database MongoDB. Questi strumenti sono strutturati utilizzando `StructuredTool` di LangChain e possono essere utilizzati per eseguire operazioni CRUD (Create, Read, Update, Delete).

### 6.1. `write_to_mongo`

- **Descrizione**: Inserisce dati nella collection specificata o in quella di default.
- **Parametri Richiesti**:
  - `database_name`: Nome del database.
  - `collection_name`: Nome della collection.
  - `data`: Stringa JSON dei dati da inserire.

#### Esempio di Utilizzo

```plaintext
Utilizza lo strumento `write_to_mongo` con i seguenti parametri:
- database_name: "item_classification_db"
- collection_name: "items"
- data: {
    "Item": {
        "Id": "12345",
        "ItemId": "A1B2C3",
        "Name": "Modulo Esempio",
        "Description": "Descrizione dettagliata del modulo.",
        "Revision": "1.0",
        "ObjectType": "TypeA",
        "Attributes": [
            {
                "InternalName": "color",
                "DisplayName": "Colore",
                "AttributeType": "String",
                "Value": "Rosso"
            }
        ],
        "CreatedDate": "2024-04-27T12:34:56Z",
        "LastModifiedDate": "2024-04-28T12:34:56Z",
        "Status": "active"
    },
    "BOM": { /* Dettagli della Distinta Base */ },
    "Forms": [ /* Elenco dei moduli associati */ ],
    "WhereUsed": [ /* Elenco degli articoli in cui l'item è utilizzato */ ],
    "Documents": [ /* Elenco dei documenti associati */ ]
}
```

### 6.2. `read_from_mongo`

- **Descrizione**: Legge dati dalla collection specificata o da quella di default.
- **Parametri Richiesti**:
  - `database_name`: Nome del database.
  - `collection_name`: Nome della collection.
  - `query`: Query per il recupero dei dati.
  - `output_format`: Formato dell'output (`"string"` o `"object"`).

#### Esempio di Utilizzo

```plaintext
Utilizza lo strumento `read_from_mongo` con i seguenti parametri:
- database_name: "item_classification_db"
- collection_name: "decisional_tree_v2"
- query: { "ParentId": null }
- output_format: "object"
```

### 6.3. `delete_from_mongo`

- **Descrizione**: Elimina dati dalla collection specificata o da quella di default.
- **Parametri Richiesti**:
  - `database_name`: Nome del database.
  - `collection_name`: Nome della collection.
  - `query`: Query per eliminare i dati.

#### Esempio di Utilizzo

```plaintext
Utilizza lo strumento `delete_from_mongo` con i seguenti parametri:
- database_name: "item_classification_db"
- collection_name: "items"
- query: { "ItemId": "A1B2C3" }
```

### 6.4. `update_in_mongo`

- **Descrizione**: Aggiorna dati nella collection specificata o da quella di default.
- **Parametri Richiesti**:
  - `database_name`: Nome del database.
  - `collection_name`: Nome della collection.
  - `query`: Query per aggiornare i dati.
  - `new_values`: Nuovi valori per l'aggiornamento.

#### Esempio di Utilizzo

```plaintext
Utilizza lo strumento `update_in_mongo` con i seguenti parametri:
- database_name: "item_classification_db"
- collection_name: "items"
- query: { "ItemId": "A1B2C3" }
- new_values: {
    "Status": "inactive",
    "LastModifiedDate": "2024-05-01T12:00:00Z"
}
```

## 7. Esecuzione delle Regole e Output JSON

### 7.1. Formato dell'Output JSON

L'LLM deve restituire un output JSON strutturato per ogni regola applicata, con i seguenti campi:

- **Result**: Booleano (`True`/`False`) che indica se la regola è soddisfatta.
- **Justification**: Stringa che fornisce una spiegazione dettagliata della decisione.
- **Notes**: Eventuali note aggiuntive o osservazioni.

#### Esempio di Output JSON

```json
{
  "Result": true,
  "Justification": "La sottostringa dell'ItemId corrisponde a '90960'.",
  "Notes": "Verificato secondo la regola di ingresso."
}
```

### 7.2. Applicazione delle Regole tramite LLM

L'agente utilizza LangChain per interfacciarsi con il modello LLM (ad esempio, GPT-4). Questo permette di:

- **Interpretare e applicare le regole** in linguaggio naturale.
- **Restituire output strutturato in JSON** con esiti delle regole, giustificazioni e note aggiuntive.
- **Gestire interazioni complesse** con i dati degli *item*.
- **Fornire spiegazioni dettagliate** sulle decisioni prese.

#### Passaggi per Applicare una Regola

1. **Creazione del Prompt per l'LLM**

    ```python
    def create_prompt_for_rule(item, rule):
        relevant_data = extract_relevant_data(item, rule)
        prompt = f"""
        Data l'item con le seguenti caratteristiche:
        {json.dumps(relevant_data, indent=2)}
        Applica la seguente regola:
        {rule}
        Fornisci il risultato in formato JSON con i seguenti campi:
        - "Result": true o false
        - "Justification": spiegazione della decisione
        - "Notes": eventuali note aggiuntive
        """
        return prompt
    ```

2. **Chiamata al LLM e Parsing della Risposta**

    ```python
    def apply_rule_with_llm(item, rule):
        prompt = create_prompt_for_rule(item, rule)
        response = llm.generate_response(prompt)
        try:
            rule_output = json.loads(response)
        except json.JSONDecodeError:
            rule_output = {
                "Result": False,
                "Justification": "Errore nel parsing della risposta dell'LLM.",
                "Notes": response
            }
        return rule_output
    ```

### 7.3. Navigazione nell'Albero Decisionale

L'agente naviga attraverso l'albero decisionale applicando le regole ai nodi. Ecco come funziona:

1. **Inizializzazione**

    ```python
    def main():
        # Carica l'albero decisionale
        decision_tree = read_from_mongo(
            database_name="item_classification_db",
            collection_name="decisional_tree_v2",
            query={"ParentId": None},
            output_format="object"
        )
        # Carica l'item da classificare
        item = read_from_mongo(
            database_name="item_classification_db",
            collection_name="items",
            query={"ItemId": "A1B2C3"},
            output_format="object"
        )
        # Inizia la classificazione dalla radice dell'albero
        classification_result = classify_item(item, decision_tree[0])
        # Salva e visualizza il risultato
        write_to_mongo(
            database_name="item_classification_db",
            collection_name=f"classification_results_{classification_result['ID']}",
            data=classification_result
        )
    ```

2. **Funzione di Classificazione Ricorsiva**

    ```python
    def classify_item(item, current_node):
        justification = {}
        if current_node.get("EntryRule"):
            entry_rule_output = apply_rule_with_llm(item, current_node["EntryRule"])
            justification['EntryRule'] = entry_rule_output
            if not entry_rule_output["Result"]:
                return {
                    'ClassId': current_node['ClassId'],
                    'Justification': justification
                }
        
        for rule in current_node.get("AttributeValuationRule", []):
            rule_output = apply_rule_with_llm(item, rule)
            justification[rule] = rule_output
        
        if current_node.get("childRef"):
            for child_class_id in current_node["childRef"]:
                child_node = find_node_by_class_id(decision_tree, child_class_id)
                child_result = classify_item(item, child_node)
                if child_result:
                    justification.update(child_result["Justification"])
                    return {
                        'ClassId': child_result['ClassId'],
                        'Justification': justification
                    }
        else:
            return {
                'ClassId': current_node['ClassId'],
                'Justification': justification
            }
        return None
    ```

3. **Funzione di Ricerca del Nodo per `ClassId`**

    ```python
    def find_node_by_class_id(decision_tree, class_id):
        for node in decision_tree:
            if node['ClassId'] == class_id:
                return node
        return None
    ```

## 8. Output Attesi

### 8.1. Risultato della Classificazione

- **ClassId Finale**: Identificatore della classe in cui l'*item* è stato classificato.
- **Percorso Seguito**: Sequenza di nodi attraversati nell'albero decisionale.

### 8.2. Giustificazione delle Scelte

- **Dettagli sulle Regole Applicate**: Spiegazione di come ogni regola ha influenzato la decisione, basata sugli output JSON dell'LLM.
- **Valori degli Attributi Considerati**: Quali attributi hanno determinato il percorso decisionale.
- **Eventuali Anomalie o Eccezioni**: Segnalazione di dati mancanti o incoerenti.

#### Esempio di Output JSON Finale

```json
{
  "ClassId": "MGT0103",
  "ClassificationPath": ["MGT0101", "MGT0102", "MGT0103"],
  "Justifications": {
    "EntryRule": {
      "Result": true,
      "Justification": "La sottostringa dell'ItemId corrisponde a '90960'.",
      "Notes": "Verificato secondo la regola di ingresso."
    },
    "color == 'red'": {
      "Result": true,
      "Justification": "Il colore dell'item è rosso.",
      "Notes": "Conformità alla regola di colore."
    },
    "size > 10": {
      "Result": false,
      "Justification": "La dimensione dell'item è inferiore a 10.",
      "Notes": "Non soddisfa la regola di dimensione."
    }
  },
  "Timestamp": "2024-04-28T15:00:00Z"
}
```

## 9. Troubleshooting

### Problema: `UnicodeDecodeError` durante lo Streaming

#### Sintomo

Durante lo streaming della risposta dal backend, si verifica un errore di decodifica UTF-8:

```plaintext
UnicodeDecodeError: 'utf-8' codec can't decode byte 0xc3 in position 0: unexpected end of data
```

#### Causa

Il byte `0xc3` è un byte iniziale per una sequenza di caratteri UTF-8 che richiede un byte successivo. L'errore si verifica quando il chunk ricevuto è incompleto, rendendo impossibile la decodifica corretta.

#### Soluzione

Modificare il codice di Streamlit per gestire correttamente i byte incompleti, accumulando i chunk fino a ottenere una sequenza UTF-8 completa prima di tentare la decodifica.

#### Passaggi Dettagliati

1. **Aggiungere la Funzione `is_complete_utf8`**

    ```python
    def is_complete_utf8(data: bytes) -> bool:
        """Verifica se `data` rappresenta una sequenza UTF-8 completa."""
        try:
            data.decode("utf-8")
            return True
        except UnicodeDecodeError:
            return False
    ```

2. **Aggiornare la Funzione `main` per Gestire i Chunk Incompleti**

    ```python
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

            if len(st.session_state.messages) > 10:
                st.session_state.messages = st.session_state.messages[-10:]

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
                            non_decoded_chunk += chunk
                            if is_complete_utf8(non_decoded_chunk):
                                decoded_chunk = non_decoded_chunk.decode("utf-8")
                                full_response += decoded_chunk
                                message_placeholder.markdown(full_response + "▌", unsafe_allow_html=True)
                                non_decoded_chunk = b''  # Svuota il buffer
                message_placeholder.markdown(full_response)
            st.session_state.messages.append({"role": "assistant", "content": full_response})
    ```

3. **Esempio Completo del File della UI (`main.py`)**

    ```python
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
    ```

## 10. Conclusione

Questo progetto ha sviluppato un agente intelligente capace di classificare *item* complessi utilizzando un albero decisionale e un insieme di regole. L'integrazione con un LLM tramite LangChain permette una flessibilità nell'interpretazione delle regole, mentre le capacità multi-strumento garantiscono un'efficiente gestione dei dati e delle operazioni necessarie. L'aggiunta di un output strutturato in JSON dall'LLM migliora l'integrazione dei risultati nel processo decisionale, facilitando l'analisi automatizzata degli esiti delle regole e delle giustificazioni. Il sistema è progettato per essere estensibile, permettendo future integrazioni con algoritmi esperti e ulteriori strumenti.

## 11. Prossimi Passi

- **Definizione Dettagliata delle Regole**: Formalizzare tutte le regole presenti nei nodi dell'albero decisionale, specificando il formato dell'output JSON per ciascuna.
- **Sviluppo del Prototipo**: Implementare una versione iniziale dell'agente per testare il flusso di lavoro e la gestione degli output JSON.
- **Validazione e Test**: Utilizzare dati reali per verificare l'efficacia del sistema, analizzando gli output JSON per migliorare l'accuratezza e l'efficienza.
- **Miglioramento dell'Interfaccia Utente**: Aggiungere funzionalità avanzate all'interfaccia Streamlit per una migliore esperienza utente.
- **Monitoraggio delle Prestazioni**: Implementare strumenti di logging e monitoraggio per analizzare le prestazioni del sistema in tempo reale.
- **Sicurezza e Gestione delle Chiavi**: Implementare misure di sicurezza per proteggere le chiavi API e garantire l'accesso sicuro al database.

---

**Nota**: Assicurati di mantenere aggiornati i file di configurazione e di seguire le best practice per la gestione delle dipendenze e della sicurezza. Questo garantisce l'integrità e la scalabilità del sistema man mano che il progetto si evolve.
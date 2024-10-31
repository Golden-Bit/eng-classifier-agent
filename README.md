# Documento di Progetto per la Progettazione Logica di un Agente Multi-Strumento Basato su LLM per la Classificazione di Item

## Indice

1. **Introduzione**
2. **Obiettivi del Progetto**
3. **Architettura del Sistema**
   - 3.1. Componenti Principali
   - 3.2. Flusso di Lavoro Generale
4. **Design dell'Agente**
   - 4.1. Integrazione con LLM tramite LangChain
   - 4.2. Capacità Multi-Strumento
   - 4.3. Applicazione delle Regole e Output Strutturato
   - 4.4. Navigazione tra i Nodi dell'Albero Decisionale
   - 4.5. Descrizione Dettagliata della Logica (Pseudocodice)
5. **Strutture Dati**
   - 5.1. Schema JSON degli Item
   - 5.2. Schema dei Nodi dell'Albero Decisionale
6. **Esecuzione delle Regole e Output JSON**
   - 6.1. Formato dell'Output JSON
   - 6.2. Applicazione Iniziale tramite Agente LLM
   - 6.3. Valutazione per Algoritmi Esperti
7. **Strumenti dell'Agente**
   - 7.1. Navigazione Efficiente dei Campi JSON
   - 7.2. Esecuzione di Codice Python
   - 7.3. Manipolazione e Visualizzazione di File
8. **Output Attesi**
   - 8.1. Risultato della Classificazione
   - 8.2. Giustificazione delle Scelte
9. **Conclusione**

---

## 1. Introduzione

Questo documento descrive il progetto per la progettazione logica, in Python, di un sistema basato su Large Language Model (LLM) utilizzando LangChain. Il sistema prevede un agente multi-strumento in grado di classificare oggetti denominati *item* (elementi e componenti) secondo uno schema di regole applicate a un albero decisionale. Gli *item* seguono uno schema JSON dettagliato, e l'agente deve navigare tra i nodi dell'albero, applicando le regole di classificazione e restituendo sia il risultato che una giustificazione delle scelte effettuate. Inoltre, l'LLM applicato sui nodi deve restituire un output in JSON strutturato dopo aver applicato le regole, dove un campo dell'output contiene l'esito True/False e un altro campo contiene la giustificazione, note aggiuntive, ecc.

## 2. Obiettivi del Progetto

- **Sviluppare un agente intelligente** capace di classificare gli *item* secondo le regole definite.
- **Integrare un LLM tramite LangChain** per l'applicazione iniziale delle regole, con output strutturato in JSON.
- **Permettere l'espansione futura** verso l'uso di algoritmi esperti per l'esecuzione delle regole.
- **Fornire strumenti all'agente** per navigare efficientemente nei campi JSON, eseguire codice Python e manipolare file.
- **Garantire un output dettagliato**, includendo sia la classificazione risultante che la giustificazione delle decisioni prese, in un formato JSON strutturato.

## 3. Architettura del Sistema

### 3.1. Componenti Principali

- **Agente LLM Multi-Strumento**: Il cuore del sistema, responsabile dell'elaborazione e della classificazione degli *item*.
- **Interfaccia LangChain**: Utilizzata per interagire con il modello LLM e orchestrare le operazioni dell'agente.
- **Albero Decisionale**: Struttura che definisce i nodi, le regole e le relazioni per la classificazione.
- **Database degli Item**: Collezione di *item* da classificare, conformi allo schema JSON fornito.

### 3.2. Flusso di Lavoro Generale

1. **Input dell'Item**: L'agente riceve un *item* da classificare.
2. **Inizializzazione**: L'agente carica l'albero decisionale e le regole associate.
3. **Navigazione dell'Albero**: L'agente inizia dal nodo radice e naviga tra i nodi applicando le regole.
4. **Applicazione delle Regole con Output JSON**: Le regole di ciascun nodo vengono applicate utilizzando l'LLM, che restituisce un output in JSON strutturato.
5. **Determinazione della Classificazione**: L'agente analizza gli output JSON per decidere il percorso nell'albero decisionale e, infine, la classificazione dell'*item*.
6. **Generazione dell'Output**: L'agente restituisce la classificazione e una giustificazione dettagliata delle scelte effettuate, in un formato JSON strutturato.

## 4. Design dell'Agente

### 4.1. Integrazione con LLM tramite LangChain

L'agente utilizzerà LangChain per interfacciarsi con un modello LLM (ad esempio, GPT-4). Questo permetterà di:

- **Interpretare e applicare le regole** in linguaggio naturale.
- **Restituire output strutturato in JSON** con esiti delle regole, giustificazioni e note aggiuntive.
- **Gestire interazioni complesse** con i dati degli *item*.
- **Fornire spiegazioni dettagliate** sulle decisioni prese.

### 4.2. Capacità Multi-Strumento

Per eseguire le operazioni richieste, l'agente avrà accesso a diversi strumenti:

- **Navigazione JSON**: Per esplorare e analizzare i dati degli *item*.
- **Esecuzione di Codice Python**: Per operazioni computazionali o manipolazioni avanzate.
- **Manipolazione e Visualizzazione di File**: Per gestire documenti associati agli *item*.

### 4.3. Applicazione delle Regole e Output Strutturato

Le regole di classificazione saranno applicate in due fasi:

1. **Applicazione Iniziale tramite LLM con Output JSON**: L'agente utilizza l'LLM per interpretare e applicare le regole in modo flessibile, ottenendo un output strutturato in JSON che include l'esito (True/False), la giustificazione e note aggiuntive.
2. **Valutazione per Algoritmi Esperti**: In base ai risultati, si potrà decidere di implementare alcune regole tramite algoritmi esperti per maggiore efficienza, mantenendo l'output coerente in formato JSON.

### 4.4. Navigazione tra i Nodi dell'Albero Decisionale

L'agente dovrà:

- **Iniziare dal nodo radice** dell'albero decisionale.
- **Applicare le regole del nodo corrente** e analizzare l'output JSON per determinare il percorso successivo.
- **Navigare tra i nodi figli** basandosi sull'esito (True/False) delle regole applicate.
- **Ripetere il processo** fino a raggiungere un nodo foglia (classificazione finale).

### 4.5. Descrizione Dettagliata della Logica (Pseudocodice)

#### Inizializzazione

```pseudo
function main():
    # Carica l'albero decisionale
    decision_tree = load_decision_tree()

    # Carica l'item da classificare
    item = load_item()

    # Inizia la classificazione dalla radice dell'albero
    classification_result = classify_item(item, decision_tree.root)

    # Genera l'output con la giustificazione
    generate_output(classification_result)
```

#### Funzione di Classificazione Ricorsiva

```pseudo
function classify_item(item, current_node):
    # Inizializza la giustificazione per il nodo corrente
    justification = {}

    # Applicazione della EntryRule del nodo corrente tramite LLM
    if current_node.EntryRule is not None:
        entry_rule_output = apply_rule_with_llm(item, current_node.EntryRule)
        justification['EntryRule'] = entry_rule_output

        if not entry_rule_output['Result']:
            # Se la EntryRule non è soddisfatta, termina la navigazione
            return {
                'ClassId': current_node.ClassId,
                'Justification': justification
            }

    # Applicazione delle AttributeValuationRule
    for rule in current_node.AttributeValuationRule:
        rule_output = apply_rule_with_llm(item, rule)
        justification[rule] = rule_output

    # Se il nodo ha figli, naviga tra essi
    if current_node.childRef is not None and len(current_node.childRef) > 0:
        for child_class_id in current_node.childRef:
            child_node = find_node_by_class_id(decision_tree, child_class_id)
            # Chiamata ricorsiva alla funzione di classificazione sul nodo figlio
            child_result = classify_item(item, child_node)
            if child_result is not None:
                # Aggrega le giustificazioni
                justification.update(child_result['Justification'])
                return {
                    'ClassId': child_result['ClassId'],
                    'Justification': justification
                }
    else:
        # Nodo foglia raggiunto
        return {
            'ClassId': current_node.ClassId,
            'Justification': justification
        }

    # Se nessun percorso è valido, ritorna None
    return None
```

#### Applicazione delle Regole con Output JSON

```pseudo
function apply_rule_with_llm(item, rule):
    # Crea il prompt per l'LLM
    prompt = create_prompt_for_rule(item, rule)
    response = llm_call(prompt)

    # L'LLM restituisce un output JSON strutturato
    rule_output = parse_llm_json_response(response)

    return rule_output
```

#### Formato dell'Output JSON dell'LLM

L'LLM deve restituire un output JSON con il seguente formato:

```json
{
  "Result": true,
  "Justification": "La giustificazione dettagliata della decisione.",
  "Notes": "Eventuali note aggiuntive o osservazioni."
}
```

#### Creazione del Prompt per l'LLM

```pseudo
function create_prompt_for_rule(item, rule):
    # Estrarre le informazioni necessarie dall'item
    relevant_data = extract_relevant_data(item, rule)

    # Creare il prompt in linguaggio naturale con istruzioni per l'output JSON
    prompt = f"""
    Data l'item con le seguenti caratteristiche:
    {relevant_data}
    Applica la seguente regola:
    {rule}
    Fornisci il risultato in formato JSON con i seguenti campi:
    - "Result": true o false
    - "Justification": spiegazione della decisione
    - "Notes": eventuali note aggiuntive
    """
    return prompt
```

#### Chiamata al LLM

```pseudo
function llm_call(prompt):
    # Utilizza LangChain per interfacciarsi con l'LLM
    response = langchain_interface.generate_response(prompt)
    return response
```

#### Analisi della Risposta del LLM

```pseudo
function parse_llm_json_response(response):
    try:
        # Parsifica la risposta JSON dell'LLM
        rule_output = json.loads(response)
    except JSONDecodeError:
        # Gestisce errori di parsing
        rule_output = {
            "Result": false,
            "Justification": "Errore nel parsing della risposta dell'LLM.",
            "Notes": response
        }
    return rule_output
```

#### Funzioni di Supporto

```pseudo
function extract_relevant_data(item, rule):
    # Naviga nei campi JSON dell'item per estrarre i dati rilevanti
    data = {}
    # Implementa la logica per estrarre gli attributi necessari
    return data

function find_node_by_class_id(decision_tree, class_id):
    # Ricerca il nodo nell'albero decisionale con il ClassId specificato
    return node
```

#### Generazione dell'Output

```pseudo
function generate_output(classification_result):
    # Crea un report con la classificazione finale e le giustificazioni
    output = {
        'ClassId': classification_result['ClassId'],
        'ClassificationPath': get_classification_path(classification_result),
        'Justification': classification_result['Justification']
    }
    # Visualizza o salva l'output
    display_output(output)
```

## 5. Strutture Dati

### 5.1. Schema JSON degli Item

Gli *item* seguono uno schema JSON dettagliato, che include:

- **Proprietà principali**: Id, ItemId, Name, Description, Revision, ObjectType, ecc.
- **Attributi personalizzati**: Una lista di attributi definiti dall'utente.
- **Relazioni**: BOM, Forms, WhereUsed, Documents.

### 5.2. Schema dei Nodi dell'Albero Decisionale

Ogni nodo dell'albero ha la seguente struttura:

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

## 6. Esecuzione delle Regole e Output JSON

### 6.1. Formato dell'Output JSON

L'LLM deve restituire un output JSON strutturato per ogni regola applicata, con i seguenti campi:

- **Result**: Booleano (True/False) che indica se la regola è soddisfatta.
- **Justification**: Stringa che fornisce una spiegazione dettagliata della decisione.
- **Notes**: Eventuali note aggiuntive o osservazioni.

### 6.2. Applicazione Iniziale tramite Agente LLM

- **Interpretazione delle Regole**: L'agente utilizza l'LLM per comprendere le regole scritte in linguaggio naturale.
- **Applicazione ai Dati dell'Item**: Le regole vengono applicate ai dati specifici dell'*item* attraverso i prompt generati.
- **Analisi dell'Output JSON**: L'agente analizza l'output JSON dell'LLM per determinare l'esito della regola e le giustificazioni.

### 6.3. Valutazione per Algoritmi Esperti

- **Identificazione di Regole Complesse**: Alcune regole potrebbero richiedere un'elaborazione più efficiente o precisa.
- **Implementazione di Algoritmi**: Sviluppare funzioni specifiche per queste regole, mantenendo l'output coerente in formato JSON.
- **Integrazione nel Flusso**: Gli algoritmi vengono utilizzati in sostituzione o in supporto all'LLM.

## 7. Strumenti dell'Agente

### 7.1. Navigazione Efficiente dei Campi JSON

- **Parsing Avanzato**: Utilizzo di librerie come `json` o `pydantic` per gestire gli *item*.
- **Ricerca e Filtraggio**: Funzionalità per cercare rapidamente attributi e valori specifici.

```pseudo
function get_attribute_value(item, attribute_name):
    for attribute in item.Attributes:
        if attribute.Name == attribute_name:
            return attribute.Value
    return None
```

### 7.2. Esecuzione di Codice Python

- **Interpreter Integrato**: L'agente può eseguire codice Python per calcoli o manipolazioni.

```pseudo
function execute_python_code(code_snippet, context):
    # Esegue il codice in un ambiente sicuro
    result = safe_exec(code_snippet, context)
    return result
```

- **Sicurezza**: Limitare l'esecuzione a codice sicuro per evitare rischi.

### 7.3. Manipolazione e Visualizzazione di File

- **Gestione di Documenti**: Apertura e lettura di file associati agli *item* (es. documenti di validazione).

```pseudo
function read_associated_documents(item):
    for document in item.Documents:
        content = read_file(document.file_path)
        # Processa il contenuto se necessario
```

- **Visualizzazione**: Presentazione dei contenuti rilevanti all'interno del processo decisionale.

## 8. Output Attesi

### 8.1. Risultato della Classificazione

- **ClassId Finale**: Identificatore della classe in cui l'*item* è stato classificato.
- **Percorso Seguito**: Sequenza di nodi attraversati nell'albero decisionale.

### 8.2. Giustificazione delle Scelte

- **Dettagli sulle Regole Applicate**: Spiegazione di come ogni regola ha influenzato la decisione, basata sugli output JSON dell'LLM.
- **Valori degli Attributi Considerati**: Quali attributi hanno determinato il percorso decisionale.
- **Eventuali Anomalie o Eccezioni**: Segnalazione di dati mancanti o incoerenti.

## 9. Conclusione

Questo progetto mira a sviluppare un agente intelligente capace di classificare *item* complessi utilizzando un albero decisionale e un insieme di regole. L'integrazione con un LLM tramite LangChain permette una flessibilità nell'interpretazione delle regole, mentre le capacità multi-strumento garantiscono un'efficiente gestione dei dati e delle operazioni necessarie. L'aggiunta di un output strutturato in JSON dall'LLM migliora l'integrazione dei risultati nel processo decisionale, facilitando l'analisi automatizzata degli esiti delle regole e delle giustificazioni. Il sistema è progettato per essere estensibile, permettendo future integrazioni con algoritmi esperti e ulteriori strumenti.

---

**Prossimi Passi**:

- **Definizione Dettagliata delle Regole**: Formalizzare tutte le regole presenti nei nodi dell'albero decisionale, specificando il formato dell'output JSON per ciascuna.
- **Sviluppo del Prototipo**: Implementare una versione iniziale dell'agente per testare il flusso di lavoro e la gestione degli output JSON.
- **Validazione e Test**: Utilizzare dati reali per verificare l'efficacia del sistema, analizzando gli output JSON per migliorare l'accuratezza e l'efficienza.
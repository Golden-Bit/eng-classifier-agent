import json
import yaml
from jsonschema import validate, Draft7Validator, exceptions


def load_yaml_schema(schema_path):
    """
    Carica lo schema YAML da un file e lo converte in un dizionario Python.
    """
    with open(schema_path, 'r', encoding='utf-8') as file:
        schema = yaml.safe_load(file)
    return schema


def validate_json_data(json_data, schema):
    """
    Valida il JSON data rispetto allo schema fornito.
    """
    try:
        validate(instance=json_data, schema=schema)
        print("Il JSON fornito è valido rispetto allo schema.")
    except exceptions.ValidationError as err:
        print("Il JSON fornito non è valido rispetto allo schema.")
        print("Messaggio di errore:", err.message)
        print("Percorso dell'errore nel JSON:", list(err.absolute_path))
        print("Percorso dell'errore nello schema:", list(err.absolute_schema_path))


def main():
    # Carica il JSON fornito (sostituisci 'data.json' con il nome del tuo file JSON)
    with open('input_data/example.json', 'r', encoding='utf-8') as file:
        json_data = json.load(file)

    # Carica lo schema YAML (sostituisci 'schema.yaml' con il nome del tuo file YAML)
    schema = load_yaml_schema('schemas/item_schema.yaml')

    print(json_data)
    print(schema)
    # Valida il JSON rispetto allo schema
    validate_json_data(json_data, schema)


if __name__ == "__main__":
    main()

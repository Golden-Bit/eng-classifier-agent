import json
from utilities.tools.mongodb import MongoDBToolKitManager


def upload_in_mongo(file_path: str):
    with open(file_path) as decisional_tree_file:
        decisional_tree = json.load(decisional_tree_file)
        dumped_decisional_tree = json.dumps(decisional_tree)

    mongodb_toolkit = MongoDBToolKitManager(
        connection_string="mongodb://localhost:27017",
        default_database="default_database",
        default_collection="default_collection",
    )

    mongodb_toolkit.write_to_mongo(
        database_name="item_classification_db_3",
        collection_name="items",
        data=dumped_decisional_tree,
    )

    loaded_data = mongodb_toolkit.read_from_mongo(
        database_name="item_classification_db_3",
        collection_name="items",
        query="{}",
        output_format="object"
    )
    # print(loaded_data)
    # loaded_data = loaded_data.replace("'", '"')
    # loaded_data = json.loads(loaded_data)

    for doc in loaded_data:
        doc["_id"] = str(doc["_id"])

    print(json.dumps(loaded_data, indent=4))

    # print(json.dumps(json.loads(loaded_data), indent=4))

def delete_all_items():
    """Elimina tutti i documenti dalla collezione 'items' nel database 'item_classification_db_3'."""
    mongodb_toolkit = MongoDBToolKitManager(
        connection_string="mongodb://localhost:27017",
        default_database="item_classification_db_3",
        default_collection="items",
    )

    # Usa una query vuota per eliminare tutti i documenti
    mongodb_toolkit.delete_from_mongo(
        database_name="item_classification_db_3",
        collection_name="items",
        query="{}"
    )
    print("Tutti gli elementi nella collezione 'items' sono stati eliminati.")


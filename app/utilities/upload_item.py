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


if __name__ == "__main__":
    upload_in_mongo(file_path="C:\\Users\\Golden Bit\\Desktop\\tmp\\input_data\\data.json")




import json
from utilities.tools.mongodb import MongoDBToolKitManager


if __name__ == "__main__":

    with open("C:\\Users\\Golden Bit\\Desktop\\tmp\\input_data\\decisional_tree.json") as decisional_tree_file:
        decisional_tree = json.load(decisional_tree_file)
        dumped_decisional_tree = json.dumps(decisional_tree)

    mongodb_toolkit = MongoDBToolKitManager(
        connection_string="mongodb://localhost:27017",
        default_database="default_database",
        default_collection="default_collection",
    )

    mongodb_toolkit.write_to_mongo(
        database_name="item_classification_db",
        collection_name="decisional_tree_v2",
        data=dumped_decisional_tree,
    )

    loaded_data = mongodb_toolkit.read_from_mongo(
        database_name="item_classification_db",
        collection_name="decisional_tree_v2",
        query="{}",
        output_format="object"
    )
    #print(loaded_data)
    #loaded_data = loaded_data.replace("'", '"')
    #loaded_data = json.loads(loaded_data)

    for doc in loaded_data:
        doc["_id"] = str(doc["_id"])

    print(json.dumps(loaded_data, indent=4))

    #print(json.dumps(json.loads(loaded_data), indent=4))



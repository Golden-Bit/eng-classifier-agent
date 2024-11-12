import json
import os
from fastapi import FastAPI, HTTPException, APIRouter, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Dict, Any, List
from utilities.tools.mongodb import MongoDBToolKitManager

router = APIRouter()

# Pydantic models
class UploadDecisionalTreeRequest(BaseModel):
    data: List[Dict[str, Any]]  # Decisional tree is a list of dictionaries

class UploadItemsRequest(BaseModel):
    data: List[Dict[str, Any]]  # Items are also a list of dictionaries


# Functions
def upload_decisional_tree_in_mongo(data: List[Dict[str, Any]]):
    mongodb_toolkit = MongoDBToolKitManager(
        connection_string="mongodb://localhost:27017",
        default_database="item_classification_db_3",
        default_collection="decisional_tree",
    )

    try:
        mongodb_toolkit.write_to_mongo(
            database_name="item_classification_db_3",
            collection_name="decisional_tree",
            data=json.dumps(data, indent=2),  # Pass data as JSON string
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to upload decisional tree to MongoDB: {e}")

def delete_all_decisional_tree_items():
    mongodb_toolkit = MongoDBToolKitManager(
        connection_string="mongodb://localhost:27017",
        default_database="item_classification_db_3",
        default_collection="decisional_tree",
    )

    try:
        mongodb_toolkit.delete_all_from_mongo(
            database_name="item_classification_db_3",
            collection_name="decisional_tree",
            query="{}"
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to delete decisional tree items: {e}")

def upload_items_in_mongo(data: List[Dict[str, Any]]):
    mongodb_toolkit = MongoDBToolKitManager(
        connection_string="mongodb://localhost:27017",
        default_database="item_classification_db_3",
        default_collection="items",
    )

    try:
        mongodb_toolkit.write_to_mongo(
            database_name="item_classification_db_3",
            collection_name="items",
            data=json.dumps(data, indent=2),  # Pass data as JSON string
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to upload items to MongoDB: {e}")

def delete_all_items():
    mongodb_toolkit = MongoDBToolKitManager(
        connection_string="mongodb://localhost:27017",
        default_database="item_classification_db_3",
        default_collection="items",
    )

    try:
        mongodb_toolkit.delete_all_from_mongo(
            database_name="item_classification_db_3",
            collection_name="items",
            query="{}"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to delete items: {e}")

# Endpoints
@router.post("/upload_decisional_tree")
async def upload_decisional_tree(request: UploadDecisionalTreeRequest):
    upload_decisional_tree_in_mongo(request.data)
    return {"message": "Decisional tree uploaded successfully"}

@router.post("/delete_decisional_tree")
async def delete_decisional_tree():
    delete_all_decisional_tree_items()
    return {"message": "All decisional tree items deleted successfully"}

@router.post("/upload_items")
async def upload_items(request: UploadItemsRequest):
    upload_items_in_mongo(request.data)
    return {"message": "Items uploaded successfully"}

@router.post("/delete_items")
async def delete_items():
    delete_all_items()
    return {"message": "All items deleted successfully"}

# New endpoints to retrieve data
@router.get("/decisional_tree")
async def get_decisional_tree(filter: str = Query("{}", description="Optional MongoDB query filter as JSON string")):
    mongodb_toolkit = MongoDBToolKitManager(
        connection_string="mongodb://localhost:27017",
        default_database="item_classification_db_3",
        default_collection="decisional_tree",
    )

    try:
        query = filter  # Assuming the read_from_mongo function accepts query as a JSON string
        data = mongodb_toolkit.read_from_mongo(
            database_name="item_classification_db_3",
            collection_name="decisional_tree",
            query=query,
            output_format="object"
        )
        # Convert ObjectId to string if necessary
        for doc in data:
            doc["_id"] = str(doc["_id"])
        return data
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to retrieve decisional tree data: {e}")

@router.get("/items")
async def get_items(filter: str = Query("{}", description="Optional MongoDB query filter as JSON string")):
    mongodb_toolkit = MongoDBToolKitManager(
        connection_string="mongodb://localhost:27017",
        default_database="item_classification_db_3",
        default_collection="items",
    )

    try:
        query = filter  # Assuming the read_from_mongo function accepts query as a JSON string
        data = mongodb_toolkit.read_from_mongo(
            database_name="item_classification_db_3",
            collection_name="items",
            query=query,
            output_format="object"
        )
        # Convert ObjectId to string if necessary
        for doc in data:
            doc["_id"] = str(doc["_id"])
        return data
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to retrieve items data: {e}")


@router.post("/overwrite_decisional_tree")
async def overwrite_decisional_tree(request: UploadDecisionalTreeRequest):
    # First delete all existing decisional tree items
    delete_all_decisional_tree_items()
    # Then upload the new data
    upload_decisional_tree_in_mongo(request.data)
    return {"message": "Decisional tree overwritten successfully"}


@router.post("/overwrite_items")
async def overwrite_items(request: UploadItemsRequest):
    # First delete all existing items
    delete_all_items()
    # Then upload the new data
    upload_items_in_mongo(request.data)
    return {"message": "Items overwritten successfully"}

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allow all methods
    allow_headers=["*"],  # Allow all headers
)

app.include_router(router, prefix="/utilities", tags=["utilities"])

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8091)

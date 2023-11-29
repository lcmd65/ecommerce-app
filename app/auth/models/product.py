from pymongo import MongoClient
import json
from bson import ObjectId  # Import ObjectId from bson
from app.cache import cache
from app.db import database_connection

class Product:
    def __init__(self):
        # Load the MongoDB connection details from the schema.json file
        client, database = database_connection()
        collection = database["Product"]
        self.documents = list(collection.find())  # Convert the cursor to a list
        client.close()

    def to_dict(self):
        # Convert ObjectId to string before returning the dictionary
        list_data = []
        for item in self.documents:
            list_data.append({"_id": str(item["_id"]), "name": str(item["name"]), "price": item["price"], "currency": item["currency"], "brand": item["brand"]})
        return list_data

    def set_cache(self):
        # Use JSON.dumps to serialize the list of documents to a JSON string
        product_json = json.dumps(self.to_dict())

        # Set the JSON string to the cache
        cache.set('Product', product_json)

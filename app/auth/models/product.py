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
        documents = list(collection.find())
        self.documents = documents[0:50]
        client.close()

    def to_dict(self):
        # Convert ObjectId to string before returning the dictionary
        processed_data = []

        for item in self.documents:
            processed_item = {}
            for key, value in item.items():
                if key == 'images':
                        # Attempt to convert the value to a float
                        processed_item[key] = "" if (str(value) == "nan" or str(value) == None) else value
                else:
                    processed_item[key] = value

            processed_data.append(processed_item)
            
        list_data = [
            {
                "_id": str(item["_id"]),
                "name": item["name"],
                "price": item["price"],
                "currency": item["currency"],
                "brand": item["brand"],
                "images": item["images"]
            }
            for item in processed_data
        ]
       
        return list_data

    def set_cache(self):
        # Use JSON.dumps to serialize the list of documents to a JSON string
        product_json = json.dumps(self.to_dict())

        # Set the JSON string to the cache
        cache.set('Product', product_json)

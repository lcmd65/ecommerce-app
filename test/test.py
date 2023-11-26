from pymongo import MongoClient
import json
from bson import ObjectId  # Import ObjectId from bson
from app.cache import cache

class Product:
    def __init__(self):
        # Load the MongoDB connection details from the schema.json file
        with open("app/schema.json", "r") as file:
            config = json.load(file)

        # Connect to MongoDB
        client = MongoClient(config["mongo_uri"])
        database = client["Datathon"]
        self.collection = database["Product"]
        self.documents = list(self.collection.find())  # Convert the cursor to a list
        client.close()

    def to_dict(self):
        # Convert ObjectId to string before returning the dictionary
        return [{**item, "_id": str(item["_id"])} for item in self.documents]

    def set_cache(self):
        # Use JSON.dumps to serialize the list of documents to a JSON string
        product_json = json.dumps(self.to_dict())

        # Set the JSON string to the cache
        cache.set('Product', product_json)

    def display(self):
        for item in self.to_dict():
            print(item)

if __name__ == "__main__":
    product = Product()
    product.display()

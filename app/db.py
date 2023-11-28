from pymongo import MongoClient
import json

def database_connection():
    with open("app/schema.json", "r") as file:
        config = json.load(file)
        # Connect to MongoDB
    client = MongoClient(config["mongo_uri"])
    database = client["Datathon"]
    return client, database
        
        
from flask import Flask
from pymongo import MongoClient
from app.auth.controllers.controllers import user_parsing
import json
from app.cache import cache

class Product():
    def __init__(self):
        file = json.load("schema.json")
        client = MongoClient(file["mongo_uri"])
        database = client["Datathon"]
        self.collection = database["Product"]
        self.document = self.collection.find()
        client.close()
        self.setCache()
    
    def __dict__(self):
        return list(self.document)
    
    def setCache(self):
        if cache.get('Product') == None:
            cache.set('Product', json.dumps(self.__dict__()))
    
from app.db import database_connection
from app.cache import cache

class UserChat:
    def __init__(self):
        self.id = cache.get("user")["id"]
        self.chat = []
        
    def to_dict(self):
        return {
                "id": self.id,
                "chat": self.chat
            }          
             
class UserCart:
    def __init__(self):
        client, database = database_connection()
        
        collection = database['User_Cart']
        cart = collection.find()
        self.id = cart["id"]
        self.item = cart["item"]
        client.close()
    
    def to_dict(self):
        return{
            "id": self.id,
            "item": self.item
        }
from flask import Flask
from pymongo import MongoClient
from app.auth.controllers.controllers import user_parsing
import json
from app.cache import cache


class User():
    def __init__(self):
        self.username = None
        self.password = None
        self.gender = None
        self.image = None
        self.chat_messate = []
        
        def user_parsing(self, username, password):
            user_information = user_parsing(username, password)
        
        def __dict__(self):
            return {
                "username": self.username,
                "password": self.password,
                "gender":self.gender,
                "image": self.image,
                "chat_message": self.chat_messa.get
                }
        
        def image_parsing(self):
            import bson
            image = bson.decode(self.image)
            self.image = image
    
        
    
    
    
    
        
        
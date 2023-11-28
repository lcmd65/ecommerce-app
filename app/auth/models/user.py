from flask import Flask
from pymongo import MongoClient
from app.auth.controllers.controllers import user_parsing
import json
from app.cache import cache
from app.db import database_connection


class User():
    def __init__(self, user_information = None):
        self.id = user_information['id']
        self.username = user_information['username']
        self.password = user_information['password']
        self.gender = user_information['gender']
        self.email = user_information['email']
        self.image = None
        self.chat_message = []
        
        def __dict__(self):
            return {
                "id": self.id,
                "username": self.username,
                "password": self.password,
                "email": self.email,
                "gender":self.gender,
                "image": self.image,
                "chat_message": self.chat_message
            }
        
    def user_parsing(self, username):
        client, database = database_connection()
        collection = database["User"]
        
        # Convert the cursor to a list
        user_information = collection.find_one({'username': username})
        self.__init__(user_information)
        client.close()
        
    def image_parsing(self):
        import bson
        client, database = database_connection()
        collection = database["User_Image"]
        
        # pasring image from id
        user_image = collection.find_one({'id': self.id})
        image = bson.decode(user_image)
        self.image = image
        
        # close connection
        client.close()
        
        
        
    
    
        
    
    
    
    
        
        
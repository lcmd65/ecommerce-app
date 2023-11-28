from app.auth.models.user import User
from app.cache import cache
from pymongo import MongoClient
from app.db import database_connection
import json

def authentication(username, password):
    # connection to db from schema
    client, database = database_connection()
    collection = database["User"]
    
    # Convert the cursor to a list
    user_information = collection.find_one({'username': username})
    client.close()
    
    # parsing user and authentication
    if user_information['password'] == password:
        user = User()
        user.user_parsing(username)
        cache.set('user' ,json.dumps(user.__dict__()))
        return True
    else:
        return False
        
def confirm_authentication(username, email, newpass, confirm_newpass):
    if newpass == confirm_newpass:
        client, database = database_connection()
        # Find the user with the given username and email
        collection = database["User"]
        user_query = {'username': username, 'email': email}
        existing_user = collection.find_one(user_query)

        if existing_user:
            # Update the user's password
            update_query = {'$set': {'password': newpass}}
            collection.update_one(user_query, update_query)
            client.close()
            return True  # Password updated successfully
        else:
            client.close()
            return False  # User not found

def register_user(username, email, password, id , gender):
    
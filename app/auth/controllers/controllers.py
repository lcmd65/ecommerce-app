import app.cache
from app.db import database_connection
import json

def authentication(username, password):
    """
    authentication processing for login

    Args:
        username (str): account username
        password (str): account password

    Returns:
        bool: result of event
    """
    # connection to db from schema
    client, database = database_connection()
    collection = database["User"]
    
    # Convert the cursor to a list
    user_information = collection.find_one({'username': username})
    client.close()
    
    # parsing user and authentication
    if user_information != None and user_information['password'] == password:
        from app.auth.models.user import User
        user = User(user_information)
        app.cache.cache.set('user' ,json.dumps(user.__dict__()))
        return True
    else:
        return False
        
def confirm_authentication(username, email, newpass, confirm_newpass):
    """
    authentication and update password

    Args:
        username (str): username account
        email (str): user email
        newpass (str): user new password
        confirm_newpass (_type_): confirm user new password

    Returns:
        bool: result of event
    """
    if newpass == confirm_newpass:
        client, database = database_connection()
        collection = database["User"]
        
        # Find the user with the given username and email
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

def register_user(username, email, password, user_id , gender):
    """
    register new user

    Args:
        username (str): username account
        email (str): user email
        password (str): user password
        user_id (str): id
        gender (M/F): Male or Female

    Returns:
        bool: result of event 
    """
    client, database = database_connection()
    collection = database["User"]
    cart_collection = database["User_Cart"] 
    
    # Check if the username or email is already registered
    existing_user = collection.find_one({'$or': [{'username': username}, {'email': email}, {'id': user_id}]})

    if existing_user:
        # Username or email is already taken
        client.close()
        return False
    else:
        # Register the new user
        new_user = {
            'username': username,
            'password': password,
            'email': email,
            'gender': gender,
            'id': user_id
        }
        
        new_cart = {
            'id': user_id,
            'cart': []
        }
        
        collection.insert_one(new_user)
        client.close()
        return True  # Registration successful
    
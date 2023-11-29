from flask import Blueprint, request, jsonify
from app.db import database_connection
import app.cache
import json

## chat data store in cache
## chat_data = 

api_blueprint = Blueprint('api_blueprint', __name__)

def extract_information(message):
    """_summary_

    Args:
        message (_type_): _description_
    """
    pass

def validate(features):
    """_summary_

    Args:
        features (_type_): _description_
    """
    pass

def prompt_generation_processing():
    pass

def processing(message):
    """
    _summary_ 

    Args:
        message (_type_): _description_

    Returns:
        _type_: _description_
    """
    features = extract_information(respone)
    while validate(features) == False:
        prompt_generation_processing()
        features = extract_information(respone)

        respone = processing
    return respone
    
            
@api_blueprint.route('/chat_api', methods = ['GET', 'POST'])
def chat():
    message = request.json.get('message')
    respone = processing(message)
    return jsonify(respone)

@api_blueprint.route("/description_get", methods = ['GET', 'POST'])
def description_get():
    message = request.json.get('_id') # product id
    client, database = database_connection()
    collection = database["Product"]
    item = collection.find_one({'_id': message})
    client.close()
    return item['description']

@api_blueprint.route("/cart_get", methods = ['GET', 'POST'])
def cart_get():
    cart = app.cache.cache.get("cart")
    if cart == None :
        message = request.json.get('user_id')
        client, database = database_connection()
        collection = database["User_Card"]
        cart = collection.find_one({'id': message})
        client.close()
    return jsonify(json.dumps(cart))

@api_blueprint.route("/cart_add", methods = ['GET', 'POST'])
def cart_add():
    try:
        item_id = request.json.get('_id') 
        user_id = app.cache.cache.get('user')['id']
        client, database = database_connection()
        collection = database["User_Card"]
        cart_db = collection.find_one({'id': user_id})
        items = json.loads(cart_db.get('item', '[]')).append(item_id)
        collection.update_one({'id': user_id}, {'$set': {'item': json.dumps(items)}})
        client.close()
        return "True"
    except:
        return "False"
    
    

    
    

    
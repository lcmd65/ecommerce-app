from flask import Blueprint, request, jsonify
from app.db import database_connection
import app.cache
import json

## chat data store in cache
## chat_data = {id: str, chat: []}

api_blueprint = Blueprint('api_blueprint', __name__)

def extract_information(message):
    """
    call api exctract user's featrues (base model) chat from user text

    Args:
        message (str): user message after prprocessing
    returns:
        features (list)
    """
    pass

def validate(features):
    """
    check the data collection of user's features

    Args:
        features (list): list[dict[feature_name: feature_data]]
    
    returns:
        features_missing
    """
    pass

def prompt_generation_processing(features_missing):
    """
    if the validate return features_missing, in that features_missing != None, generate prompt for continues extraction
    
    Args:
        fetures_missing (list): list[feature_name]
    returns:
        prompt questtion (str): bot question
    """
    pass

def processing(message):
    """
    message overall processing

    Args:
        message (str): user message input

    Returns:
        respone: system bot message output
    """
    features = extract_information(respone)
    while validate(features) == False:
        prompt_generation_processing()
        features = extract_information(respone)

        respone = processing
    return respone
    
            
@api_blueprint.route('/chat_api', methods = ['GET', 'POST'])
def chat():
    """
    chat api

    Returns:
        respone: json(str)
    """
    message = request.json.get('message')
    respone = processing(message)
    return jsonify(respone)

@api_blueprint.route("/description_get", methods = ['GET', 'POST'])
def description_get():
    """
    get item product description view when click detail to product

    Returns:
        description: str
    """
    message = request.json.get('_id') # product id
    client, database = database_connection()
    collection = database["Product"]
    item = collection.find_one({'_id': message})
    client.close()
    return item['description']

@api_blueprint.route("/cart_get", methods = ['GET', 'POST'])
def cart_get():
    """
    get the cart data when click cart icon button

    Returns:
        cart: [id: user_id, [cart_data: data]]
    """
    cart = app.cache.cache.get("cart")
    if cart == None :
        user = app.cache.cache.get("user")
        user_id = user["id"]
        client, database = database_connection()
        collection = database["User_Card"]
        cart = collection.find_one({'id': user_id})
        client.close()
    return jsonify(json.dumps(cart))

@api_blueprint.route("/cart_add", methods = ['GET', 'POST'])
def cart_add():
    """
    cart add one item when event clicked

    Returns:
        bool: result of event item add to db
    """
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
    
    

    
    

    
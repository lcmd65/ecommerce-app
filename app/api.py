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
    message = request.json.get('id') # product id
    client, database = database_connection()
    collection = database["Product"]
    item = collection.find_one({'id': message})
    client.close()
    return item['description']

@api_blueprint.route("/cart_get", methods = ['GET', 'POST'])
def cart_get():
    message = request.json.get('id') # user id
    
    client, database = database_connection()
    collection = database["User_Card"]
    card = collection.find_one({'id': message})
    client.close()
    
    return jsonify(json.dumps(card))
    
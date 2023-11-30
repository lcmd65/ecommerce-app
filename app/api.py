from flask import Blueprint, request, jsonify
from app.db import database_connection

## chat data store in cache
## chat: = {id: str, chat: []}
## user: {id:str, username:str, password: str, email:str, gender: M/F}
## features:
##  //_id
##  //name
##  //description
##  //availability
##  //brand
##  //color
##  //currency
##  //price
##  //avg_rating
##  //review_count
##  //scraped_at
##  //url

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
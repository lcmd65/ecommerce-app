from flask import Blueprint, request, jsonify
import app.cache

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
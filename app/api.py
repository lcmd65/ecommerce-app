from flask import Blueprint, request, jsonify

api_blueprint = Blueprint('api_blueprint', __name__)


def processing(message):
    """_summary_

    Args:
        message (_type_): _description_

    Returns:
        _type_: _description_
    """
    
    respone = message
    return respone
    
            
@api_blueprint.route('/chat_api', methods = ['GET', 'POST'])
def chat():
    message = request.json.get('message')
    respone = processing(message)
    return jsonify(respone)
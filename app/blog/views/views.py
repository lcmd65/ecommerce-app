#blogging main function of nohdata
from flask import (
    Blueprint,
    request,
    render_template,
    redirect,
    jsonify,
    g)
from app.db import database_connection
import app.cache
import json

blog_blueprint = Blueprint('blog_blueprint', __name__)
            
# home page
@blog_blueprint.route("/home",methods = ['GET', 'POST'])
def home():
    from app.auth.models.user import User
    user = json.loads(app.cache.cache.get('user')) # cache get
    print(user) # NULL data user
    
    if request.method == "POST":
        render_template("blog/home.html" ,user_name = user["username"])
    return render_template("blog/home.html", user_name = user["username"])

@blog_blueprint.route("/description_get", methods = ['GET', 'POST'])
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

@blog_blueprint.route("/cart_get", methods = ['GET', 'POST'])
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

@blog_blueprint.route("/cart_add", methods = ['GET', 'POST'])
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

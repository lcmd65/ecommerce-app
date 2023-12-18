#blogging main function of nohdata
from flask import (
    Blueprint,
    request,
    render_template,
    session,
    jsonify)
from app.db import database_connection
import app.cache
import json
import bson

blog_blueprint = Blueprint('blog_blueprint', __name__)
            
# home page
@blog_blueprint.route("/home",methods = ['GET', 'POST'])
def home():
    user = session.get("user")
    cart = session.get("cart")
    app.cache.cache.set("user", user)
    app.cache.cache.set("cart", cart)
     # cache get    
    if request.method == "POST":
        if request.button.get("name") == "button":
            pass
        render_template("blog/home.html" ,user_name = user["username"])
    return render_template("blog/home.html", user_name = user["username"])

@blog_blueprint.route("/description_get", methods = ['GET', 'POST'])
def description_get():
    """
    get item product description view when click detail to product

    Returns:
        description: str
    """
    if request.method == "POST":
        message = request.json.get('item_id') # product id
        if message != None:
            client, database = database_connection()
            collection = database["Product"]
            item = collection.find_one({'_id': bson.ObjectId(message)})
            client.close()
            return jsonify(item['description'])
        else:
            return jsonify("can't find item")

@blog_blueprint.route("/cart_get", methods = ['GET', 'POST'])
def cart_get():
    """
    get the cart data when click cart icon button

    Returns:
        cart: [id: user_id, [cart_data: data]]
    """
    if request.method == "POST":
        cart = app.cache.cache.get("cart")
        if cart == None :
            user = session.get("user")
            user_id = user["id"]
            client, database = database_connection()
            collection = database["User_Card"]
            cart = collection.find_one({'id': user_id})
            client.close()
            return cart
        return cart

@blog_blueprint.route("/cart_add", methods = ['GET', 'POST'])
def cart_add():
    """
    cart add one item when event clicked

    Returns:
        str: information result of event item add to db
    """
    if request.method == "POST":
        item_id = request.json.get('item_id') 
        user = app.cache.cache.get("user")
        user_id = user["id"]
        client, database = database_connection()
        collection = database["User_Cart"]
        collection.update_one(
            {'id': user_id},
            {'$push': {'item': item_id}}  
        )
        client.close()
        return jsonify({'success': True})
    return jsonify({'success': False})

@blog_blueprint.route("/item_get", methods =['GET', 'POST'])
def item_get():
    """
    get all attributes of item

    Returns:
        item:  item dict
    """
    if request.method == "POST":
        item_id = request.json.get('item_id')
        client, database = database_connection()
        collection = database["Product"]
        item = collection.find_one({"_id": bson.ObjectId(item_id)})
        item['_id'] = str(item['_id'])
        client.close()
        return item

@blog_blueprint.route("/item_del", methods =['GET', 'POST'])
def item_del():
    """
    delete item from cart 
    
    Returns:
        item{}:  item dict
    """
    if request.method == "POST":
        item_id = request.json.get('id')
        client, database = database_connection()
        collection = database["Cart"]
        result = collection.delete_one({"_id": bson.ObjectId(item_id)})
        client.close()
        return str(result) 

@blog_blueprint.route("/user_get", methods =['GET', 'POST'])
def user_get():
    """ 
    fetch user dict information

    Returns:
        _type_: _description_
    """
    if request.method == "POST":
        return session.get("user")
    
@blog_blueprint.route("/user_information", methods = ["GET", "POST"])
def user_information():
    """
    render user infor page
    
    Returns:
        _type_: _description_
    """
    user = session.get("user")
    client, database = database_connection()
    collection = database["User_Contact"]
    user_contact = collection.find_one({"id": user["id"]})
    client.close()
    if request.method == "POST":
        return render_template("blog/user.html", user = user, user_contact = user_contact)
    return render_template("blog/user.html", user = user, user_contact = user_contact)
    
            
@blog_blueprint.route('/filtering_redirect', methods=['POST'])
def filtering_redirect():
    # Retrieve form data
    selected_values_json = request.form.get('selectedValues')

    # Parse the JSON string to a Python object
    selected_values = json.loads(selected_values_json) if selected_values_json else {}

    # Process the selected values and perform filtering (replace this with your logic)
    brand_values = selected_values.get('brand', [])
    price_values = selected_values.get('price', [])
    availability_values = selected_values.get('availability', [])
    session["filtering"] = {
        "BRAND": brand_values,
        "PRICE": price_values ,
        "AVAI": availability_values
    }
    
@blog_blueprint.route('/filtering', methods=['POST'])
def filtering():
    if request.method == "POST":
        filter_data = session.get("filtering")
        client, database = database_connection()
        
        collection = database["Product"]
        
        query = {
            "brand": filter_data["BRAND"],
            "availability": filter_data["AVAI"]
        }

        for a in filter_data["PRICE"]:
            query["price"] = {"$gt": a, "$lt": a + 50}

        item = list(collection.find(query))
        client.close()
        return item




    

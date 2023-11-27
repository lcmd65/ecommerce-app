# authentication function of nohg.application
from flask import (\
    Blueprint,
    request,
    jsonify,
    render_template,
    redirect,
    url_for,
    current_app,
    g)
import app
from app import db
from app.auth.controllers.controllers import authentication
from app.cache import cache
from pymongo import MongoClient
from pymongo.server_api import ServerApi
from flask_caching import Cache
import json
from bson import json_util
import re

auth_blueprint = Blueprint('auth_blueprint', __name__)

def count_braces(input_str):
    open_braces = input_str.count('{')
    close_braces = input_str.count('}')
    return open_braces, close_braces

@auth_blueprint.route("/login",  methods = ['GET', 'POST'])
def login():
    try:
        error = None
        if request.method == "POST":
            username = request.values['user'] 
            password = request.values['pass']
            user = User(username, password, None, None, None)
            data_base = db.DB()
            data_base.getUser(user)
            bool = data_base.userAuthentication(username, password)
            if bool == True:
                data_base.parsingUser()
                model = dbModel(data_base._user)
                cache.set('database', json.dumps(model.__dict__()))
                return redirect("/home")
            else: 
                return render_template("auth/login.html", error="Invalid username or password.")
    except:
        pass
    return render_template('auth/login.html', error = error)

@auth_blueprint.route("/forgot",  methods = ['GET', 'POST'])
def forgotPassword():
    try:
        error = None
        if request.method == "POST":
            if request.form.get("button") == "back":
                return render_template("auth/login.html", error = None)
            else:
                username = request.values['user'] 
                email = request.values['email']
                new_pass = request.values['new_password']
                confirm_pass = request.values['confirm_new_password']
                if new_pass == confirm_pass:
                    user = json.loads(app.cache.cache.get('database'))
                    data_base = db.DB()
                    data_base.getUser(user)
                    boolean = data_base.userAuthenticationChange(username, email, new_pass)
                    model = dbModel(data_base._user)
                    cache.set('database', json.dumps(model.__dict__()))
                    if boolean == True:
                        return render_template("auth/forgot.html", error="Success change")
                else:
                    return render_template("auth/forgot.html", error="Wrong username or email")
    except: 
        pass
    return render_template("forgot.html", error = error)
    

@auth_blueprint.route("/register", methods = ['GET', 'POST'])
def register():
    try:
        if request.method == "POST":
            username = request.values['user'] 
            password = request.values['pass']
            confirm_password = request.values['confirm_password']
            email = request.values['email'] 
            id = request.values['id']
            gender = request.values['gender']
            if confirm_password == password:
                user = json.loads(app.cache.cache.get('database'))
                data_base = db.DB()
                data_base.getUser(user)
                boolean = data_base.addUserMongoDB(username, email, password, id , gender)
                model = dbModel(data_base._user)
                app.cache.cache.set('database', json.dumps(model.__dict__()))
                if boolean == True:
                    return render_template("auth/register.html", error = "Success")
                else:   
                    return render_template("auth/register.html", error = "Can't register new user")   
        return render_template("auth/register.html", error = None)
    except Exception as e:
        return render_template("auth/register.html", error = e)

@auth_blueprint.route("/product", methods=['GET','POST'])
def product():
    from app.auth.models.product import Product
    product_database = Product()
    data = product_database.to_dict()
    return str(data).replace("'", "\"")

@auth_blueprint.route("/ecommerce",  methods = ['GET','POST'])
def ecommerce():
    try:
        if request.method == "POST":
            button_name = request.form.get("button")
            if button_name == "login":
                return redirect('/login')
            elif button_name == "register":
                return redirect('/register')
            return render_template("base.html")
        return render_template("base.html")
    except Exception as e:
        print(e)
        


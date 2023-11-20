#blogging main function of nohdata
from flask import Blueprint
from flask import (
    request,
    render_template,
    redirect,
    jsonify,
    g)
import app.cache
import json
import openai
from app import db
from app.auth.models.models import User

blog_blueprint = Blueprint('blog_blueprint', __name__)
            
# home page
@blog_blueprint.route("/home",methods = ['GET', 'POST'])
def home():
    model = json.loads(app.cache.cache.get('database')) # cache get
    user = User(None, None, None, None, None) # NULL data user
    user.initFromUser(model) # init User data from cache
    if request.method == "POST":
        button_value = request.form.get("button")
        if button_value == "chatbox":
            return redirect("/chatbox")
        elif button_value == "chatbot":
            return redirect("/chatbot")
        else:
            return redirect("/speechtotext")
    return render_template("blog/home.html", app_username = user.username,\
        app_image = user.image)

@blog_blueprint.route("/chatbox", methods = ['GET', 'POST'])
def homeChatbox():
    tree, button = None, None
    model = json.loads(app.cache.cache.get('database'))
    user = User(None, None, None, None, None)
    user.initFromUser(model)
    data_base = db.DB()
    data_base.getUser(user)
    if request.method == "POST":
        id = request.form.get("option")
        for item in data_base._user.requests:
            if item["_id"] == id:
                tree = item
                break
        if tree != None:
            return render_template("blog/chatbox.html", user_name= data_base._user.username,\
            user_image = data_base._user.image,\
            tree_request = data_base._user.requests,\
            item_request = tree,\
            item_new = None)
        elif tree == None:
            button = request.form.get("button")
            if button == "init":
                return render_template("blog/chatbox.html", user_name= data_base._user.username,\
                    user_image = data_base._user.image,\
                    tree_request = data_base._user.requests,\
                    item_request = None,\
                    item_new = button)
            elif button =="init_request":
                subject_text = request.values["subject-entry"]
                request_text = request.values["question-entry"]
                data_base.pushRequestToMongo(user.id, subject_text, request_text)
                return render_template("blog/chatbox.html", user_name= data_base._user.username,\
                    user_image = data_base._user.image,\
                    tree_request = data_base._user.requests,\
                    item_request = None,\
                    item_new = None)
            elif button == "destroy":
                return render_template("blog/chatbox.html", user_name= data_base._user.username,\
                    user_image = data_base._user.image,\
                    tree_request = data_base._user.requests,\
                    item_request = None,\
                    item_new = None)
    return render_template("blog/chatbox.html", user_name= data_base._user.username,\
            user_image = data_base._user.image,\
            tree_request = data_base._user.requests,\
            item_request = None,\
            item_new = None)



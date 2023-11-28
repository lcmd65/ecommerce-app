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

blog_blueprint = Blueprint('blog_blueprint', __name__)
            
# home page
@blog_blueprint.route("/home",methods = ['GET', 'POST'])
def home():
    from app.auth.models.user import User
    user = json.loads(app.cache.cache.get('user')) # cache get
    user_model = User(user) # NULL data user
    
    if request.method == "POST":
        render_template("blog/home.html")
    return render_template("blog/home.html")



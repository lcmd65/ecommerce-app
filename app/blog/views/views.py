from flask import blueprints, request, render_template
from cache import cache
from auth.models.models import User

blog_blueprint = blueprints("blog_blueprint")

@blog_blueprint.route("/home")
def home():
    user = cache.get("user")
    
    return render_template("home.html")
    pass
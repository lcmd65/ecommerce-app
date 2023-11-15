from flask import blueprints, request, render_template
from cache import cache
from auth.models.models import User

api_auth = blueprints("api_auth")

@api_auth.route("\base", request = "POST")
def base():
    pass

@api_auth.route("\login", request = "POST")
def login():
    from app.auth.controllers.controllers import authentication
    error = None
    username = request.get("username")
    password = request.get("password")
    if request.method == "POST":
        try:
            if authentication(username, password) == True:
                user = User()
                user.user_parsing(username, password)
                cache.set["user"] = user.to_dict()
            return render_template("\home")
        except Exception as e:
            error = e
            return render_template("login.html", error)
    return render_template("login.html", error)
        
@api_auth.route("\sign_up", request = "POST")
def register():
    pass



        
    
    
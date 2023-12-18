# authentication route of application
from flask import (\
    Blueprint,
    request,
    jsonify,
    render_template,
    redirect,
    url_for,
    current_app,
    session,
    g)

import app.cache

auth_blueprint = Blueprint('auth_blueprint', __name__)

@auth_blueprint.route("/product", methods=['GET','POST'])
def product():
    from app.auth.models.product import Product
    product_database = Product()
    data = product_database.to_dict()
    return str(data).replace("'", "\"")

# base route define
@auth_blueprint.route("/ecommerce",  methods = ['GET','POST'])
def ecommerce():
    """
    Base window of ecommerce app

    Returns:
        index.html
    """
    user_features ={
            'clothing': None,
            'brand': None,
            'style':None,
            'material': None,
            'activity': None,
            'feature': None,
            'age': None
        }
    filtering = []
    if request.method == "POST":
        session["user_features"] = user_features
        session["filter"] = filtering
        button_name = request.form.get("button")
        if button_name == "login": return redirect('/login')
        elif button_name == "register": return redirect('/register')
        return render_template("index.html")
    session["user_features"] = user_features
    return render_template("index.html")
        


@auth_blueprint.route("/login",  methods = ['GET', 'POST'])
def login():
    """
    Login route render template
    Returns:
       login.html
    """
    error = None
    try:
        from app.auth.controllers.controllers import authentication
        if request.method == "POST":
            if request.form.get("button") == "back":
                return redirect('/ecommerce')
            else:
                username = request.values['user'] 
                password = request.values['pass']
                boolean = authentication(username, password)
                if boolean == True:
                    return redirect("/home")
                else: 
                    return render_template("auth/login.html", error="Invalid username or password.")
        elif request.method == "GET":
            return render_template('auth/login.html', error = error)
    except Exception as e:
        print('error oocur when login: ', e)
    return render_template('auth/login.html', error = error)

# route forgot
@auth_blueprint.route("/forgot",  methods = ['GET', 'POST'])
def forgot():
    """
    forgot password route render template
    
    Returns:
       forgot.html
    """
    error = None
    try:
        from app.auth.controllers.controllers import confirm_authentication
        if request.method == "POST":
            if request.form.get("button") == "back":
                return render_template("auth/login.html", error = None)
            else:
                username = request.values['user'] 
                email = request.values['email']
                new_pass = request.values['new_password']
                confirm_pass = request.values['confirm_new_password']
                boolean = confirm_authentication(username, email, new_pass, confirm_pass)
                if boolean == True:
                    return render_template("auth/forgot.html", error="successful")
                else:
                    return render_template("auth/forgot.html", error="Wrong username or email")
    except Exception as e:
        print('error oocur when login: ', e)
    return render_template("auth/forgot.html", error = error)
    

@auth_blueprint.route("/register", methods = ['GET', 'POST'])
def register():
    """
    Register user route render template
    
    Returns:
       register.html
    """
    try:
        from app.auth.controllers.controllers import register_user
        if request.method == "POST":
            if request.form.get("button") == "back":
                return redirect('/ecommerce')
            else:
                username = request.values['user'] 
                password = request.values['pass']
                confirm_password = request.values['confirm_password']
                email = request.values['email']
                user_id = request.values['id']
                gender = request.values['gender']
                role = "0"
                if confirm_password == password:
                    boolean = register_user(username, email, password, user_id , gender, role)
                    if boolean == True:
                        return render_template("auth/register.html", error = "Success")
                    else:   
                        return render_template("auth/register.html", error = "Can't register new user")  
        return render_template("auth/register.html", error = None)
    except Exception as e:
        return render_template("auth/register.html", error = e)


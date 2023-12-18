import os
from flask import (Flask, 
                   Blueprint, 
                   render_template, 
                   redirect,request, 
                   url_for)
from flask_sqlalchemy import SQLAlchemy
from flask_caching import Cache
import app.cache as cache_path
from app.api import api_getting
from openai import OpenAI
import warnings
warnings.filterwarnings("ignore")

def create_app(test_config=None):
    # Set up the OpenAI API
    openai_api_key = os.environ.get("OPENAI_API_KEY")
    if openai_api_key is None:
        openai_api_key = api_getting()
    openai_client = OpenAI(api_key=openai_api_key)
    
    app = Flask(__name__, instance_relative_config=True)
    # create and configure the app
    app.config.from_mapping(
        SECRET_KEY='dev1911007',
        DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
        CACHE_TYPE = 'FileSystemCache',
        CACHE_DIR = 'cache',
        CACHE_THRESHOLD = 100000,
    )
    app.config.from_pyfile("config.py")
    from .auth.views.views import auth_blueprint
    from .blog.views.views import blog_blueprint
    from .api import flask_api
    app.register_blueprint(auth_blueprint)
    app.register_blueprint(blog_blueprint)
    app.register_blueprint(flask_api)
    cache_path.cache.init_app(app)
    app.config["OPENAI_CLIENT"] = openai_client
    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # a base page
    @app.route('/')
    def main():
        return redirect(url_for('auth_blueprint.ecommerce'))
            
    @app.route('/intro', methods = ['GET','POST'])
    def intro():
        if request.method == 'POST':
            return redirect(url_for('auth_blueprint.ecommerce'))
        return render_template("intro.html")
    
    return app





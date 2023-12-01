import os
import cache
import json
import pickle
import ssl
from flask import (Flask, 
                   Blueprint, 
                   render_template, 
                   redirect,request, 
                   url_for)
from flask_sqlalchemy import SQLAlchemy
from flask import g, session
from flask_caching import Cache

def create_app(test_config=None):
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
    cache.cache.init_app(app)
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
    
    return app





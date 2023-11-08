from flask import Flask, blueprints
from flask import Cache
import gc

if __name__ == "__main__":
    app = Flask(__name__)
    app.iter_blueprints()
    
    
    return app
    
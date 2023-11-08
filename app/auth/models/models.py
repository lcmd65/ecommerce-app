from flask import db
import app.auth.controllers.controllers


class User(db.Model):
    def __init__(self):
        self.username = db.Model("usesname")
        self.password = db.Model("password")
        self.gender = None
        self.image = None
        self.visited = []
        
        app.auth.controllers.controllers.user_parsing(self, self.username, self.password)
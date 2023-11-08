from flask import blueprints, request

api_auth = blueprints("api_auth")

@api_auth.route("\login", request = "POST")
def login():
    username = request.get("username")
    password = request.get("password")
    
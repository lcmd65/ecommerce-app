from app.blog.models.models import UserCard, UserChat
import app.cache
import json

def chat_to_cache(chat_message):
    if app.cache.cache.get("chat") != None:
        chat_data = app.cache.cache.get("chat")
        chat_data.chat.append(chat_message)
        app.cache.cache.set("chat", json.dumps(chat_data.to_dict()))
    else:
        chat_data = UserChat()
        chat_data.append(chat_message)
        app.cache.cache.set("chat", json.dumps(chat_data.to_dict()))


def to_database():
    pass
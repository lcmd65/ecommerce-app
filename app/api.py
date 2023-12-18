from flask import Blueprint, request, jsonify, session, current_app
from app.db import database_connection
import gensim 
import numpy as np
from bson import ObjectId
from fuzzywuzzy import fuzz
import spacy
import openai
from pymongo import MongoClient
from openai import OpenAI
import os
import json
import random
import warnings
warnings.filterwarnings("ignore")

flask_api = Blueprint('flask_api', __name__)


def api_getting():
    """
    getting api openai key

    Returns:
        api key: str
    """
    with open("app/schema.json", "r") as file:
        uri = json.load(file)
    client = MongoClient(uri["mongo_uri"])
    client.admin.command('ping')
    db = client["Api"]
    collection = db["api"]
    documents = collection.find()
    api_key = None
    for item in documents:
        if item['api'] == 'datathon-service':
            api_key = item['api-key']
            break
    client.close()
    return api_key

def extract_information(message):
    """
    call api exctract user's featrues (base model) chat from user text

    Args:
        message (str): user message after prprocessing
    returns:
        features (list)
    """
    user_features = session.get("user_features")
    nlp_ner = spacy.load("model/ner")
    doc = nlp_ner(message)
     # Extract named entities and their information
    ner_info = []
    for ent in doc.ents:
        ner_info.append({
            'text': ent.text,
            'start': ent.start_char,
            'end': ent.end_char,
            'label': ent.label_
        })
    for item in ner_info:
        if item['label'].lower() != 'color':
            if user_features[item['label'].lower()] == None:
                user_features[item['label'].lower()] = []
                user_features[item['label'].lower()].append(item['text'])
            else:
                user_features[item['label'].lower()].append(item['text'])
    session["user_features"] = user_features

def validate():
    """
    check the data collection of user's features

    Args:
        features (list): list[dict[feature_name: feature_data]]
    
    returns:
        features_missing
    """
    user_features = session.get("user_features")
    missing_features = [key for key, value in user_features.items() if value is None]
    print(missing_features)
    return missing_features

def prompt_generation_processing(openai_client, features_missing):
    """
    if the validate return features_missing, in that features_missing != None, generate prompt for continues extraction
    
    Args:
        features_missing (list): list[feature_name]
    returns:
        prompt questtion (str): bot question
    """
    product_recommend = recommend_content_based()
    if features_missing != []:
        number = random.choice([x for x in range(1, len(features_missing))])
        random_items = random.choices(features_missing, k=number)
        missing_text = ", ".join(random_items)
        if product_recommend != []:
            # Convert string IDs to ObjectId if needed
            client, database = database_connection()
            collection =database["Product"]
            object_id_list = [ObjectId(id_str["_id"]) for id_str in product_recommend]
            # Query for documents with matching _id values
            product_query = list(collection.find({"_id": {"$in": object_id_list}}))
            product = []
            for prod in product_query:
                product.append({"_id": str(prod['_id']), "name": prod['name'], "price": prod['price']})
            product_name = [x['name'] for x in product_query]
            completion = openai_client.chat.completions.create(
                model = "gpt-3.5-turbo",
                messages =[
                    {"role": "system", "content": "You are a seller"},
                    {"role": "assistant", "content" :"Please describe the product you are looking for"},
                    {"role": "system", "content": f"let ask only 1 question shortly about {missing_text} of product user want"},
                    {"role": "system", "content": f"let generate recommend shorly with max token = 600, for threse product: {product_name} .Convince customers to increase their purchasing ability as much as possible"}
                ]
            )
            respone = completion.choices[0].message.content
            return {"respone": [respone], "recommend": product}
        else:
            completion = openai_client.chat.completions.create(
                model = "gpt-3.5-turbo", 
                messages =[
                    {"role": "system", "content": "You are a seller"},
                    {"role": "assistant", "content" :"Please describe the product you are looking for"},
                    {"role": "system", "content": f"let ask question shortly about {missing_text} of product user want"},
                ]
            )
            respone = completion.choices[0].message.content
            return {"respone": [respone], "recommend": None}
    else:
        if product_recommend != []:
            # Convert string IDs to ObjectId if needed
            client, database = database_connection()
            collection =database["Product"]
            object_id_list = [ObjectId(id_str) for id_str in product_recommend]
            # Query for documents with matching _id values
            product_query = list(collection.find({"_id": {"$in": object_id_list}}))
            product = []
            for prod in product_query:
                product.append({"_id": str(prod['_id']), "name": prod['name'], "price": prod['price']})
            product_name = [x['name'] for x in product_query]

            completion = openai_client.chat.completions.create(
                    model = "gpt-3.5-turbo",
                    messages=[
                        {"role": "system", "content": "You are a seller"},
                        {"role": "assistant", "content" :"Please describe the product you are looking for"},
                        {"role": "system", "content": f"let ask quesion shortly about another attribute of product user want"},
                        {"role": "system", "content": f"let generate recommend shorly with max token =  600 for threse product: {product_name} .Convince customers to increase their purchasing ability as much as possible"}
                    ]
                )
            respone = completion.choices[0].message.content
            return {"respone": [respone], "recommend": product}
        else:
            completion = openai_client.chat.completions.create(
                    model = "gpt-3.5-turbo",
                    messages=[
                        {"role": "system", "content": "You are a seller"},
                        {"role": "assistant", "content" :"Please describe the product you are looking for"},
                        {"role": "system", "content": f"generate 1 ask quesion for user about another attribute of product user want"},
                    ]
                )
            respone = completion.choices[0].message.content
            return {"respone": [respone], "recommend": None}
    
def processing(openai_client, message):
    """
    message overall processing
    
    Args:
        message (str): user message input

    Returns:
        respone: system bot message output
    """
    extract_information(message)
    missing_features = validate()
    result = prompt_generation_processing(openai_client, missing_features)
    return result

# search message processing    
def processing_search_message(message):
    """
    search bar

    Args:
        message (Str)):message input

    Returns:
        product []: render filtering
    """
    client, database = database_connection()
    collection = database["Product"].find()
    score_list = []
    desired_size = 10

    for item in collection:
        # Compare the input message with product name and description
        similarity_score_name = fuzz.token_set_ratio(message, item["name"])
        similarity_score_des = fuzz.token_set_ratio(message, item["description"])

        # Take the maximum similarity score between name and description
        similarity_score = max(similarity_score_name, similarity_score_des)
        new_element = {"_id": str(item["_id"]), "score": similarity_score}

        if len(score_list) < desired_size or new_element["score"] >= score_list[-1]["score"]:
            score_list.append(new_element)
            score_list.sort(key=lambda x: x["score"], reverse=True)
            score_list = score_list[:desired_size]
    result = [x["_id"] for x in score_list[:desired_size]]
    client.close()
    return result

# recommendation model
def recommend_model_based():
    """
    model-based vector recommendation
    """
    pass

# recommendation querry content base
def recommend_content_based():
    """
    content-based querry recommendation
    """
    threshold = 0.3
    product = []
    features_data = session.get("user_features")
    client, database = database_connection()
    collection = database["Product_Profile"]
    for item in collection.find():
        item_score, num = 0,0
        for index in ['clothing','brand', 'style', 'material', 'activity', 'age', 'feature']:
            if (features_data.get(index) is not None) and (item.get(index) is not None) and (item.get(index) is not []):
                field_value = item.get(index)
                max_score = 0
                for feature_field in features_data[index]:
                    try:
                        ratio = fuzz.ratio(feature_field.lower(), field_value.lower())
                        max_score = max(max_score, ratio)
                        item_score += max_score
                        num+= 1
                    except:
                        for field_db_value in field_value:
                            ratio = fuzz.ratio(feature_field.lower(), field_db_value.lower())
                            max_score = max(max_score, ratio)
                        item_score += max_score
                        num+= 1
        if num > 0:
            item_score /= max([num, 1])
        
        # If the ratio is above the threshold, consider it a match
        if item_score >= threshold:
            if len(product) <3:
                 product.append({
                    "_id": str(item["_id"]),
                    "score": item_score
                })
            elif item_score > product[-1]["score"]:
                product.append({
                    "_id": str(item["_id"]),
                    "score": item_score
                })
                product = sorted(product, key=lambda x: x["score"], reverse=True)
                product.pop()
    client.close()
    return product
    
# RESTful API flask
@flask_api.route('/chat_api', methods = ['GET', 'POST'])
def chat():
    """
    chat api
    
    Returns:
        respone: json(str)
    """
    if request.method == "POST":
        openai_client = current_app.config["OPENAI_CLIENT"]
        message = request.json.get('message')
        respone = processing(openai_client, message)
        return respone


@flask_api.route("/search_2vec", methods = ["GET", "POST"])
def search_2vec():
    """
    search api
    """
    if request.method == "POST":
        message = request.json.get('search_message')
        return processing_search_message(message)

@flask_api.route("/product_get", methods = ["GET", "POST"])
def product_get():
    """
    search api
    """
    if request.method == "POST":
        id_list = request.json.get('list_id')
        client, database = database_connection()
        collection = database["Product"]
        id_list = [ObjectId(x) for x in id_list]
        result = collection.find({"_id": {"$in": id_list}})

        # Convert the result to a list of dictionaries
        list_data = [
            {
                "_id": str(item["_id"]),
                "name": item["name"],
                "price": item["price"],
                "currency": item["currency"],
                "brand": item["brand"],
            }
            for item in result
        ]

        # Close the database connection
        client.close()
        return list_data
    return jsonify({"error": "Invalid request method"}), 405
from guppy import hpy

<<<<<<< HEAD
h = hpy()
print(h.heap())
=======
## chat data store in cache
## chat: = {id: str, chat: []}
## user: {id:str, username:str, password: str, email:str, gender: M/F}
## features:
##  //_id
##  //name
##  //description
##  //availability
##  //brand
##  //color
##  //currency
##  //price
##  //avg_rating
##  //review_count
##  //scraped_at


def prompt_generation_processing(features_missing):
    """
    if the validate return features_missing, in that features_missing != None, generate prompt for continues extraction
    
    Args:
        fetures_missing (list): list[feature_name]
    returns:
        prompt questtion (str): bot question
    """
    openai.api_key = api_getting()
    product_recommend = None
    missing_text = ", ".join(features_missing)

    if features_missing != []:
        completion = openai.ChatCompletion.create(
            model="gpt-4-1106-preview",
            messages=[
                {"role": "user", "content": f"generate ask question for user about: {missing_text}"},
                {"role": "user", "content": f"recommend this product: {str(product_recommend)}"}
            ]
        )
        respone = completion.choices[0].message.content
        return respone
    else:
        completion = openai.ChatCompletion.create(
                model="gpt-4-1106-preview",
                messages=[
                    {"role": "system", "content": "".join(["generate ask quesion for user about: ", missing_text]) }
                ]
            )
        respone = completion.choices[0].message.content
        return jsonify(respone)
    

def api_getting():
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
    return api_key
if __name__ =="__main__":
   print(prompt_generation_processing(["clothing"]))
>>>>>>> 77412cbd1e225cde396b5647935cc202b5f9ee74

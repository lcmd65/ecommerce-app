import pandas as pd 
from app.db import database_connection

if __name__ == "__main__":
    df = pd.read_excel("test/adidas_nikes_products_snaphost_data.xlsx")
    client, database = database_connection()
    collection = database["Product"]
    
    for index, element in df.iterrows():
        query = {"name": element["name"]}
        update_data = {"$set": {"images": element["images"]}}  # Update images field
        collection.update_one(query, update_data)
    
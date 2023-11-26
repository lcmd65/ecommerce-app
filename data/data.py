import pandas as pd
from pymongo import MongoClient

df = pd.read_csv("data/adidas_nikes_products_snaphost_data.csv")
# Assuming you have a DataFrame named 'df'
# Replace the following information with your MongoDB connection details
mongo_uri = "mongodb+srv://datlemindast:Minhdat060501@cluster0.ixcliyp.mongodb.net/?retryWrites=true&w=majority"
database_name = "Datathon"
collection_name = "Product"

# Connect to MongoDB
def main():
    client = MongoClient(mongo_uri)
    database = client[database_name]
    collection = database[collection_name]

    # Convert the DataFrame to a list of dictionaries with column names as keys
    data_list = df.to_dict(orient='records')

    # Insert the data into MongoDB
    collection.insert_many(data_list)

    # Close the MongoDB connection
    client.close()

if __name__ == "__main__":
    main()
    
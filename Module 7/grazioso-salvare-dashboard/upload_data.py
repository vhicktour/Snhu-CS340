import pandas as pd
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

# MongoDB connection string
uri = "mongodb+srv://victoroudeh:naijaboy007@vudehdb.jqn22qz.mongodb.net/?retryWrites=true&w=majority&appName=VUDEHDB"

# Create a new client and connect to the server
client = MongoClient(uri, server_api=ServerApi('1'))
db = client['victorDB']
collection = db['shelter_outcomes']

# Load CSV data
csv_file_path = '/Users/victorudeh/Desktop/Snhu CS340/Module 7/grazioso-salvare-dashboard/data/aac_shelter_outcomes.csv'
data = pd.read_csv(csv_file_path)

# Insert data into MongoDB
collection.drop()  # Clear existing data
collection.insert_many(data.to_dict('records'))

print("Data loaded into MongoDB successfully.")

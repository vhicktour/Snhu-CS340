# insert_csv_to_mongodb.py

# Import necessary libraries
import pandas as pd  # Pandas for data manipulation
from pymongo import MongoClient, errors  # PyMongo for MongoDB interaction and error handling

# MongoDB connection details
username = "victoroudeh"
password = "dpa2Vmz631UCUNYF"
cluster_url = "victordb.w6hvjsj.mongodb.net"
database_name = "victorDB"
collection_name = "animals"

# Construct the MongoDB connection string
connection_string = f"mongodb+srv://{username}:{password}@{cluster_url}/?retryWrites=true&w=majority&appName=victorDB"

# Attempt to connect to MongoDB
try:
    # Create a MongoClient instance with a 5-second server selection timeout
    client = MongoClient(connection_string, serverSelectionTimeoutMS=5000)
    
    # Access the specified database and collection
    database = client[database_name]
    collection = database[collection_name]
    
    # Trigger an exception if the server is not accessible
    client.server_info()
    print("Connected to MongoDB")
except errors.ServerSelectionTimeoutError as err:
    # Print the error message if the connection fails
    print(f"Failed to connect to server: {err}")
    client = None

# Read the CSV file into a DataFrame
csv_file_path = "aac_shelter_outcomes.csv"  # Ensure this path is correct
df = pd.read_csv(csv_file_path)

# Convert the DataFrame to a list of dictionaries
data_dict = df.to_dict("records")

# Insert data into MongoDB if the client is connected
if client:
    try:
        # Insert the list of dictionaries into the collection
        collection.insert_many(data_dict)
        print(f"Inserted {len(data_dict)} records into MongoDB")
    except errors.BulkWriteError as err:
        # Print the error message if the bulk insert fails
        print(f"Failed to insert documents: {err}")
else:
    # Print a message if the client is not connected
    print("No connection to MongoDB")

# crud.py

# Import the MongoClient class from pymongo to interact with MongoDB
from pymongo import MongoClient

class AnimalShelter:
    """
    This class handles interactions with the MongoDB database.
    It provides methods to read data from the database.
    """
    def __init__(self):
        """
        Initialize the AnimalShelter class with MongoDB connection details.
        """
        # MongoDB connection details
        username = "victoroudeh"
        password = "dpa2Vmz631UCUNYF"
        cluster_url = "victordb.w6hvjsj.mongodb.net"
        database_name = "victorDB"
        collection_name = "animals"

        # Construct the connection string for MongoDB
        connection_string = f"mongodb+srv://{username}:{password}@{cluster_url}/?retryWrites=true&w=majority&appName=victorDB"
        
        # Create a MongoClient instance to connect to the MongoDB server
        self.client = MongoClient(connection_string)
        
        # Access the specified database and collection
        self.db = self.client[database_name]
        self.collection = self.db[collection_name]

    def read(self, query):
        """
        Retrieve documents from the MongoDB collection based on the query.
        
        Parameters:
        query (dict): The query to filter documents from the collection.

        Returns:
        list: A list of documents that match the query.
        """
        try:
            # Execute the query and convert the cursor to a list
            documents = self.collection.find(query)
            data = [doc for doc in documents]
            
            # Debug: Print the retrieved data
            print(f"Data retrieved from MongoDB: {data}")
            
            return data
        except Exception as e:
            # Print the error message if an exception occurs
            print(f"Error retrieving documents: {e}")
            return []

    def close_connection(self):
        """
        Close the connection to the MongoDB server.
        """
        self.client.close()

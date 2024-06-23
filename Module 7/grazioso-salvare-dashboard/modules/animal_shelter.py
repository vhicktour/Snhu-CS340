from pymongo import MongoClient
from pymongo.server_api import ServerApi

class AnimalShelter:
    def __init__(self, username, password):
        uri = f"mongodb+srv://{username}:{password}@vudehdb.jqn22qz.mongodb.net/?retryWrites=true&w=majority&appName=VUDEHDB"
        self.client = MongoClient(uri, server_api=ServerApi('1'))
        self.database = self.client['victorDB']
        self.collection = self.database['shelter_outcomes']
    
    def read(self, query, limit=0):
        return list(self.collection.find(query).limit(limit))

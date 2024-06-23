from pymongo import MongoClient

class AnimalShelter:
    """ CRUD operations for Animal collection in MongoDB """

    def __init__(self, username, password, host, port, db, collection):
        """ Initialize the MongoClient and the database and collection names. """
        self.client = MongoClient(f'mongodb://{username}:{password}@{host}:{port}')
        self.database = self.client[db]
        self.collection = self.database[collection]

    def create(self, data):
        """ Insert a document into the collection. """
        if data is not None:
            result = self.collection.insert_one(data)
            return True if result.acknowledged else False
        else:
            raise Exception("Nothing to save, because data parameter is empty")

    def read(self, query):
        """ Query for documents in the collection. """
        if query is not None:
            cursor = self.collection.find(query)
            return [doc for doc in cursor]
        else:
            raise Exception("Query parameter is empty")

# Example usage
if __name__ == "__main__":
    USER = 'aacuser'
    PASS = 'VUDEHSNHUCS340'
    HOST = 'nv-desktop-services.apporto.com'
    PORT = 31593
    DB = 'AAC'
    COL = 'animals'

    shelter = AnimalShelter(USER, PASS, HOST, PORT, DB, COL)
    sample_data = {"animal_id": "A123456", "name": "Fido", "breed": "Labrador"}
    print(shelter.create(sample_data))  # True if successful
    print(shelter.read({"animal_id": "A123456"}))  # Should return the document with animal_id A123456

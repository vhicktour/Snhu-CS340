from pymongo import MongoClient
from pymongo.errors import ConnectionFailure

class AnimalShelter:
    def __init__(self, host, port, username, password):
        try:
            self.client = MongoClient(
                host=host,
                port=int(port),
                username=username,
                password=password,
                authSource='admin'
            )
            self.db = self.client['AAC']
        except ConnectionFailure as e:
            print(f"Could not connect to MongoDB: {e}")

    def create(self, data):
        if data is not None:
            insert_result = self.db.outcomes.insert_one(data)
            return insert_result.acknowledged
        else:
            raise Exception("Nothing to save, because data parameter is empty")

    def read(self, query):
        if query is not None:
            cursor = self.db.outcomes.find(query)
            return [doc for doc in cursor]
        else:
            raise Exception("Nothing to read, because query parameter is empty")

    def update(self, query, update_data):
        if query is not None:
            update_result = self.db.outcomes.update_many(query, {"$set": update_data})
            return update_result.modified_count
        else:
            raise Exception("Nothing to update, because query parameter is empty")

    def delete(self, query):
        if query is not None:
            delete_result = self.db.outcomes.delete_many(query)
            return delete_result.deleted_count
        else:
            raise Exception("Nothing to delete, because query parameter is empty")

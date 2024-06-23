# Grazioso Salvare CRUD Operations BY VICTOR UDEH

## Purpose
This Python module provides CRUD (Create, Read, Update, Delete) operations for the Grazioso Salvare project, allowing interaction with the MongoDB database containing animal shelter data.

## Usage
### MongoDB Driver
We use `pymongo` as the Python driver for MongoDB due to its ease of use and comprehensive documentation.

### CRUD Class
The `AnimalShelter` class provides the following methods:
- `create(data)`: Inserts a document into the database.
- `read(query)`: Queries documents from the database.
- `update(query, update_data)`: Updates documents in the database.
- `delete(query)`: Deletes documents from the database.

### Example
Here's how to use the CRUD class:

```python
from crud import AnimalShelter

# Connection details
MONGO_HOST = 'nv-desktop-services.apporto.com'
MONGO_PORT = 31593
MONGO_USER = 'aacuser'
MONGO_PASS = 'VUDEHSNHUCS340'

# Instantiate the AnimalShelter class
shelter = AnimalShelter(MONGO_HOST, MONGO_PORT, MONGO_USER, MONGO_PASS)

# Create a new document
new_animal = {
    "age_upon_outcome_in_weeks": 12,
    "animal_type": "Dog",
    "breed": "Labrador Retriever Mix",
    "color": "Black/White",
    "date_of_birth": "2021-04-20",
    "outcome_type": "Adoption"
}
print("Create:", shelter.create(new_animal))

# Read documents with limited output
query = {"animal_type": "Dog"}
results = shelter.read(query)
limited_results = results[:10]  # Limiting output to the first 10 documents
for doc in limited_results:
    print(doc)

# Update documents
update_query = {"animal_type": "Dog"}
update_data = {"color": "Black/White/Brown"}
print("Update:", shelter.update(update_query, update_data))

# Delete documents
delete_query = {"animal_type": "Dog"}
print("Delete:", shelter.delete(delete_query))

import pymongo

DB_NAME = "api"
COLLECTION_NAME = "recipies"
CONNECTION_STRING = "mongodb://localhost:27017" #local mongodb instance currently unsecure

DATA = {
    '_id': 2,
    'name': 'recipe-1',
    'description': 'test data',
    'oils': [
        {'olive': .66},
        {'coconut': .34}
    ],
    'liquid': 124,
    'lye': 56.3,
    'weight': 800
}

def create():
    client = pymongo.MongoClient(CONNECTION_STRING)
    try:
        client.server_info() # validate connection string
    except pymongo.errors.ServerSelectionTimeoutError:
        raise TimeoutError("Invalid API for MongoDB connection string or timed out when attempting to connect")

    db = client[DB_NAME]
    col = db[COLLECTION_NAME]
    response = col.insert_one(DATA)
    print(response.inserted_id)

def delete():
    client = pymongo.MongoClient(CONNECTION_STRING)
    try:
        client.server_info() # validate connection string
    except pymongo.errors.ServerSelectionTimeoutError:
        raise TimeoutError("Invalid API for MongoDB connection string or timed out when attempting to connect")

    db = client[DB_NAME]
    col = db[COLLECTION_NAME]
    col.delete_many({})


if __name__ == "__main__": 
    create()
    #delete()
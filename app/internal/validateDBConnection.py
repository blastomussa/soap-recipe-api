from pymongo.errors import ServerSelectionTimeoutError

def validateMongo(client):
    try:
        client.server_info() # validate connection string
    except ServerSelectionTimeoutError:
        raise TimeoutError("Invalid API for MongoDB connection string or timed out when attempting to connect")
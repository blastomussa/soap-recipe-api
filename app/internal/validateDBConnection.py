from pymongo.errors import ServerSelectionTimeoutError
from fastapi import HTTPException, status

def validateMongo(client):
    try:
        client.server_info() # validate connection string
    except ServerSelectionTimeoutError:
        raise HTTPException(
            status_code=status.HTTP_408_REQUEST_TIMEOUT,
            detail="Invalid API for MongoDB connection string or timed out when attempting to connect"
        )
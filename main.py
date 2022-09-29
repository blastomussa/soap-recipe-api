import random
import pymongo
from fastapi import FastAPI
from pydantic import BaseModel


DB_NAME = "api"
COLLECTION_NAME = "recipies"
CONNECTION_STRING = "mongodb://localhost:27017"


class Recipe(BaseModel):
    _id: int | None = None
    name: str
    description: str | None = None
    oils: list[dict] = None
    liquid: float | None = None
    lye: float | None = None
    weight: float | None = None


app = FastAPI()

@app.get("/recipes")
async def get_items():
    client = pymongo.MongoClient(CONNECTION_STRING)
    try:
        client.server_info() # validate connection string
    except pymongo.errors.ServerSelectionTimeoutError:
        raise TimeoutError("Invalid API for MongoDB connection string or timed out when attempting to connect")

    db = client[DB_NAME]
    col = db[COLLECTION_NAME]
    items = {
        'items': [],
        'count': 0
        }
    cursor = col.find({})
    for document in cursor:
        items['items'].append(document)  
        items['count'] =  int(items['count']) + 1 
    return items



@app.post("/recipes")
async def create_item(recipe: Recipe):
    client = pymongo.MongoClient(CONNECTION_STRING)
    try:
        client.server_info() # validate connection string
    except pymongo.errors.ServerSelectionTimeoutError:
        raise TimeoutError("Invalid API for MongoDB connection string or timed out when attempting to connect")

    db = client[DB_NAME]
    col = db[COLLECTION_NAME]

    id = random.randint(0,1000)
    docs = col.find({'_id': id})
    while len(list(docs)) != 0:
        id = random.randint(0,1000)
        docs = col.find({'_id': id})
        
    result = {**recipe.dict()}
    result['_id'] = id
    col.insert_one(result)
    return result

import random
import pymongo
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

DB_NAME = "api"
CONNECTION_STRING = "mongodb://localhost:27017"

class Recipe(BaseModel):
    _id: int | None = None
    name: str
    description: str | None = None
    oils: list[dict]
    liquid: float | None = None
    lye: float | None = None
    weight: float 
    superfat: float


class Oil(BaseModel):
    _id: int | None = None
    name: str 
    sapratio: float


def validateConnection(client):
    try:
        client.server_info() # validate connection string
    except pymongo.errors.ServerSelectionTimeoutError:
        raise TimeoutError("Invalid API for MongoDB connection string or timed out when attempting to connect")


def calculate_recipe(Recipe):
    weight = Recipe['weight']
    superfat = Recipe['superfat']

    # 1:3 liquid to oil ratio
    liquid = weight * .33
    Recipe['liquid'] = liquid
    client = pymongo.MongoClient(CONNECTION_STRING)
    validateConnection(client)

    db = client['api']
    col = db['oils']

    # calculate individual oil weights and update dictionary
    i = 0
    for r in Recipe['oils']:
        name = r['name']
        w = r['ratio'] * weight #need to validate ratios; must total 1
        Recipe['oils'][i]['weight'] = w
        
        # calculate lye weight
        search = list(col.find({'name': name})) #need to validate if oil is found 
        converted_weight = w - (w * superfat)
        lye = converted_weight * search[0]['sapratio']
        if Recipe['lye']: 
            Recipe['lye'] = Recipe['lye'] + lye
        else:
            Recipe['lye'] = lye
        i = i + 1
 
    return Recipe


@app.get("/recipes")
async def get_recipes():
    client = pymongo.MongoClient(CONNECTION_STRING)
    validateConnection(client)

    db = client[DB_NAME]
    col = db['recipes']
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
async def create_recipe(recipe: Recipe):
    result = {**recipe.dict()}
    recipe = calculate_recipe(result)

    client = pymongo.MongoClient(CONNECTION_STRING)
    validateConnection(client)

    db = client[DB_NAME]
    col = db['recipes']

    id = random.randint(0,1000)
    docs = col.find({'_id': id})
    while len(list(docs)) != 0:
        id = random.randint(0,1000)
        docs = col.find({'_id': id})
        
    
    recipe['_id'] = id
    col.insert_one(recipe)
    return recipe


@app.delete("/recipes/{recipe_id}")
async def delete_recipe(recipe_id: int):
    client = pymongo.MongoClient(CONNECTION_STRING)
    validateConnection(client)

    db = client[DB_NAME]
    col = db['recipes']

    if len(list(col.find({'_id': recipe_id}))) == 0:
        return {'Error': f"A recipe with the _id: {recipe_id} was not found in the database"}
    else:
        col.delete_one({'_id': recipe_id})
        return {'Success': f"recipe _id: {recipe_id} was successfully deleted"}
    


@app.get("/oils")
async def get_oils():
    client = pymongo.MongoClient(CONNECTION_STRING)
    validateConnection(client)

    db = client[DB_NAME]
    col = db['oils']
    items = {
        'items': [],
        'count': 0
        }
    cursor = col.find({})
    for document in cursor:
        items['items'].append(document)  
        items['count'] =  int(items['count']) + 1 
    return items


@app.post("/oils")
async def create_oil(oil: Oil):
    client = pymongo.MongoClient(CONNECTION_STRING)
    validateConnection(client)
    result = {**oil.dict()}

    db = client[DB_NAME]
    col = db['oils']

    if len(list(col.find({'name': result['name']}))) != 0:
        ls = list(col.find({'name': result['name']}))
        schema = ls[0]
        return {'Error': f"{schema['name']} oil already exists in the database"}

    id = random.randint(0,1000)
    docs = col.find({'_id': id})
    while len(list(docs)) != 0:
        id = random.randint(0,1000)
        docs = col.find({'_id': id})
           
    result['_id'] = id
    col.insert_one(result)
    return result


@app.delete("/oils/{oil_id}")
async def delete_oil(oil_id: int):
    client = pymongo.MongoClient(CONNECTION_STRING)
    validateConnection(client)

    db = client[DB_NAME]
    col = db['oils']

    if len(list(col.find({'_id': oil_id}))) == 0:
        return {'Error': f"An oil with the _id: {oil_id} was not found in the database"}
    else:
        col.delete_one({'_id': oil_id})
        return {'Success': f"Oil _id: {oil_id} was successfully deleted"}
    
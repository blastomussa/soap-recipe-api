import random
import pymongo
from datetime import datetime
from fastapi import FastAPI, HTTPException
from models import Items, Version, Oil, Recipe
from calculate import calculate_recipe

app = FastAPI()

# use host.docker.internal for docker to access mongo on local machine
CONNECTION_STRING = "mongodb://host.docker.internal:27017"  # needs to be dynamic; maybe pulled from ENV variable


def validateMongo(client):
    try:
        client.server_info() # validate connection string
    except pymongo.errors.ServerSelectionTimeoutError:
        raise TimeoutError("Invalid API for MongoDB connection string or timed out when attempting to connect")

@app.get("/", response_model=Version)
async def get_version():
    version_info = {
        'version': '0.0.1',
        'author': 'Joe Courtney',
        'repository': 'https://github.com/blastomussa/soap-recipe-api'
    }
    return version_info


@app.get("/recipes", response_model=Items, tags=["Recipes"])
async def get_recipes():
    client = pymongo.MongoClient(CONNECTION_STRING)
    validateMongo(client)
    items = {
        'items': [],
        'count': 0
        }
    cursor = client.api.recipes.find({})
    for document in cursor:
        items['items'].append(document)  
        items['count'] =  int(items['count']) + 1 
    return items


@app.post("/recipes", status_code=201, response_model=Recipe, tags=["Recipes"])
async def create_recipe(recipe: Recipe):
    result = {**recipe.dict()}
    recipe = calculate_recipe(result)

    client = pymongo.MongoClient(CONNECTION_STRING)
    validateMongo(client)

    id = random.randint(0,1000)
    docs = client.api.recipes.find({'_id': id})
    while len(list(docs)) != 0:
        id = random.randint(0,1000)
        docs = client.api.recipes.find({'_id': id})
        
    recipe['_id'] = id
    recipe['date'] = str(datetime.today())
    client.api.recipes.insert_one(recipe)
    return recipe


@app.get("/recipes/{recipe_id}", response_model=Recipe, tags=["Recipes"])
async def get_recipe(recipe_id: int):
    client = pymongo.MongoClient(CONNECTION_STRING)
    validateMongo(client)
    document = client.api.recipes.find_one({'_id': recipe_id})
    if document: 
        return document
    else: 
        raise HTTPException(status_code=404,  detail="Item not found")


@app.delete("/recipes/{recipe_id}", response_model=Recipe, tags=["Recipes"])
async def delete_recipe(recipe_id: int):
    client = pymongo.MongoClient(CONNECTION_STRING)
    validateMongo(client)

    if len(list(client.api.recipes.find({'_id': recipe_id}))) == 0:
        return {'Error': f"A recipe with the _id: {recipe_id} was not found in the database"}
    else:
        client.api.recipes.delete_one({'_id': recipe_id})
        return {'Success': f"recipe _id: {recipe_id} was successfully deleted"}
    


@app.get("/oils", response_model=Items, tags=["Oils"])
async def get_oils():
    client = pymongo.MongoClient(CONNECTION_STRING)
    validateMongo(client)
    items = {
        'items': [],
        'count': 0
        }
    cursor = client.api.oils.find({})
    for document in cursor:
        items['items'].append(document)  
        items['count'] =  int(items['count']) + 1 
    return items


@app.get("/oils/{oil_id}", response_model=Oil, tags=["Oils"])
async def get_oil(oil_id: int):
    client = pymongo.MongoClient(CONNECTION_STRING)
    validateMongo(client)
    document = client.api.oils.find_one({'_id': oil_id})
    if document: 
        return document
    else: 
        raise HTTPException(status_code=404,  detail="Item not found")


@app.post("/oils", status_code=201, response_model=Oil, tags=["Oils"])
async def create_oil(oil: Oil):
    client = pymongo.MongoClient(CONNECTION_STRING)
    validateMongo(client)
    result = {**oil.dict()}

    if len(list(client.api.oils.find({'name': result['name']}))) != 0:
        ls = list(client.api.oils.find({'name': result['name']}))
        schema = ls[0]
        return {'Error': f"{schema['name']} oil already exists in the database"}

    id = random.randint(0,1000)
    docs = client.api.oils.find({'_id': id})
    while len(list(docs)) != 0:
        id = random.randint(0,1000)
        docs = client.api.oils.find({'_id': id})
           
    result['_id'] = id
    client.api.oils.insert_one(result)
    return result


@app.delete("/oils/{oil_id}", tags=["Oils"])
async def delete_oil(oil_id: int):
    client = pymongo.MongoClient(CONNECTION_STRING)
    validateMongo(client)
    if len(list(client.api.oils.find({'_id': oil_id}))) == 0:
        return {'Error': f"An oil with the _id: {oil_id} was not found in the database"}
    else:
        client.api.oils.delete_one({'_id': oil_id})
        return {'Success': f"Oil _id: {oil_id} was successfully deleted"}
    
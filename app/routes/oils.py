import random
from pymongo import MongoClient
from fastapi import APIRouter, Depends, HTTPException

# Internal modules
from models import Oil
from schema import User, Items
from internal.validateDBConnection import validateMongo
from internal.connectionString  import CONNECTION_STRING
from internal.dependencies import get_current_admin_user


router = APIRouter(
    prefix="/oils",
    tags=["Oils"],
    responses={404: {"description": "Not found"}},
)


@router.get("", response_model=Items)
async def get_oils():
    client = MongoClient(CONNECTION_STRING)
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


@router.get("/{oil_id}", response_model=Oil)
async def get_oil(oil_id: int):
    client = MongoClient(CONNECTION_STRING)
    validateMongo(client)
    document = client.api.oils.find_one({'_id': oil_id})
    if document: 
        return document
    else: 
        raise HTTPException(status_code=404,  detail="Item not found")


@router.post("", status_code=201, response_model=Oil, )
async def create_new_oil(oil: Oil, current_user: User = Depends(get_current_admin_user)):
    client = MongoClient(CONNECTION_STRING)
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


@router.delete("/{oil_id}")
async def delete_oil(oil_id: int, current_user: User = Depends(get_current_admin_user)):
    client = MongoClient(CONNECTION_STRING)
    validateMongo(client)
    if len(list(client.api.oils.find({'_id': oil_id}))) == 0:
        return {'Error': f"An oil with the _id: {oil_id} was not found in the database"}
    else:
        client.api.oils.delete_one({'_id': oil_id})
        return {'Success': f"Oil _id: {oil_id} was successfully deleted"}
    
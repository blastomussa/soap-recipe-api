from random import randint
from pymongo import MongoClient
from fastapi import APIRouter, Depends, HTTPException, status

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
    if client.api.oils.find_one({'_id': oil_id}): 
        return client.api.oils.find_one({'_id': oil_id})
    else: 
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"oil id: {oil_id} not found"
        )


@router.post("", status_code=201)
async def create_new_oil(oil: Oil, current_user: User = Depends(get_current_admin_user)):
    client = MongoClient(CONNECTION_STRING)
    validateMongo(client)
    result = {**oil.dict()}
    name = result['name']
    result['name'] = name.lower()
    if client.api.oils.find_one({'name': result['name']}):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"{result['name']} oil already exists in the database"
        )

    id = randint(0,1000)
    while client.api.oils.find_one({'_id': id}):
        id = randint(0,1000)       
    result['_id'] = id

    client.api.oils.insert_one(result)
    return result


@router.delete("/{oil_id}")
async def delete_oil(oil_id: int, current_user: User = Depends(get_current_admin_user)):
    client = MongoClient(CONNECTION_STRING)
    validateMongo(client)
    if not client.api.oils.find_one({'_id': oil_id}):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"An oil with the _id: {oil_id} was not found in the database"
        )
    else:
        client.api.oils.delete_one({'_id': oil_id})
        return {'Success': f"Oil _id: {oil_id} was successfully deleted"}
    
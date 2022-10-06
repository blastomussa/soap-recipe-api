from random import randint
from datetime import datetime
from pymongo import MongoClient
from fastapi import APIRouter, Depends, HTTPException, status

# Internal modules
from models import Recipe
from schema import User, Items
from internal.calculate import calculateRecipe
from internal.validateDBConnection import validateMongo
from internal.connectionString  import CONNECTION_STRING
from internal.dependencies import get_current_active_user


router = APIRouter(
    prefix="/recipes",
    tags=["Recipes"],
    responses={404: {"description": "Not found"}},
)


@router.get("", response_model=Items)
async def get_recipes():
    client = MongoClient(CONNECTION_STRING)
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


@router.post("", status_code=201, response_model=Recipe)
async def create_recipe(recipe: Recipe, current_user: User = Depends(get_current_active_user)):
    result = {**recipe.dict()}
    recipe = calculateRecipe(result)

    client = MongoClient(CONNECTION_STRING)
    validateMongo(client)

    id = randint(0,1000)
    while client.api.recipes.find_one({'_id': id}):
        id = randint(0,1000)
        
    recipe['_id'] = id
    recipe['date'] = str(datetime.today())
    recipe['creator'] = current_user
    client.api.recipes.insert_one(recipe)
    return recipe


@router.get("/{recipe_id}", response_model=Recipe)
async def get_recipe(recipe_id: int):
    client = MongoClient(CONNECTION_STRING)
    validateMongo(client)
    if client.api.recipes.find_one({'_id': recipe_id}): 
        return client.api.recipes.find_one({'_id': recipe_id})
    else: 
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f"A recipe with the id: {recipe_id} was not found in the database"
        )


@router.delete("/{recipe_id}", response_model=Recipe)
async def delete_recipe(recipe_id: int, current_user: User = Depends(get_current_active_user)):
    client = MongoClient(CONNECTION_STRING)
    validateMongo(client)
    if not client.api.recipes.find_one({'_id': recipe_id}):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f"A recipe with the id: {recipe_id} was not found in the database"
        )
    else:
        client.api.recipes.delete_one({'_id': recipe_id})
        return {'Success': f"recipe _id: {recipe_id} was successfully deleted"}
    

from random import randint
from datetime import datetime
from pymongo import MongoClient
from fastapi import APIRouter, Depends, HTTPException, status

from fastapi.encoders import jsonable_encoder

# Internal modules
from models import Recipe, NewRecipe
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
        recipe = Recipe(**document)
        items['items'].append(recipe)  
        items['count'] =  int(items['count']) + 1 
    return items


@router.post("", status_code=201)   # reponse model was giving validation error with oilwieght class, test different options 
async def create_recipe(newrecipe: NewRecipe, current_user: User = Depends(get_current_active_user)):
    result = {**newrecipe.dict()}

    # calculate recipe and validate response
    recipe = calculateRecipe(result)
    if 'oil not found' in recipe:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=recipe
        )

    if 'must equal 1' in recipe:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail=recipe
        )
        
    client = MongoClient(CONNECTION_STRING)
    validateMongo(client)

    # choose id for new recipe
    id = randint(0,10000)
    while client.api.recipes.find_one({'_id': id}):
        id = randint(0,10000)
        
    #construct recipe dictionary for return
    recipe['_id'] = id
    recipe['date'] = str(datetime.today())
    creator = {
        'username': current_user.username,
        'full_name': current_user.full_name
    }
    recipe['creator'] = creator 

    # insert recipe ID into User document
    query = {'username': current_user.username}
    user = client.api.Users.find_one(query)
    try:
        if not user['recipes']:
            user['recipes'] = []
        user['recipes'].append(id)
        insert = user['recipes']
    except KeyError:
        user['recipes'] = [id]
        insert = user['recipes']
    update = {'$set':{'recipes': insert}}
    client.api.Users.update_one(query,update)

    client.api.recipes.insert_one(jsonable_encoder(recipe)) #encode data because it includes a pydantic model 
    return recipe


@router.get("/{recipe_id}", response_model=Recipe)
async def get_recipe(recipe_id: int):
    client = MongoClient(CONNECTION_STRING)
    validateMongo(client)
    if client.api.recipes.find_one({'_id': recipe_id}): 
        return Recipe(**client.api.recipes.find_one({'_id': recipe_id}))
    else: 
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f"A recipe with the id: {recipe_id} was not found in the database"
        )


# delete recipe; only allowed if admin or recipe is associated with user
@router.delete("/{recipe_id}", status_code=204)
async def delete_recipe(recipe_id: int, current_user: User = Depends(get_current_active_user)):
    client = MongoClient(CONNECTION_STRING)
    validateMongo(client)
    if not client.api.recipes.find_one({'_id': recipe_id}):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f"A recipe with the id: {recipe_id} was not found in the database"
        )
    elif not current_user.admin:
        if current_user.recipes:
            found = False
            for r in current_user.recipes:
                if r == recipe_id:
                    found = True
                    deleted_recipe = client.api.recipes.find_one_and_delete({'_id': recipe_id})
                    
                    #search for creator to remove entry from their associated recipies list
                    username = deleted_recipe['creator']['username']
                    creator = client.api.Users.find_one({'username': username})

                    recipes_list = creator['recipes']
                    try:
                        for i in recipes_list:
                            if i == recipe_id:
                                recipes_list.remove[i]
                        client.api.Users.update_one({'username': username},{'recipes':recipes_list})
                    except TypeError:
                        pass
                    
                    return {'Success': f"recipe _id: {recipe_id} was successfully deleted"}
            if not found:
                raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, 
                detail=f"A recipe with the id: {recipe_id} is not associated with non-admin user"
                ) 
        else:
           raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f"A recipe with the id: {recipe_id} is not associated with non-admin user"
            ) 

    else:
        client.api.recipes.delete_one({'_id': recipe_id})
        return {'Success': f"recipe _id: {recipe_id} was successfully deleted"}
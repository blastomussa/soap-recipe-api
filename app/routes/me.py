from fastapi import APIRouter, Depends
from schema import User, Items
from internal.dependencies import get_current_active_user

from pymongo import MongoClient
from internal.validateDBConnection import validateMongo
from internal.connectionString  import CONNECTION_STRING

router = APIRouter(
    prefix="/users/me",
    tags=["Me"],
    responses={404: {"description": "Not found"}},
)


@router.get("", response_model=User)
async def read_users_me(current_user: User = Depends(get_current_active_user)):
    return current_user


# get recipes associated with user
@router.get("/recipes", response_model=Items)
async def read_own_items(current_user: User = Depends(get_current_active_user)):
    client = MongoClient(CONNECTION_STRING)
    validateMongo(client)
    user = client.api.Users.find_one({'username': current_user.username})
    items = {
        'items': [],
        'count': 0
    }
    # might not need the try-except becuase of pydantic model validation
    try:
        for id in user['recipes']:
            recipe = client.api.recipes.find_one({'_id': id})
            items['items'].append(recipe)
            items['count'] =  int(items['count']) + 1 
    except KeyError:
        pass

    return items
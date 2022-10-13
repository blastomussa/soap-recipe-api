from fastapi import APIRouter, Depends, HTTPException, status
from models import NewPassword, User, Items, UserInDB
from internal.dependencies import get_current_active_user
from internal.dependencies import get_password_hash, verify_password

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


@router.patch("/password", status_code=201)
async def change_password(password: NewPassword, current_user: User = Depends(get_current_active_user)):
    client = MongoClient(CONNECTION_STRING)
    validateMongo(client)

    db_user = UserInDB(**client.api.Users.find_one({'_id': current_user.id}))

    if not verify_password(password.password1,db_user.hashed_password):
        update = {'$set': {'hashed_password': get_password_hash(password.password1)}}
        result = client.api.Users.update_one({'_id': current_user.id}, update)
        if result.modified_count != 1:
            raise HTTPException(
                status_code=status.HTTP_417_EXPECTATION_FAILED,
                detail="Password change failed for unknown reason"
            )
    else:
        raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="New password cannot be the same as old password"
        )
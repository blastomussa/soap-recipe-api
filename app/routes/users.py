from random import randint
from schema import User, Items, Admin, UserInDB, Disabled
from models import NewUser
from fastapi import APIRouter, Depends, HTTPException, status

from internal.dependencies import get_current_admin_user
from internal.dependencies import get_password_hash

from pymongo import MongoClient
from internal.validateDBConnection import validateMongo
from internal.connectionString  import CONNECTION_STRING


router = APIRouter (
    prefix="/users",
    tags=["Users"],
    responses={404: {"description": "Not found"}},
)


@router.get("", response_model=Items)
async def read_users(current_user: User = Depends(get_current_admin_user)):
    client = MongoClient(CONNECTION_STRING)
    validateMongo(client)
    
    items = {
        'items': [],
        'count': 0
    }
  
    cursor = client.api.Users.find({})
    for document in cursor:
        items['items'].append(document)  
        items['count'] =  int(items['count']) + 1 
    return items    


@router.post("",status_code=201, response_model=UserInDB)
async def register_user(user: NewUser):
    client = MongoClient(CONNECTION_STRING)
    validateMongo(client)

    if client.api.Users.find_one({'username': user.username.lower()}):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Username already in use"
        )
    elif client.api.Users.find_one({'email': user.email.lower()}):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Email already in use"
        )

    id = randint(0,1000)
    while client.api.User.find_one({'_id': id}):
        id = randint(0,1000)

    new_db_user = {
        'username': user.username.lower(),
        'email': user.email.lower(),
        'full_name': user.full_name,
        'disabled': False,
        'admin': False,
        'hashed_password': get_password_hash(user.password1),
        'recipes': [],
        '_id': id,
    }
    
    client.api.Users.insert_one(new_db_user)
    return new_db_user


@router.patch("/{user_id}", status_code=201, response_model=User)
async def toggle_user_admin(user_id: int, admin: Admin, current_user: User = Depends(get_current_admin_user)):
    client = MongoClient(CONNECTION_STRING)
    validateMongo(client)
    query = {'_id': user_id}
    if not client.api.Users.find_one(query):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with id: {user_id} not found"
        )
    update = {'$set':{'admin': True}} if admin.admin else {'$set':{'admin': False}} #ternary operator
    client.api.Users.update_one(query,update)
    return client.api.Users.find_one(query)


@router.patch("/{user_id}/disabled", status_code=201, response_model=User)
async def toggle_user_disabled(user_id: int, disabled: Disabled, current_user: User = Depends(get_current_admin_user)):
    client = MongoClient(CONNECTION_STRING)
    validateMongo(client)
    query = {'_id': user_id}
    if not client.api.Users.find_one(query):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with id: {user_id} not found"
        )
    update = {'$set':{'disabled': True}} if disabled.disabled else {'$set':{'admin': False}} #ternary operator
    client.api.Users.update_one(query,update)
    return client.api.Users.find_one(query)
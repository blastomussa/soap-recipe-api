from random import randint

from models import NewUser, User, Items, Admin, Disabled
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.encoders import jsonable_encoder


from internal.dependencies import get_current_admin_user, get_current_active_user
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
        user = User(**document)
        items['items'].append(user)  
        items['count'] =  int(items['count']) + 1 
    return items  


@router.get("/{user_id}", status_code=200 , response_model=User)
async def get_user(user_id: int,current_user: User = Depends(get_current_active_user)):
    client = MongoClient(CONNECTION_STRING)
    validateMongo(client)
    if client.api.Users.find_one({'_id': user_id}):
        return User(**client.api.Users.find_one({'_id': user_id}))
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with id: {user_id} not found"
        )  


@router.post("",status_code=201, response_model=User)
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
    return User(**new_db_user)


@router.patch("/{user_id}", status_code=200, response_model=User)
async def update_user(user_id: int, data: User, current_user: User = Depends(get_current_active_user)):
    client = MongoClient(CONNECTION_STRING)
    validateMongo(client)
    stored_user_model = client.api.Users.find_one({'_id': user_id})
    user_data = User(**stored_user_model)
    update_data = data.dict(exclude_unset=True)
    patched = False


    if current_user.admin or current_user.id == user_id:
        try:
            if update_data['username']:
                if not client.api.Users.find_one({'username': update_data['username']}) :
                    updated_user = user_data.copy(update={'username': update_data['username']})
                    user_data = updated_user
                    patched = True
        except KeyError:
            pass
        try:
            if update_data['email']:
                if not client.api.Users.find_one({'email': update_data['email']}) :
                    updated_user = user_data.copy(update={'email': update_data['email']})
                    user_data = updated_user
                    patched = True
        except KeyError:
            pass
        try:
            if update_data['full_name']:
                updated_user = user_data.copy(update={'full_name': update_data['full_name']})
                user_data = updated_user
                patched = True
        except KeyError:
            pass
    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Only admins can update users unless updating your own user"
        )

    if patched:
        update = {'$set': jsonable_encoder(user_data)}
        client.api.Users.find_one_and_update({'_id': user_id}, update)
        return user_data
    else:
        raise HTTPException(
            status_code=status.HTTP_304_NOT_MODIFIED,
            detail="No user data was modified."
        )
    

@router.delete("/{user_id}",status_code=204)
async def delete_user(user_id: int, current_user: User = Depends(get_current_active_user)):
    client = MongoClient(CONNECTION_STRING)
    validateMongo(client)
    if current_user.admin:
        client.api.Users.delete_one({'_id': user_id})
    elif user_id == current_user.id:
        client.api.Users.delete_one({'_id': user_id})
    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Only admins can delete users unless deleting your own user"
        )


@router.patch("/{user_id}/admin", status_code=201, response_model=User)
async def toggle_user_admin(user_id: int, admin: Admin, current_user: User = Depends(get_current_admin_user)):
    client = MongoClient(CONNECTION_STRING)
    validateMongo(client)
    query = {'_id': user_id}
    if client.api.Users.find_one(query):  
        update = {'$set':{'admin': True}} if admin.admin else {'$set':{'admin': False}} #ternary operator
        client.api.Users.update_one(query,update)
        return User(**client.api.Users.find_one(query))
    else:
        raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"User with id: {user_id} not found"
        )


@router.patch("/{user_id}/disabled", status_code=201, response_model=User)
async def toggle_user_disabled(user_id: int, disabled: Disabled, current_user: User = Depends(get_current_admin_user)):
    client = MongoClient(CONNECTION_STRING)
    validateMongo(client)
    query = {'_id': user_id}
    if client.api.Users.find_one(query):   
        update = {'$set':{'disabled': True}} if disabled.disabled else {'$set':{'admin': False}} #ternary operator
        client.api.Users.update_one(query,update)
        return User(**client.api.Users.find_one(query))
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with id: {user_id} not found"
        )
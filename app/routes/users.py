from pydantic import ValidationError
from models import User, Items, Admin, NewUser
from fastapi import APIRouter, Depends, HTTPException, status, Form

from internal.dependencies import get_current_admin_user

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

    


# WORK ON THIS
@router.post("",status_code=201)
async def create_user(user: NewUser):
    try:
        return {user.username: user.password1}
    except ValidationError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Unable to validate new user fields.",
            headers={"WWW-Authenticate": "Bearer"},
        )



@router.patch("/{user_id}", status_code=201, response_model=User)
async def toggle_user_admin(user_id: int, admin: Admin, current_user: User = Depends(get_current_admin_user)):
    client = MongoClient(CONNECTION_STRING)
    validateMongo(client)
    query = {'_id': user_id}
    update = {'$set':{'admin': True}} if admin.admin else {'$set':{'admin': False}} #ternary operator
    client.api.Users.update_one(query,update)
    return client.api.Users.find_one(query)
   
    

    








from models import User, Items
from fastapi import APIRouter, Depends, HTTPException, status

from internal.dependencies import get_current_active_user, get_current_admin_user, get_password_hash

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

    


# NOT DONE
@router.post("",status_code=201, response_model=User)
async def create_user():
    pass


@router.patch("/{user_id}", status_code=201, response_model=User)
async def toggle_user_admin(user_id: int, admin: dict[str,bool], current_user: User = Depends(get_current_admin_user)):
    client = MongoClient(CONNECTION_STRING)
    validateMongo(client)

    query = {'_id': user_id}
    try:
        if admin['admin'] == True:
            update = {'$set':{'admin': True}}
        elif admin['admin'] == False:
            update = {'$set':{'admin': False}}

        client.api.Users.update_one(query,update)
        return client.api.Users.find_one(query)
    except KeyError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Bad request",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    

    








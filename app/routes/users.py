from models import User, Items
from fastapi import APIRouter, Depends

from internal.dependencies import get_current_active_user, get_current_admin_user, get_password_hash

from pymongo import MongoClient
from internal.validateDBConnection import validateMongo
from internal.connectionString  import CONNECTION_STRING


router = APIRouter (
    prefix="/users",
    tags=["users"],
    responses={404: {"description": "Not found"}},
    dependencies=[Depends(get_current_admin_user)]  # all endpoints require admin: True
)


@router.get("", response_model=Items)
async def read_users():
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
@router.post("", response_model=User)
async def create_user(current_user: User = Depends(get_current_active_user)):
    return current_user



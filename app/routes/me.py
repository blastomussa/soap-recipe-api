from fastapi import APIRouter, Depends
from models import User
from routes.token import get_current_active_user

router = APIRouter(
    prefix="/users/me",
    tags=["me"],
    responses={404: {"description": "Not found"}},
)


@router.get("", response_model=User)
async def read_users_me(current_user: User = Depends(get_current_active_user)):
    return current_user


@router.get("/items")
async def read_own_items(current_user: User = Depends(get_current_active_user)):
    return [{"item_id": "Foo", "owner": current_user.username}]
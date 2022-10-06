from datetime import timedelta
from fastapi.security import OAuth2PasswordRequestForm
from fastapi import Depends, HTTPException, status, APIRouter

# internal modules
from internal.dependencies import authenticate_user, create_access_token

# models
from schema import Token

# environment variable
from config import settings


router = APIRouter(
    prefix="/token",
    tags=["Token"],
    responses={404: {"description": "Not found"}},
)


@router.post("", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=settings.access_token_expire_minutes)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}
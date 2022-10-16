from datetime import timedelta
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordRequestForm
from fastapi import Depends, HTTPException, status, APIRouter

# internal modules
from internal.dependencies import authenticate_user, create_access_token, create_refresh_token

# models
from models import Token

# environment variable
from config import settings


router = APIRouter(
    prefix="/token",
    tags=["Token"],
    responses={404: {"description": "Not found"}},
)


@router.post("", response_model=Token, status_code=200)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    # Create access token
    access_token_expires = timedelta(minutes=settings.access_token_expire_minutes)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    refresh_token_expires = timedelta(minutes=settings.refresh_token_expire_minutes)
    refresh_token = create_refresh_token(
        data={"sub": user.username}, expires_delta=refresh_token_expires
    )
    content = {"message": "Success"}
    response = JSONResponse(content=content)
    response.set_cookie(key="access_token", value=f"Bearer {access_token}")
    response.set_cookie(key="refresh_token", value=refresh_token)
    return response


@router.get("/refresh")
def refresh_token():
    pass


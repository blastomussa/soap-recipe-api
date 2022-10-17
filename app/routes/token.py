from datetime import timedelta
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordRequestForm
from fastapi import Depends, HTTPException, status, APIRouter
from jose import JWTError, jwt


# internal modules
from internal.dependencies import authenticate_user, create_access_token, create_refresh_token

# models
from models import Token, RefreshToken

# environment variable
from config import settings


router = APIRouter(
    prefix="/token",
    tags=["Token"],
    responses={404: {"description": "Not found"}},
)

required_cookie_args = {
        'name':'SOAP_API_COOKIE',
        'value':'the cookie works'
    }
optional_cookie_args = {
    'version':0,
    'port':None,
    'domain':'127.0.0.1', #NOTE: If domain is a blank string or not supplied this creates a "super cookie" that is supplied to all domains.
    'path':'/',
    'secure':False,
    'expires':None,
    'discard':True,
    'comment':None,
    'comment_url':None,
    'rest':{'HttpOnly': None},
    'rfc2109':False
}


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
    content = {"access_token": access_token, "token_type":"Bearer"}
    response = JSONResponse(content=content)
    response.set_cookie(key="access_token", value=f"Bearer {access_token}")
    response.set_cookie(key="refresh_token", value=refresh_token)
    response.set_cookie(key="logged_in", value=1)
    response.set_cookie(key="username", value=user.username)
    return response


@router.get("/refresh")
def refresh_token(refresh_token: RefreshToken):
    refresh = refresh_token.dict()
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not refresh token",
        headers={"WWW-Authenticate": "Bearer"},
    )
    if refresh_token:
        try: 
            payload = jwt.decode(refresh['refresh_token'], settings.secret_key, algorithms=[settings.algorithm])
            username: str = payload.get("sub")
            if username: # can i test to see if this matches current user somehow(without needing to auth)
                # Create access token
                access_token_expires = timedelta(minutes=settings.access_token_expire_minutes)
                access_token = create_access_token(
                    data={"sub": username}, expires_delta=access_token_expires
                )
                refresh_token_expires = timedelta(minutes=settings.refresh_token_expire_minutes)
                refresh = create_refresh_token(
                    data={"sub": username}, expires_delta=refresh_token_expires
                )
                content = {"access_token": access_token}
                response = JSONResponse(content=content)
                response.set_cookie(key="access_token", value=f"Bearer {access_token}")
                response.set_cookie(key="refresh_token", value=refresh)
                return response
            else:
                raise credentials_exception
        except JWTError:
                raise credentials_exception


from fastapi import FastAPI
from fastapi.security import OAuth2PasswordBearer # not implemented yet; for Oauth2

#internal modules
from models import Version

# routes
from routes import oils, recipes

app = FastAPI()


app.include_router(oils.router)
app.include_router(recipes.router)


@app.get("/", response_model=Version)
async def get_version():
    version_info = {
        'version': '0.0.1',
        'author': 'Joe Courtney',
        'repository': 'https://github.com/blastomussa/soap-recipe-api'
    }
    return version_info
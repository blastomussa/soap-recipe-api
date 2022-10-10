from fastapi import FastAPI

#internal modules
from schema import Version
from routes import oils, recipes, token, me, users

description = """
Calculates and stores soap recipes
"""

app = FastAPI(
    title="Soap Recipe Calculator API",
    description=description,
    version="0.0.2",
    contact={
        "name": "Joe Courtney",
    },
    license_info={
        "name": "MIT",
        "url": "https://mit-license.org",
    },
)


app.include_router(oils.router)
app.include_router(recipes.router)
app.include_router(token.router)
app.include_router(me.router)
app.include_router(users.router)


@app.get("/", response_model=Version, tags=["Version"])
async def get_version():
    version_info = {
        'version': '0.0.2',
        'author': 'Joe Courtney',
        'description': 'REST API to calculate soap recipes.',
        'language': 'Python 3.10.7',
        'framework': 'FastAPI',
        'repository': 'https://github.com/blastomussa/soap-recipe-api'
    }
    return version_info
from pydantic import BaseModel

# token models
class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str | None = None


# user models
class User(BaseModel):
    _id: int | None = None
    username: str
    email: str | None = None
    full_name: str | None = None
    disabled: bool | None = None
    admin: bool | None = None 


class UserInDB(User):
    hashed_password: str # additional pw fields for database user model
    

# items model
class Items(BaseModel):
    items: list[dict]
    count: int


# version information model
class Version(BaseModel):
    version: str
    author: str
    description: str
    language: str
    framework: str
    repository: str


# oil model
class Oil(BaseModel):
    _id: int | None = None
    name: str 
    sapratio: float


# Recipes model
class Recipe(BaseModel):
    _id: int | None = None
    name: str
    description: str | None = None
    date: str | None = None
    oils: list[dict]
    liquid: float | None = None
    lye: float | None = None
    weight: float 
    superfat: float

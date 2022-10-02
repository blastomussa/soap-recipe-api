from pydantic import BaseModel

class User(BaseModel):
    _id: int | None = None
    username: str
    email: str | None = None
    full_name: str | None = None
    disabled: bool | None = None


# additional pw fields for database user model
class UserInDB(User):
    hashed_password: str
    

class Items(BaseModel):
    items: list[dict]
    count: int


class Version(BaseModel):
    version: str
    author: str
    repository: str


class Oil(BaseModel):
    _id: int | None = None
    name: str 
    sapratio: float


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

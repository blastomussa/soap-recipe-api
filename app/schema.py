from pydantic import BaseModel

# token schema
class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str | None = None


# user schema
class User(BaseModel):
    _id: int | None = None
    username: str
    email: str | None = None
    full_name: str | None = None
    disabled: bool | None = None
    admin: bool | None = None 


class UserInDB(User):
    hashed_password: str # additional pw hash field for database user model


class Admin(BaseModel):
    admin: bool 


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
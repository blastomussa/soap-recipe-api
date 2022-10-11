from pydantic import BaseModel, Field

# token schema
class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str | None = None


# user schema
class User(BaseModel):
    id: int | None = Field(..., alias='_id')
    username: str
    email: str | None = None
    full_name: str | None = None
    disabled: bool | None = None
    admin: bool | None = None
    recipes: list[int] | None = None


class UserInDB(User):
    hashed_password: str # additional pw hash field for database user model


class Admin(BaseModel):
    admin: bool

class Disabled(BaseModel):
    disabled: bool


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
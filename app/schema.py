from pydantic import BaseModel, EmailStr, Field, validator
from re import compile, fullmatch

# token schema
class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str | None = None


# user schema
class User(BaseModel):
    id: int = Field(default=None, alias='_id')   # use this line to update other schema to fix 422 errors 
    username: str | None = None
    email: EmailStr | None = None
    full_name: str | None = None
    disabled: bool | None = None
    admin: bool | None = None
    recipes: list[int] | None = None

    @validator('username')
    def check_username(cls, v):
        regex = compile(r"^[a-zA-Z]{5,20}$")
        if not fullmatch(regex,v):
            raise ValueError('username must be must only use letters and be 5-20 characters in length')
        return v

    @validator('full_name')
    def name_must_contain_space(cls, v):
        if ' ' not in v:
            raise ValueError('full name must contain a space')
        elif len(v) > 30 or len(v) < 5:
            raise ValueError('full name must be between 5 and 30 characters long')
        return v.title()


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
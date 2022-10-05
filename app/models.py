from re import compile, fullmatch, search
from pydantic import BaseModel, validator, root_validator


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
    hashed_password: str # additional pw hash field for database user model


class NewUser(BaseModel):
    username: str
    full_name: str
    email: str | None = None
    password1: str
    password2: str
    
    @root_validator
    def check_passwords(cls, values):
        pw1, pw2 = values.get('password1'), values.get('password2')
        # upercase, lowercase, number, special character, between 6-20 chars long
        regex = compile(r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!#%*?&]{6,20}$")
        if not search(regex,pw1):
            raise ValueError('password complexit not met')
        elif pw1 is not None and pw2 is not None and pw1 != pw2: #ensure password are the same
            raise ValueError('passwords do not match')
        return values

    @validator('username')
    def check_username(cls, v):
        regex = compile(r"^[a-zA-Z]{5,20}$")
        if not fullmatch(regex,v):
            raise ValueError('username must be must only use letters and be 5-20 characters in length')
        return v.title()
    
    @validator('full_name')
    def name_must_contain_space(cls, v):
        if ' ' not in v:
            raise ValueError('full name must contain a space')
        elif len(v) > 30 or len(v) < 5:
            raise ValueError('full name must be between 5 and 30 characters long')
        return v.title()

    @validator('email')
    def check_email(cls, v):
        # validated based on RFC5322 specification
        regex = compile(r"([-!#-'*+/-9=?A-Z^-~]+(\.[-!#-'*+/-9=?A-Z^-~]+)*|\"([]!#-[^-~ \t]|(\\[\t -~]))+\")@([-!#-'*+/-9=?A-Z^-~]+(\.[-!#-'*+/-9=?A-Z^-~]+)*|\[[\t -Z^-~]*])")
        if not fullmatch(regex, v):
            raise ValueError('Email must be valid')
        return v.title()   


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


# oil model
class Oil(BaseModel):
    _id: int | None = None
    name: str 
    sapratio: float

    @validator('name')
    def check_oilname(cls, v):
        regex = compile(r"^[a-zA-Z]{3,20}$")
        if not fullmatch(regex,v):
            raise ValueError('oil name must be must only use letters and be 3-20 characters in length')
        return v.title()

    @validator('sapratio')
    def check_sapratio(cls, v):
        if v > 1:  #test to make sure v is a being passed as a float for comparison
            raise ValueError('SAP ratio must be less than 1')
        return v.title()


# ADD VALIDATORS
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

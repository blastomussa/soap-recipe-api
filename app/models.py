from re import compile, fullmatch, search
from pydantic import BaseModel, EmailStr, validator, root_validator

from schema import User

from pymongo import MongoClient
from internal.validateDBConnection import validateMongo
from internal.connectionString import CONNECTION_STRING


class NewUser(BaseModel):
    username: str
    full_name: str
    email: EmailStr | None = None
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
        return v
    
    @validator('full_name')
    def name_must_contain_space(cls, v):
        if ' ' not in v:
            raise ValueError('full name must contain a space')
        elif len(v) > 30 or len(v) < 5:
            raise ValueError('full name must be between 5 and 30 characters long')
        return v.title()


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
        return v

    @validator('sapratio')
    def check_sapratio(cls, v):
        if v > 1: 
            raise ValueError('SAP ratio must be less than 1')
        return v


# ADD VALIDATORS
# Recipes models
class OilRatio(BaseModel):
    name: str
    ratio: float

    @validator('name')
    def check_name(cls, v):
        client = MongoClient(CONNECTION_STRING)
        validateMongo(client)
        if not client.api.oils.find_one({'name': v}):
            raise ValueError('Oil not found')
        return v

    @validator('ratio')
    def check_ratio(cls, v):
        if v > 1:  
            raise ValueError('ratio must be 1 or less')
        return v


class OilWeight(BaseModel):
    name: str
    weight: float


class NewRecipe(BaseModel):
    name: str
    description: str | None = None
    oils: list[OilRatio]           # HOW DO I VALIDATE DATA IN THE DICTS; for each validator?
    weight: float 
    superfat: float

    @validator('superfat')
    def check_superfat(cls, v):
        if v >= .2:  #test to make sure v is a being passed as a float for comparison
            raise ValueError('superfat ratio must be less than .2 (20%)')
        return v

    @validator('weight')
    def check_weight(cls, v):
        if v <= 0:
            raise ValueError('weight must be greater than 0')
        return v


class Recipe(BaseModel):
    _id: int | None = None
    name: str
    description: str | None = None
    date: str | None = None
    oils: list[OilWeight]           # HOW DO I VALIDATE DATA IN THE DICTS; for each validator? or elsewhere in app
    liquid: float | None = None
    lye: float | None = None
    weight: float 
    superfat: float
    creator: User
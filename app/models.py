from pydantic import BaseModel

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

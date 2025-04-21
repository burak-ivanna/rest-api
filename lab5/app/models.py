from pydantic_mongo import ObjectIdField
from pydantic import BaseModel, Field


class Book(BaseModel):
    id: ObjectIdField = Field(alias="_id")
    title: str
    author: str
    year: int

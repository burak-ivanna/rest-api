from pydantic import BaseModel, Field
from typing import Optional


class BookSchema(BaseModel):
    id: int
    title: str
    author: str
    year: int

    class Config:
        from_attributes = True


class BookCreateSchema(BaseModel):
    title: str = Field(..., min_length=1, max_length=100)
    author: str = Field(..., min_length=1, max_length=100)
    year: int = Field(..., gt=0, lt=2100)

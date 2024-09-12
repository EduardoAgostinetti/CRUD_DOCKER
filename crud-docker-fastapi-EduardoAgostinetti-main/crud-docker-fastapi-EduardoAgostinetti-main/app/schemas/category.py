from pydantic import BaseModel

from ..schemas.item import Item

class CategoryBase(BaseModel):
    name: str
    description: str

class CategoryCreate(CategoryBase):
    pass

class Category(CategoryBase):
    id: int
    # items: list[Item] = []

    class Config:
        orm_mode = True

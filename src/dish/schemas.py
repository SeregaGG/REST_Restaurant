from pydantic import BaseModel, UUID4, condecimal
from typing import Optional


class DishBase(BaseModel):
    title: str
    description: str
    price: condecimal(decimal_places=2)


class DishResponse(DishBase):
    id: UUID4


class DishDelete(BaseModel):
    status: bool
    message: str


class DishPatch(DishBase):
    title: Optional[str] = None
    description: Optional[str] = None

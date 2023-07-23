from pydantic import BaseModel, UUID4
from typing import Optional


class MenuBase(BaseModel):
    title: str
    description: str


class MenuResponse(MenuBase):
    id: UUID4
    submenus_count: int
    dishes_count: int


class MenuDelete(BaseModel):
    status: bool
    message: str


class MenuPatch(MenuBase):
    title: Optional[str] = None
    description: Optional[str] = None

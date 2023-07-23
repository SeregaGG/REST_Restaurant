from pydantic import BaseModel, UUID4
from typing import Optional


class SubmenuBase(BaseModel):
    title: str
    description: str


class SubmenuResponse(SubmenuBase):
    id: UUID4
    dishes_count: int


class SubmenuDelete(BaseModel):
    status: bool
    message: str


class SubmenuPatch(SubmenuBase):
    title: Optional[str] = None
    description: Optional[str] = None

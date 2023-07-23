from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import UUID4
from .crud import create_submenu, get_all_submenus, get_submenu, update_submenu, delete_submenu
from .schemas import SubmenuResponse, SubmenuBase, SubmenuDelete, SubmenuPatch
from src.database import get_db

submenu = APIRouter()


@submenu.get("/", response_model=list[SubmenuResponse])
async def get_submenus(
        menu_id: UUID4,
        db: AsyncSession = Depends(get_db)
):
    return await get_all_submenus(menu_id, db)


@submenu.get("/{submenu_id}", response_model=SubmenuResponse)
async def get_submenu_by_id(
        submenu_id: UUID4,
        db: AsyncSession = Depends(get_db)
):
    result = await get_submenu(submenu_id, db)
    if result is None:
        raise HTTPException(status_code=404, detail="submenu not found")

    return result


@submenu.post("/", response_model=SubmenuResponse, status_code=201)
async def create_submenu_with_body(
        menu_id: UUID4,
        data: SubmenuBase,
        db: AsyncSession = Depends(get_db)
):
    return await create_submenu(menu_id, data, db)


@submenu.delete("/{submenu_id}", response_model=SubmenuDelete)
async def delete_submenu_by_id(
        submenu_id: UUID4,
        db: AsyncSession = Depends(get_db)
):
    result = await delete_submenu(submenu_id, db)

    if result is None:
        raise HTTPException(status_code=404, detail="submenu not found")

    return result


@submenu.patch("/{submenu_id}", response_model=SubmenuResponse)
async def update_menu_by_id(
        submenu_id: UUID4,
        data: SubmenuPatch,
        db: AsyncSession = Depends(get_db)
):
    result = await update_submenu(submenu_id, data, db)
    if result is None:
        raise HTTPException(status_code=404, detail="submenu not found")

    return result

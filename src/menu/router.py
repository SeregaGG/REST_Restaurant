from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import UUID4
from .schemas import MenuResponse, MenuBase, MenuDelete, MenuPatch
from .crud import create_menu, get_all_menus, get_menu, update_menu, delete_menu
from src.database import get_db

menu = APIRouter()


@menu.get("/", response_model=list[MenuResponse], status_code=200)
async def get_menus(
        db: AsyncSession = Depends(get_db)
):
    return await get_all_menus(db)


@menu.get("/{menu_id}", response_model=MenuResponse, status_code=200)
async def get_menu_by_id(
        menu_id: UUID4,
        db: AsyncSession = Depends(get_db)
):
    result = await get_menu(menu_id, db)
    if result is None:
        raise HTTPException(status_code=404, detail="menu not found")

    return result


@menu.post("/", response_model=MenuResponse, status_code=201)
async def create_menu_with_body(
        data: MenuBase,
        db: AsyncSession = Depends(get_db)
):
    return await create_menu(data, db)


@menu.delete("/{menu_id}", response_model=MenuDelete)
async def delete_menu_by_id(
        menu_id: UUID4,
        db: AsyncSession = Depends(get_db)
):
    result = await delete_menu(menu_id, db)

    if result is None:
        raise HTTPException(status_code=404, detail="menu not found")

    return result


@menu.patch("/{menu_id}", response_model=MenuResponse)
async def update_menu_by_id(
        menu_id: UUID4,
        data: MenuPatch,
        db: AsyncSession = Depends(get_db)
):
    result = await update_menu(menu_id, data, db)
    if result is None:
        raise HTTPException(status_code=404, detail="menu not found")

    return result

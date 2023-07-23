from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import UUID4
from .schemas import DishResponse, DishBase, DishDelete, DishPatch
from src.database import get_db
from .crud import create_dish, get_all_dishes, get_dish, update_dish, delete_dish

dish = APIRouter()


@dish.get("/", response_model=list[DishResponse])
async def get_dishes(
        submenu_id: UUID4,
        db: AsyncSession = Depends(get_db)
):
    return await get_all_dishes(submenu_id, db)


@dish.get("/{dish_id}", response_model=DishResponse)
async def get_dish_by_id(
        dish_id: UUID4,
        db: AsyncSession = Depends(get_db)
):
    result = await get_dish(dish_id, db)
    if result is None:
        raise HTTPException(status_code=404, detail="dish not found")

    return result


@dish.post("/", response_model=DishResponse, status_code=201)
async def create_dish_with_body(
        submenu_id: UUID4,
        data: DishBase,
        db: AsyncSession = Depends(get_db)
):
    return await create_dish(submenu_id, data, db)


@dish.delete("/{dish_id}", response_model=DishDelete)
async def delete_dish_by_id(
        dish_id: UUID4,
        db: AsyncSession = Depends(get_db)
):
    result = await delete_dish(dish_id, db)

    if result is None:
        raise HTTPException(status_code=404, detail="dish not found")

    return result


@dish.patch("/{dish_id}", response_model=DishResponse)
async def update_menu_by_id(
        dish_id: UUID4,
        data: DishPatch,
        db: AsyncSession = Depends(get_db)
):
    result = await update_dish(dish_id, data, db)
    if result is None:
        raise HTTPException(status_code=404, detail="dish not found")

    return result

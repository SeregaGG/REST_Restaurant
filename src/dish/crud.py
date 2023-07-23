from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from pydantic import UUID4
from src.dish.models import Dish
from .schemas import DishBase, DishResponse, DishDelete


async def get_dish(dish_id: UUID4, db: AsyncSession) -> DishResponse | None:
    query = select(Dish).where(Dish.id == dish_id)
    dish = await db.execute(query)
    dish = dish.scalar_one_or_none()
    if dish is None:
        return None
    return DishResponse(**dish.__dict__)


async def get_all_dishes(submenu_id: UUID4, db: AsyncSession) -> list[DishResponse] | None:
    query = select(Dish).where(Dish.submenu_id == submenu_id)
    dishes = await db.execute(query)
    dishes = dishes.scalars()
    result = [
        DishResponse(
            **dish.__dict__
        ) for dish in dishes
    ]
    return result


async def create_dish(submenu_id: UUID4, data: DishBase, db: AsyncSession) -> DishResponse:
    dish = Dish(**data.model_dump(), submenu_id=submenu_id)
    try:
        db.add(dish)
        await db.commit()
        await db.refresh(dish)
    except Exception as e:
        print(e)

    return DishResponse(**dish.__dict__)


async def update_dish(dish_id: UUID4, data: DishBase, db: AsyncSession) -> DishResponse | None:
    query = select(Dish).where(Dish.id == dish_id)
    dish = await db.execute(query)
    dish = dish.scalar_one_or_none()
    if dish is None:
        return None

    for key in data.model_dump():
        new_value = getattr(data, key)
        if new_value:
            setattr(dish, key, new_value)

    await db.commit()
    await db.refresh(dish)

    return DishResponse(**dish.__dict__)


async def delete_dish(dish_id: UUID4, db: AsyncSession) -> DishDelete | None:
    query = select(Dish).where(Dish.id == dish_id)
    dish = await db.execute(query)
    dish = dish.scalar_one_or_none()
    if dish is None:
        return None

    await db.delete(dish)
    await db.commit()

    return DishDelete(status=True, message="The dish has been deleted")

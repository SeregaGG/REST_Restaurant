from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from pydantic import UUID4
from src.menu.models import Menu
from .schemas import MenuBase, MenuResponse, MenuDelete


async def get_menu(menu_id: UUID4, db: AsyncSession) -> MenuResponse | None:
    query = select(Menu).where(Menu.id == menu_id)
    menu = await db.execute(query)
    menu = menu.scalar_one_or_none()
    if menu is None:
        return None
    return MenuResponse(**menu.__dict__, submenus_count=await menu.submenus_count, dishes_count=await menu.dishes_count)


async def get_all_menus(db: AsyncSession) -> list[MenuResponse] | None:
    query = select(Menu)
    menus = await db.execute(query)
    menus = menus.scalars()
    result = [
        MenuResponse(
            **menu.__dict__,
            submenus_count=await menu.submenus_count,
            dishes_count=await menu.dishes_count
        ) for menu in menus
    ]
    return result


async def create_menu(data: MenuBase, db: AsyncSession) -> MenuResponse:
    menu = Menu(**data.model_dump())
    try:
        db.add(menu)
        await db.commit()
        await db.refresh(menu)
    except Exception as e:
        print(e)

    return MenuResponse(**menu.__dict__, submenus_count=0, dishes_count=0)


async def update_menu(menu_id: UUID4, data: MenuBase, db: AsyncSession) -> MenuResponse | None:
    query = select(Menu).where(Menu.id == menu_id)
    menu = await db.execute(query)
    menu = menu.scalar_one_or_none()
    if menu is None:
        return None

    for key in data.model_dump():
        new_value = getattr(data, key)
        if new_value:
            setattr(menu, key, new_value)

    await db.commit()
    await db.refresh(menu)

    return MenuResponse(**menu.__dict__, submenus_count=await menu.submenus_count, dishes_count=await menu.dishes_count)


async def delete_menu(menu_id: UUID4, db: AsyncSession) -> MenuDelete | None:
    query = select(Menu).where(Menu.id == menu_id)
    menu = await db.execute(query)
    menu = menu.scalar_one_or_none()
    if menu is None:
        return None

    await db.delete(menu)
    await db.commit()

    return MenuDelete(status=True, message="The menu has been deleted")

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from pydantic import UUID4
from src.submenu.models import Submenu
from .schemas import SubmenuBase, SubmenuResponse, SubmenuDelete


async def get_submenu(submenu_id: UUID4, db: AsyncSession) -> SubmenuResponse | None:
    query = select(Submenu).where(Submenu.id == submenu_id)
    submenu = await db.execute(query)
    submenu = submenu.scalar_one_or_none()
    if submenu is None:
        return None
    return SubmenuResponse(**submenu.__dict__, dishes_count=await submenu.dishes_count)


async def get_all_submenus(menu_id: UUID4, db: AsyncSession) -> list[SubmenuResponse] | None:
    query = select(Submenu).where(Submenu.menu_id == menu_id)
    submenu = await db.execute(query)
    submenu = submenu.scalars()
    result = [
        SubmenuResponse(
            **submenu.__dict__,
            dishes_count=await submenu.dishes_count
        ) for submenu in submenu
    ]
    return result


async def create_submenu(menu_id: UUID4, data: SubmenuBase, db: AsyncSession) -> SubmenuResponse:
    submenu = Submenu(**data.model_dump(), menu_id=menu_id)
    try:
        db.add(submenu)
        await db.commit()
        await db.refresh(submenu)
    except Exception as e:
        print(e)

    return SubmenuResponse(**submenu.__dict__, dishes_count=0)


async def update_submenu(submenu_id: UUID4, data: SubmenuBase, db: AsyncSession) -> SubmenuResponse | None:
    query = select(Submenu).where(Submenu.id == submenu_id)
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

    return SubmenuResponse(**menu.__dict__, dishes_count=await menu.dishes_count)


async def delete_submenu(submenu_id: UUID4, db: AsyncSession) -> SubmenuDelete | None:
    query = select(Submenu).where(Submenu.id == submenu_id)
    menu = await db.execute(query)
    menu = menu.scalar_one_or_none()
    if menu is None:
        return None

    await db.delete(menu)
    await db.commit()

    return SubmenuDelete(status=True, message="The menu has been deleted")

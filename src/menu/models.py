from sqlalchemy import Column, String, UUID
from sqlalchemy.ext.hybrid import hybrid_property
from src.database import Base, DBContextManager
import uuid
from sqlalchemy import select, func
from src.dish.models import Dish
from src.submenu.models import Submenu


class Menu(Base):
    __tablename__ = "menu"

    id = Column(UUID, primary_key=True, default=uuid.uuid4)

    description = Column(String, nullable=False)
    title = Column(String, nullable=False)

    @hybrid_property
    async def submenus_count(self):
        query = select(func.count(Submenu.id)).where(Submenu.menu_id == self.id)
        async with DBContextManager() as db:
            count = await db.execute(query)
            count = count.scalar_one_or_none()
        return count

    @hybrid_property
    async def dishes_count(self):
        submenu_query = select(Submenu).where(Submenu.menu_id == self.id)
        async with DBContextManager() as db:
            submenus = await db.execute(submenu_query)
            submenus = submenus.scalars()
            count = 0

            for submenu in submenus:
                query_count = select(func.count(Dish.id)).where(Dish.submenu_id == submenu.id)
                current_count = await db.execute(query_count)
                count += current_count.scalar_one_or_none()

        return count

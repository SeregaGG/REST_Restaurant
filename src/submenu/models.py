import uuid
from sqlalchemy import Column, String, UUID, ForeignKey
from sqlalchemy.ext.hybrid import hybrid_property
from src.database import Base, DBContextManager
from sqlalchemy import select, func
from src.dish.models import Dish


class Submenu(Base):
    __tablename__ = "submenu"

    id = Column(UUID, primary_key=True, default=uuid.uuid4)

    menu_id = Column(UUID, ForeignKey("menu.id", ondelete="CASCADE"), nullable=False)

    description = Column(String, nullable=False)
    title = Column(String, nullable=False, unique=True)

    @hybrid_property
    async def dishes_count(self):
        query = select(func.count(Dish.id)).where(Dish.submenu_id == self.id)
        async with DBContextManager() as db:
            count = await db.execute(query)
            count = count.scalar_one_or_none()
        return count

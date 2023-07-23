import uuid

from sqlalchemy import Column, String, UUID, ForeignKey, Numeric
from src.database import Base


class Dish(Base):
    __tablename__ = "dish"

    id = Column(UUID, primary_key=True, default=uuid.uuid4)

    submenu_id = Column(UUID, ForeignKey("submenu.id", ondelete="CASCADE"), nullable=False)

    description = Column(String, nullable=False)
    title = Column(String, nullable=False, unique=True)
    price = Column(Numeric(10, 2), nullable=False)

    # __table_args__ = (UniqueConstraint("title", "menu_id", name="menu_id_submenu_title"),)

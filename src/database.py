from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from src.settings import DBSettings

db_settings = DBSettings()

DATABASE_URL = f"postgresql+asyncpg://" \
               f"{db_settings.POSTGRES_USER}:" \
               f"{db_settings.POSTGRES_PASSWORD}@" \
               f"{db_settings.POSTGRES_HOST}:" \
               f"{db_settings.POSTGRES_PORT}/" \
               f"{db_settings.POSTGRES_DB}"

engine = create_async_engine(DATABASE_URL, echo=True)
Base = declarative_base()
async_session = async_sessionmaker(
    engine, class_=AsyncSession, expire_on_commit=False
)


async def get_db():
    db: AsyncSession = async_session()
    try:
        yield db
    finally:
        await db.close()


async def init_db() -> None:
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


class DBContextManager:
    async def __aenter__(self):
        self.db: AsyncSession = async_session()
        return self.db

    async def __aexit__(self, exc_type, exc, tb):
        await self.db.close()

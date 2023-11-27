from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from bot.config_reader import config  # Импорт конфигурации


def get_async_sessionmaker():
    engine = create_async_engine(str(config.db_url), echo=False)
    return sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


# Initialize the session factory once and use it throughout the application
async_sessionmaker = get_async_sessionmaker()

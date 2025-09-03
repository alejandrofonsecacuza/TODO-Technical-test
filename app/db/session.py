# app/db/database.py

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker,declarative_base
from app.core.config import settings

#Models

# Crea el motor de base de datos asíncrono
engine = create_async_engine(settings.GET_URL_DB(), echo=True, future=True)

# Crea una fábrica de sesiones asíncronas
AsyncSessionLocal = sessionmaker(
    autocommit=False, autoflush=False, bind=engine, class_=AsyncSession
)

# Base declarativa para los modelos de SQLAlchemy

Base = declarative_base()


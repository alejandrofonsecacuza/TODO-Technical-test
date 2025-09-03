#Imports
import pytest
from fastapi.testclient import TestClient
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
import os
#Main
from app.main import app

#Database
from app.db.base import Base
#Dependens
from app.dependens.db import get_db


os.environ["APP_ENV"] = "testing"
# ---------------------------
# Configuración de base de datos de test
# ---------------------------

TEST_DATABASE_URL = "sqlite+aiosqlite:///:memory:"

# Usamos StaticPool para que la misma conexión persista en toda la sesión
engine_test = create_async_engine(
    TEST_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
    future=True,
    echo=False
)

async_session_maker_test = sessionmaker(
    engine_test, class_=AsyncSession, expire_on_commit=False
)

# ---------------------------
# Fixture para preparar la DB
# ---------------------------

@pytest.fixture(scope="session", autouse=True)
def prepare_database():
    """
    Crea todas las tablas antes de los tests y las elimina después.
    """
    import asyncio
    async def create_tables():
        async with engine_test.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)

    asyncio.run(create_tables())
    yield
    async def drop_tables():
        async with engine_test.begin() as conn:
            await conn.run_sync(Base.metadata.drop_all)
    asyncio.run(drop_tables())

# ---------------------------
# Sobrescribir la dependencia get_db
# ---------------------------

def override_get_db():
    """
    Yield de sesión async para la app
    """
    async def _get_db():
        async with async_session_maker_test() as session:
            yield session
    return _get_db

app.dependency_overrides[get_db] = override_get_db()

# ---------------------------
# Fixture del cliente de test
# ---------------------------

@pytest.fixture
def client():
    """
    Cliente síncrono de FastAPI para tests
    """
    return TestClient(app)

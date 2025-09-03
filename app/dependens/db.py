
#Session
from app.db.session import AsyncSessionLocal
# app/db/session_gen.py

async def get_db():
    """
    Dependencia de FastAPI para obtener una sesión de base de datos.
    """
    async with AsyncSessionLocal() as session:
        yield session

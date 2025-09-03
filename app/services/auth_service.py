# Imports
from fastapi import HTTPException, status
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import SQLAlchemyError


#Models
from app.db.models.user import User

#Schemas
from app.schemas.user import UserCreate

#Core
from app.core.log import logger
from app.core.security import verify_password, hash_password, create_access_token


class AuthService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def register(self, user_data: UserCreate):
        """Registra un nuevo usuario."""
        try:
            # Revisar si ya existe el usuario
            result = await self.db.execute(
                select(User).filter(User.email == user_data.email)
            )
            existing_user = result.scalars().first()
            if existing_user:
                logger.warning(f"Attempted registration with existing email: {user_data.email}")
                raise HTTPException(status_code=409, detail="Email already registered")

            # Crear nuevo usuario
            new_user = User(
                email=user_data.email,
                hashed_password=hash_password(user_data.password)
            )
            self.db.add(new_user)
            await self.db.commit()
            await self.db.refresh(new_user)
            logger.info(f"New user registered: {new_user.email}")
            return new_user
        except SQLAlchemyError as e:
            await self.db.rollback()
            logger.error(f"Error registering user {user_data.email}: {e}")
            raise HTTPException(status_code=500, detail="Database error")

    async def _authenticate_user(self, email: str, password: str):
        """Autentica un usuario internamente, retorna None si falla."""
        try:
            result = await self.db.execute(
                select(User).filter(User.email == email)
            )
            user = result.scalars().first()
            if not user or not verify_password(password, user.hashed_password):
                logger.warning(f"Failed login attempt for email: {email}")
                return None
            return user
        except SQLAlchemyError as e:
            logger.error(f"Error authenticating user {email}: {e}")
            return None

    async def login(self, email: str, password: str):
        """Login de usuario y generación de token JWT."""
        user = await self._authenticate_user(email, password)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid credentials"
            )
        token = create_access_token({"sub": user.email})
        logger.info(f"User logged in: {email}")
        return {"access_token": token, "token_type": "bearer"}

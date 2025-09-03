from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession


from app.dependens.security import get_current_user
from app.dependens.db import get_db
from app.schemas.user import UserOut,UserCreate
from app.schemas.token import Token


from app.services.auth_service import AuthService

router = APIRouter()

@router.post("/register", response_model=UserOut)
async def register(user_data: UserCreate, db: AsyncSession = Depends(get_db)):
    return await AuthService(db).register(user_data)
    

@router.post("/login", response_model=Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends(), db: AsyncSession = Depends(get_db)):
    return await AuthService(db).login(form_data.username, form_data.password)

@router.get("/me", response_model=UserOut)
def get_profile(current_user: UserOut = Depends(get_current_user)):
    return current_user
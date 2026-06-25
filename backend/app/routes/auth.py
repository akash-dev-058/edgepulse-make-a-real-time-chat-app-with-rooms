import logging
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from ..schemas.user import UserCreate, UserRead, Token
from ..services.auth import AuthService
from ..dependencies import get_db

router = APIRouter(prefix="/auth", tags=["auth"])
logger = logging.getLogger("app.routes.auth")

@router.post("/register", response_model=UserRead, status_code=status.HTTP_201_CREATED)
async def register(user_in: UserCreate, db: AsyncSession = Depends(get_db)):
    try:
        user = await AuthService.register_user(db, user_in)
        return user
    except ValueError as ve:
        logger.warning("Registration error: %s", ve)
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(ve))
    except Exception as exc:
        logger.exception("Unexpected error during registration")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error")

@router.post("/login", response_model=Token)
async def login(form: UserCreate, db: AsyncSession = Depends(get_db)):
    try:
        token = await AuthService.authenticate_user(db, form.email, form.password)
        return token
    except ValueError as ve:
        logger.warning("Login failed: %s", ve)
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(ve))
    except Exception as exc:
        logger.exception("Unexpected error during login")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error")

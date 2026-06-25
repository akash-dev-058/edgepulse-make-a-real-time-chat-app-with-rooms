import logging
from datetime import timedelta
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from ..models.user import User
from ..core.security import get_password_hash, verify_password, create_access_token
from ..schemas.user import UserCreate, Token

logger = logging.getLogger("app.services.auth")

class AuthService:
    @staticmethod
    async def register_user(db: AsyncSession, user_in: UserCreate) -> User:
        stmt = select(User).where(User.email == user_in.email)
        result = await db.execute(stmt)
        existing = result.scalar_one_or_none()
        if existing:
            raise ValueError("Email already registered")
        hashed = get_password_hash(user_in.password)
        user = User(email=user_in.email, hashed_password=hashed)
        db.add(user)
        await db.commit()
        await db.refresh(user)
        logger.info("Registered new user %s", user.email)
        return user

    @staticmethod
    async def authenticate_user(db: AsyncSession, email: str, password: str) -> Token:
        stmt = select(User).where(User.email == email)
        result = await db.execute(stmt)
        user = result.scalar_one_or_none()
        if not user:
            raise ValueError("Incorrect email or password")
        if not verify_password(password, user.hashed_password):
            raise ValueError("Incorrect email or password")
        access_token = create_access_token({"sub": str(user.id)})
        logger.info("User %s authenticated", email)
        return Token(access_token=access_token)

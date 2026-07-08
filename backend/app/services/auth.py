from datetime import timedelta
from typing import Optional

from fastapi import HTTPException, status
from jose import JWTError

from app.models.user import User
from app.schemas.auth import UserCreate, UserLogin, UserOut
from app.db.repository import UserRepository
from app.core.security import (
    create_access_token,
    create_refresh_token,
    verify_password,
    get_password_hash,
)
from app.core.logger import get_logger

logger = get_logger(__name__)


class AuthService:
    def __init__(self, user_repo: UserRepository):
        self.user_repo = user_repo

    async def register_user(self, payload: UserCreate) -> UserOut:
        # Check if user exists
        if await self.user_repo.get_by_email(payload.email):
            logger.warning("Registration attempt with existing email", email=payload.email)
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail={"error": "Email already registered"}
            )
        if await self.user_repo.get_by_username(payload.username):
            logger.warning("Registration attempt with existing username", username=payload.username)
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail={"error": "Username already taken"}
            )

        # Create user
        hashed_password = get_password_hash(payload.password)
        user = await self.user_repo.create(
            User,
            email=payload.email,
            username=payload.username,
            hashed_password=hashed_password,
        )
        logger.info("User registered", user_id=user.id, email=user.email)
        return UserOut.from_orm(user)

    async def authenticate_user(self, payload: UserLogin) -> Optional[User]:
        user = await self.user_repo.get_by_email(payload.email)
        if not user or not verify_password(payload.password, user.hashed_password):
            logger.warning("Failed login attempt", email=payload.email)
            return None
        return user

    async def create_tokens(self, user: User) -> dict:
        access_token = create_access_token(user.id)
        refresh_token = create_refresh_token(user.id)
        logger.info("Tokens issued", user_id=user.id)
        return {
            "access_token": access_token,
            "refresh_token": refresh_token,
        }

    async def refresh_tokens(self, refresh_token: str) -> dict:
        payload = verify_token(refresh_token, token_type="refresh")
        if not payload:
            logger.warning("Invalid refresh token used")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail={"error": "Invalid refresh token"}
            )
        user_id = payload.get("sub")
        user = await self.user_repo.get_by_id(User, user_id)
        if not user:
            logger.warning("User not found for refresh token", user_id=user_id)
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail={"error": "User not found"}
            )
        return await self.create_tokens(user)


def get_auth_service(user_repo: UserRepository) -> AuthService:
    return AuthService(user_repo)

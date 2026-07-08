import pytest
from fastapi import status

from app.models.user import User
from app.schemas.auth import UserCreate, UserLogin
from app.core.security import verify_password


@pytest.mark.asyncio
async def test_register_user(auth_service, user_repo):
    payload = UserCreate(email="new@example.com", username="newuser", password="password123")
    user = await auth_service.register_user(payload)
    assert user.email == "new@example.com"
    assert user.username == "newuser"
    assert user.id is not None


@pytest.mark.asyncio
async def test_register_duplicate_email(auth_service, user_repo):
    payload = UserCreate(email="user1@example.com", username="newuser2", password="password123")
    with pytest.raises(Exception) as exc_info:
        await auth_service.register_user(payload)
    assert exc_info.value.status_code == status.HTTP_409_CONFLICT


@pytest.mark.asyncio
async def test_register_duplicate_username(auth_service, user_repo):
    payload = UserCreate(email="new2@example.com", username="user1", password="password123")
    with pytest.raises(Exception) as exc_info:
        await auth_service.register_user(payload)
    assert exc_info.value.status_code == status.HTTP_409_CONFLICT


@pytest.mark.asyncio
async def test_authenticate_user(auth_service, user_repo):
    payload = UserLogin(email="user1@example.com", password="password1")
    user = await auth_service.authenticate_user(payload)
    assert user is not None
    assert user.email == "user1@example.com"
    assert verify_password("password1", user.hashed_password)


@pytest.mark.asyncio
async def test_authenticate_invalid_password(auth_service, user_repo):
    payload = UserLogin(email="user1@example.com", password="wrongpassword")
    user = await auth_service.authenticate_user(payload)
    assert user is None


@pytest.mark.asyncio
async def test_create_tokens(auth_service, user_repo):
    user = await user_repo.get_by_email("user1@example.com")
    tokens = await auth_service.create_tokens(user)
    assert "access_token" in tokens
    assert "refresh_token" in tokens


@pytest.mark.asyncio
async def test_refresh_tokens(auth_service, user_repo):
    user = await user_repo.get_by_email("user1@example.com")
    refresh_token = auth_service.create_refresh_token(user.id)
    new_tokens = await auth_service.refresh_tokens(refresh_token)
    assert "access_token" in new_tokens
    assert "refresh_token" in new_tokens

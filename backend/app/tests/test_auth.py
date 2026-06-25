import pytest
from httpx import AsyncClient
from app.schemas.user import UserCreate

@pytest.mark.asyncio
async def test_register_and_login(client: AsyncClient):
    # Register
    register_payload = {"email": "test@example.com", "password": "StrongPass123"}
    resp = await client.post("/auth/register", json=register_payload)
    assert resp.status_code == 201
    data = resp.json()
    assert data["email"] == register_payload["email"]
    # Login
    resp = await client.post("/auth/login", json=register_payload)
    assert resp.status_code == 200
    token_data = resp.json()
    assert "access_token" in token_data
    # Access protected route
    headers = {"Authorization": f"Bearer {token_data['access_token']}"}
    resp = await client.get("/rooms/me", headers=headers)
    assert resp.status_code == 200

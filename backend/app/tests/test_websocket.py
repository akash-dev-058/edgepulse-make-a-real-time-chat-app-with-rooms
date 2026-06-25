import json
import pytest
from fastapi import WebSocket
from starlette.testclient import TestClient
from app.main import app
from app.core.security import create_access_token

@pytest.fixture
def token():
    return create_access_token({"sub": "00000000-0000-0000-0000-000000000001"})

def test_websocket_connection(token):
    client = TestClient(app)
    with client.websocket_connect(f"/ws?token={token}") as websocket:
        # Send init payload
        init = {"room_id": "test-room"}
        websocket.send_text(json.dumps(init))
        # Send a chat message
        msg = {"content": "Hello world"}
        websocket.send_text(json.dumps(msg))
        # Receive broadcast (may be typing or message)
        data = websocket.receive_text()
        payload = json.loads(data)
        assert payload["type"] in ["message", "typing"]

import pytest
from client import MCPClient
import os


@pytest.mark.asyncio
async def test_client_init():
    server_url = os.getenv("SERVER_URL", "http://localhost:8000")
    client = MCPClient(server_url)
    assert client.server_url == server_url
    assert client.timeout == 30

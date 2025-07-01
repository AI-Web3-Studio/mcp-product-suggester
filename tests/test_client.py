import pytest
from client import MCPClient


@pytest.mark.asyncio
async def test_client_init():
    client = MCPClient("http://localhost:8000")
    assert client.server_url == "http://localhost:8000"
    assert client.timeout == 30

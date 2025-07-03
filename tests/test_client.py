# This test uses pytest-asyncio for async test support
import os
import pytest
import asyncio
from fastmcp import Client

@pytest.mark.asyncio
async def test_fastmcp_client_health():
    server_url = os.getenv("SERVER_URL", "http://localhost:8000")
    async with Client(f"{server_url}/mcp-server/mcp") as client:
        # 调用 health 工具，检查服务端健康
        result = await client.call_tool("health")
        # 适配新版 fastmcp，CallToolResult.content 是 list
        assert result.content[0].text == "ok"

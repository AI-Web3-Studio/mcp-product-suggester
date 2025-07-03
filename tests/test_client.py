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
        # 断言第一个返回内容的 text 字段为 "ok"
        assert result[0].text == "ok"

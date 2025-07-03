"""
MCP 客户端模块
MCP client module

提供与 MCP 服务器通信的客户端功能
Provides client functions for communicating with the MCP server
支持通过 HTTP URL 连接
Supports connection via HTTP URL
"""

import asyncio
import aiohttp
from typing import Dict, Any, Optional
from common.log import logger
from fastmcp import Client
import os


class MCPClient:
    """
    MCP 客户端类
    MCP client class
    提供与 MCP 服务器通信的异步客户端接口
    Provides an async client interface for communicating with the MCP server
    """

    def __init__(self, server_url: str, timeout: int = 30) -> None:
        """
        初始化客户端
        Initialize the client
        Args:
            server_url: MCP 服务器 URL / MCP server URL
            timeout: 请求超时时间（秒）/ Request timeout (seconds)
        """
        self.server_url: str = server_url.rstrip('/')
        self.timeout: int = timeout
        self.session: Optional[aiohttp.ClientSession] = None

    async def __aenter__(self) -> 'MCPClient':
        """
        异步上下文管理器入口
        Async context manager entry
        """
        self.session = aiohttp.ClientSession(
            timeout=aiohttp.ClientTimeout(total=self.timeout))
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb) -> None:
        """
        异步上下文管理器出口
        Async context manager exit
        """
        if self.session:
            await self.session.close()

    async def call_tool(self, tool_name: str, **kwargs) -> Optional[str]:
        """
        调用 MCP 工具
        Call MCP tool
        Args:
            tool_name: 工具名称 / Tool name
            **kwargs: 工具参数 / Tool parameters
        Returns:
            工具执行结果 / Tool execution result
        """
        if not self.session:
            raise RuntimeError(
                "Client session not initialized. Use async context manager.")
        try:
            request_data = {
                "jsonrpc": "2.0",
                "id": 1,
                "method": "tools/call",
                "params": {
                    "name": tool_name,
                    "arguments": kwargs
                }
            }
            async with self.session.post(
                f"{self.server_url}/mcp",
                json=request_data,
                headers={"Content-Type": "application/json"}
            ) as response:
                if response.status == 200:
                    result = await response.json()
                    if "result" in result:
                        return result["result"]["content"][0]["text"]
                    elif "error" in result:
                        logger.error(f"MCP tool error: {result['error']}")
                        return None
                else:
                    logger.error(f"HTTP error {response.status}: {await response.text()}")
                    return None
        except asyncio.TimeoutError:
            logger.error(f"Request timeout for tool {tool_name}")
            return None
        except Exception as e:
            logger.error(f"Error calling tool {tool_name}: {e}")
            return None

    async def gpt_recommend(self, query: str, limit: int = 3) -> Optional[str]:
        """
        基于GPT的语义推荐
        Semantic recommendation based on GPT
        Args:
            query: 用户查询 / User query
            limit: 返回结果数量限制 / Limit of returned results
        Returns:
            推荐商品结果 / Recommended product result
        """
        return await self.call_tool("gpt_recommend", query=query, limit=limit)

    async def test_connection(self) -> bool:
        """
        测试服务器连接
        Test server connection
        Returns:
            连接是否成功 / Whether the connection is successful
        """
        try:
            if not self.session:
                raise RuntimeError("Client session not initialized")
            async with self.session.get(f"{self.server_url}/health") as response:
                return response.status == 200
        except Exception as e:
            logger.error(f"Connection test failed: {e}")
            return False


async def create_client(server_url: str, timeout: int = 30) -> MCPClient:
    """
    创建 MCP 客户端
    Create MCP client
    Args:
        server_url: 服务器 URL / Server URL
        timeout: 超时时间 / Timeout
    Returns:
        MCP 客户端实例 / MCP client instance
    """
    return MCPClient(server_url, timeout)


async def test_mcp_server(server_url: str) -> bool:
    """
    测试 MCP 服务器连接
    Test MCP server connection
    Args:
        server_url: 服务器 URL / Server URL
    Returns:
        连接是否成功 / Whether the connection is successful
    """
    async with MCPClient(server_url) as client:
        return await client.test_connection()


async def main():
    server_url = os.getenv("SERVER_URL", "http://localhost:8000")
    try:
        async with Client(f"{server_url}/mcp-server/mcp") as client:
            # 英文自然语言描述用户需求 / English natural language product query
            query = "I want a discreet, travel-friendly vibrator suitable for beginners, preferably waterproof and USB rechargeable."
            result = await client.call_tool("gpt_recommend", {"query": query, "limit": 1})
            print(result)
    except Exception as e:
        logger.error(f"Client main exception: {e}")


if __name__ == "__main__":
    asyncio.run(main())

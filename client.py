"""
MCP 客户端模块
MCP client module

提供与 MCP 服务器通信的客户端功能
Provides client functions for communicating with the MCP server
支持通过 HTTP URL 连接
Supports connection via HTTP URL
"""

import asyncio
from common.log import logger
from fastmcp import Client
import os
from dotenv import load_dotenv

load_dotenv()

async def main():
    try:
        server_url = os.getenv("SERVER_URL", "http://localhost:8000")
        async with Client(f"{server_url}/mcp-server/mcp") as client:
            # 英文自然语言描述用户需求 / English natural language product query
            query = "I want a discreet, travel-friendly vibrator suitable for beginners, preferably waterproof and USB rechargeable."
            result = await client.call_tool("gpt_recommend", {"query": query, "limit": 1})
            print(result)
    except Exception as e:
        logger.error(f"Client main exception: {e}")


if __name__ == "__main__":
    asyncio.run(main())

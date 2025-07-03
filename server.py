"""
FastMCP 服务器模块
FastMCP server module

极简化，适配 fastmcp/uv 生态，直接暴露 app = FastMCP(...)，注册工具。
Minimalist, adapted to fastmcp/uv ecosystem, directly exposes app = FastMCP(...), registers tools.
"""

from fastmcp import FastMCP
from fastapi import FastAPI
from starlette.routing import Mount
import os
import json
from database import ProductDatabase
from gpt_service import GPTRecommendationService
from common.log import logger

# 创建 FastMCP 服务器
mcp = FastMCP("product-recommendation-server")

# 健康检查工具 / Health check tool
@mcp.tool()
def health() -> str:
    """
    健康检查接口
    Health check endpoint
    Returns:
        str: "ok" 字符串 / "ok" string
    """
    return "ok"

# 纯GPT推荐工具 / Pure GPT recommendation tool
@mcp.tool()
async def gpt_recommend(query: str, limit: int = 3) -> str:
    """
    基于GPT的商品推荐工具
    Product recommendation tool based on GPT
    Args:
        query: 用户查询 / User query
        limit: 推荐数量 / Number of recommendations
    Returns:
        格式化推荐结果 / Formatted recommendation result
    """
    logger.info(f"gpt_recommend request params: query={query}, limit={limit}")
    try:
        db = ProductDatabase()
        products = await db.load_products(limit=1000)
        gpt_service = GPTRecommendationService()
        recommended = await gpt_service.get_recommendations(query, products, limit)
        return json.dumps(recommended)
    except Exception as e:
        logger.error(f"gpt_recommend exception: {e}")
        return str([])

# 创建 ASGI app
mcp_app = mcp.http_app(path='/mcp')

# 创建 FastAPI app 并挂载 MCP 服务
app = FastAPI(lifespan=mcp_app.lifespan)
app.mount("/mcp-server", mcp_app)

# 可选：FastAPI 根路由健康检查
@app.get("/")
def root():
    return {"status": "ok", "msg": "MCP FastAPI server is running."}

if __name__ == "__main__":
    # 启动并运行服务 / Initialize and run the server
    port = int(os.getenv("SERVER_PORT", 8000))
    app.run(transport="http", host="127.0.0.1", port=port, path="/mcp")

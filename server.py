"""
FastMCP 服务器模块
FastMCP server module

极简化，适配 fastmcp/uv 生态，直接暴露 app = FastMCP(...)，注册工具。
Minimalist, adapted to fastmcp/uv ecosystem, directly exposes app = FastMCP(...), registers tools.
"""

from fastmcp import FastMCP
from database import ProductDatabase
from gpt_service import GPTRecommendationService

app = FastMCP("product-recommendation-server")

# 健康检查工具 / Health check tool


def health() -> str:
    """
    健康检查接口
    Health check endpoint
    Returns:
        str: "ok" 字符串 / "ok" string
    """
    return "ok"


app.tool()(health)

# 纯GPT推荐工具 / Pure GPT recommendation tool


@app.tool()
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
    db = ProductDatabase()
    products = await db.load_products(limit=1000)
    gpt_service = GPTRecommendationService()
    recommended = await gpt_service.get_recommendations(query, products, limit)
    return str(recommended)

if __name__ == "__main__":
    # 启动并运行服务 / Initialize and run the server
    app.run(transport="http", host="127.0.0.1", port=8000, path="/mcp")

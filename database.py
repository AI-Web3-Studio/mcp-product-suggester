"""
数据库操作模块
Database operation module

负责从数据库加载商品数据，处理分类编号转换等
Responsible for loading product data from the database and handling category code conversion, etc.
"""

import json
from typing import List, Dict, Any, Optional
import aiomysql
from common.log import logger
from common.config import DB_ADMIN, PRODUCT_TABLE, PRODUCT_SQL_TEMPLATE
from common.database import BaseDatabase


class ProductDatabase(BaseDatabase):
    """
    商品数据库操作类，极简通用模式
    Product database operation class, minimal universal mode
    """

    def __init__(self):
        self.pool: Optional[aiomysql.Pool] = None

    async def connect(self):
        """
        初始化异步数据库连接池
        Initialize async database connection pool
        """
        try:
            self.pool = await aiomysql.create_pool(
                host=DB_ADMIN['HOST'],
                port=DB_ADMIN['PORT'],
                user=DB_ADMIN['USER'],
                password=DB_ADMIN['PASS'],
                db=DB_ADMIN['BASE'],
                charset='utf8mb4',
                autocommit=True,
                minsize=1,
                maxsize=10
            )
            logger.info("Async DB pool created successfully")
        except Exception as e:
            logger.error(f"Failed to create async DB pool: {e}")
            raise

    async def query(self, sql: str, params: Any = None) -> List[Dict]:
        """
        异步执行SQL查询，返回结果列表
        Execute SQL query asynchronously, return result list
        """
        if not self.pool:
            await self.connect()
        async with self.pool.acquire() as conn:
            async with conn.cursor(aiomysql.DictCursor) as cursor:
                await cursor.execute(sql, params) if params else await cursor.execute(sql)
                return await cursor.fetchall()

    async def close(self):
        """
        关闭数据库连接池
        Close the database connection pool
        """
        if self.pool:
            self.pool.close()
            await self.pool.wait_closed()

    async def load_products(self, limit: int = 1000) -> List[Dict[str, Any]]:
        """
        从数据库加载商品数据（原始字段，不做适配）
        Load product data from the database (raw fields, no adaptation)
        Args:
            limit: 加载商品数量限制 / Limit of products to load
        Returns:
            商品数据列表（原始字段）/ List of product data (raw fields)
        """
        try:
            sql = PRODUCT_SQL_TEMPLATE.format(table=PRODUCT_TABLE, limit=limit)
            results = await self.query(sql)
            logger.info(
                f"Loaded {len(results)} products from database (raw mode)")
            return results
        except Exception as e:
            logger.error(f"Error loading products from database: {e}")
            return []

"""
GPT 智能推荐服务模块
GPT intelligent recommendation service module

负责调用 GPT API 进行智能商品推荐
Responsible for calling GPT API for intelligent product recommendation
"""

import re
import os
import aiohttp
import asyncio
import json
from typing import List, Dict, Any, Optional
from common.log import logger
from tenacity import AsyncRetrying, stop_after_attempt, wait_fixed
from common.config import LLM_PROVIDER, OPENAI_API_KEY, PROXY_URL

# 全局信号量，限制GPT API最大并发
# Global semaphore to limit max concurrency of GPT API
GPT_API_SEMAPHORE = asyncio.Semaphore(10)


class GPTRecommendationService:
    """
    GPT 智能推荐服务类（极简通用模式）
    GPT intelligent recommendation service class (minimal universal mode)
    负责调用 GPT API 进行智能商品推荐
    Responsible for calling GPT API for intelligent product recommendation
    """

    def __init__(self) -> None:
        self.llm_provider = os.getenv("LLM_PROVIDER", "monica").lower()
        if self.llm_provider == "openai":
            self.api_key: Optional[str] = os.getenv("OPENAI_API_KEY")
            self.api_url: str = "https://api.openai.com/v1/chat/completions"
        else:
            self.api_key: Optional[str] = os.getenv("MONICA_API_KEY")
            self.api_url: str = "https://openapi.monica.im/v1/chat/completions"
        if not self.api_key:
            logger.warning(
                f"{self.llm_provider.upper()} API KEY not set, GPT recommendations will be disabled")

    def _build_products_text(self, products: List[Dict[str, Any]]) -> str:
        """
        构建商品信息文本（直接序列化为 JSON 字符串）
        Build product info text (serialize as JSON string)
        Args:
            products: 商品列表 / List of products
        Returns:
            JSON 字符串 / JSON string
        """
        return json.dumps(products, ensure_ascii=False)

    def _build_system_prompt(self) -> str:
        """
        构建系统提示词（通用化，无行业限定）
        Build system prompt (universal, not industry-specific)
        Returns:
            系统提示词 / System prompt
        """
        return ("""You are a product recommendation expert for an e-commerce platform.\nYour task is to analyze user queries and recommend the most suitable products from the available inventory.\n\nEach product is provided as a set of key-value pairs (field: value).\nPlease use all available information to make your recommendations.\n\nGuidelines:\n1. Consider the user's specific needs and preferences\n2. Match products based on functionality, features, and user intent\n3. Consider price sensitivity and value for money\n4. Prioritize products that best match the user's query\n5. Return only the product IDs (comma-separated) of the most relevant products\n6. Limit recommendations to the requested number\n\nExample response format: \"1, 5, 12\" (product IDs)""")

    def _build_user_prompt(self, query: str, products_text: str, limit: int) -> str:
        """
        构建用户提示词
        Build user prompt
        Args:
            query: 用户查询 / User query
            products_text: 商品信息文本 / Product info text
            limit: 推荐数量限制 / Recommendation limit
        Returns:
            用户提示词 / User prompt
        """
        return (f"""User query: \"{query}\"\n\nPlease recommend the top {limit} most suitable products from the following inventory:\n\n{products_text}\n\nReturn only the product IDs (comma-separated) of the most relevant products:""")

    def _parse_gpt_response(self, gpt_response: str) -> List[int]:
        """
        解析 GPT 响应，提取商品ID
        Parse GPT response, extract product IDs
        Args:
            gpt_response: GPT 响应文本 / GPT response text
        Returns:
            商品ID列表 / List of product IDs
        """
        try:
            product_ids = [int(x.strip())
                           for x in re.findall(r'\d+', gpt_response)]
            return product_ids
        except Exception as e:
            logger.error(f"Error parsing GPT response: {e}")
            return []

    def _find_products_by_ids(self, product_ids: List[int], products: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        根据ID查找商品
        Find products by ID
        Args:
            product_ids: 商品ID列表 / List of product IDs
            products: 所有商品列表 / All products list
        Returns:
            匹配的商品列表 / List of matched products
        """
        recommended_products = []
        for product_id in product_ids:
            for product in products:
                if str(product.get('id')) == str(product_id):
                    recommended_products.append(product)
                    break
        return recommended_products

    async def get_recommendations(self, query: str, products: List[Dict[str, Any]], limit: int = 3) -> List[Dict[str, Any]]:
        """
        使用 GPT 进行智能商品推荐
        Use GPT for intelligent product recommendation
        Args:
            query: 用户查询 / User query
            products: 商品列表 / List of products
            limit: 推荐数量限制 / Recommendation limit
        Returns:
            推荐的商品列表 / List of recommended products
        """
        if not self.api_key:
            logger.warning(
                f"{self.llm_provider.upper()} API key not available, skipping GPT recommendation")
            return []
        try:
            products_text = self._build_products_text(products)
            system_prompt = self._build_system_prompt()
            user_prompt = self._build_user_prompt(query, products_text, limit)
            headers = {
                "Content-Type": "application/json",
                "Authorization": f"Bearer {self.api_key}"
            }
            payload = {
                "model": "gpt-4o",
                "messages": [
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                "max_tokens": 100,
                "temperature": 0.3
            }
            timeout = aiohttp.ClientTimeout(total=30)

            async with GPT_API_SEMAPHORE:
                async for attempt in AsyncRetrying(stop=stop_after_attempt(3), wait=wait_fixed(2), reraise=True):
                    with attempt:
                        async with aiohttp.ClientSession(timeout=timeout) as session:
                            async with session.post(self.api_url, headers=headers, json=payload, proxy=PROXY_URL, ssl=False) as resp:
                                if resp.status == 200:
                                    result = await resp.json()
                                    gpt_response = result["choices"][0]["message"]["content"].strip(
                                    )
                                    product_ids = self._parse_gpt_response(
                                        gpt_response)
                                    recommended_products = self._find_products_by_ids(
                                        product_ids, products)
                                    logger.info(
                                        f"GPT recommended products: {product_ids}")
                                    return recommended_products[:limit]
                                else:
                                    logger.error(
                                        f"GPT API error: {resp.status}")
                                    raise Exception(
                                        f"GPT API error: {resp.status}")
            return []
        except Exception as e:
            logger.error(f"Error calling GPT API: {e}")
            return []

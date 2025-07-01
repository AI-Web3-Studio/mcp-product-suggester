"""
工具函数模块

包含格式化响应、分类处理等通用功能
"""

from typing import List, Dict, Any


def extract_search_query(text: str) -> str:
    """
    从用户消息中提取搜索查询

    Args:
        text: 用户消息

    Returns:
        提取的搜索查询
    """
    # 简单的关键词提取，实际项目中可以用更复杂的 NLP
    text_lower = text.lower()

    # 移除常见的询问词
    remove_words = ["i want", "i need", "looking for", "search for",
                    "find", "buy", "purchase", "recommend", "suggest"]
    for word in remove_words:
        text_lower = text_lower.replace(word, "").strip()

    return text_lower if text_lower else text


def is_product_search_intent(text: str) -> bool:
    """
    判断用户是否有商品搜索意图

    Args:
        text: 用户消息

    Returns:
        是否有搜索意图
    """
    text_lower = text.lower()

    # 商品搜索关键词
    product_keywords = [
        "buy", "purchase", "shop", "product", "item", "vibrator", "toy", "lube", "oil",
        "ring", "egg", "anal", "massage", "couples", "recommend", "suggest", "find",
        "looking for", "need", "want", "search", "browse", "category", "type"
    ]

    # 检查是否包含商品搜索关键词
    return any(keyword in text_lower for keyword in product_keywords)

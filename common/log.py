# 日志模块
# Logging module

import logging
import sys

# 创建并配置日志记录器 / Create and configure logger
logger = logging.getLogger("mcp-product-suggester")
logger.setLevel(logging.INFO)

handler = logging.StreamHandler(sys.stdout)
formatter = logging.Formatter(
    '[%(asctime)s] %(levelname)s %(name)s: %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)

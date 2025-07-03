# 日志模块
# Logging module

import logging
import sys
import os

# 日志目录和文件
log_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'logs')
os.makedirs(log_dir, exist_ok=True)
log_file = os.path.join(log_dir, 'mcp-server.log')

# 创建并配置日志记录器 / Create and configure logger
logger = logging.getLogger("mcp-server")
logger.setLevel(logging.INFO)

# 文件日志处理器
file_handler = logging.FileHandler(log_file, encoding='utf-8')
file_formatter = logging.Formatter('[%(asctime)s] %(levelname)s %(name)s: %(message)s')
file_handler.setFormatter(file_formatter)
logger.addHandler(file_handler)

# 控制台日志处理器
stream_handler = logging.StreamHandler(sys.stdout)
stream_handler.setFormatter(file_formatter)
logger.addHandler(stream_handler)

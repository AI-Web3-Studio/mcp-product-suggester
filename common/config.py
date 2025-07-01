from dotenv import load_dotenv
import os

# 自动加载根目录下的 .env 文件
# Automatically load the .env file in the project root directory
load_dotenv(dotenv_path=os.path.join(
    os.path.dirname(os.path.dirname(__file__)), '.env'))

# 数据库配置 / Database configuration
DB_ADMIN = {
    'HOST': os.getenv('DB_HOST', 'localhost'),
    'PORT': int(os.getenv('DB_PORT', 3306)),
    'USER': os.getenv('DB_USER', 'root'),
    'PASS': os.getenv('DB_PASS', 'password'),
    'BASE': os.getenv('DB_BASE', 'product_db'),
}

# Redis 配置 / Redis configuration
REDIS_CONFIG = {
    'HOST': os.getenv('REDIS_HOST', 'localhost'),
    'PORT': int(os.getenv('REDIS_PORT', 6379)),
    'DB': int(os.getenv('REDIS_DB', 0)),
    'PASSWORD': os.getenv('REDIS_PASSWORD', None),
}

# 商品表名和SQL模板（极简通用模式，适配任意表结构）
# Product table name and SQL template (minimal universal mode, supports any table structure)
PRODUCT_TABLE = os.getenv('PRODUCT_TABLE', 'product_meta')
PRODUCT_SQL_TEMPLATE = os.getenv(
    'PRODUCT_SQL_TEMPLATE',
    'SELECT * FROM {table} WHERE deleted_at IS NULL AND available = 1 ORDER BY created_at DESC LIMIT {limit}'
)

# 大模型服务配置（支持 monica/openai，可扩展）
# LLM service configuration (supports monica/openai, extensible)
# 可选 monica/openai / Options: monica/openai
LLM_PROVIDER = os.getenv('LLM_PROVIDER', 'monica')
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY', '')
MONICA_API_KEY = os.getenv('MONICA_API_KEY', '')

# 代理配置（如需 HTTP/HTTPS 代理）
# Proxy configuration (for HTTP/HTTPS proxy if needed)
PROXY_URL = os.getenv('PROXY_URL', None)

# 其他业务相关配置可在此扩展
# Other business-related configurations can be extended here

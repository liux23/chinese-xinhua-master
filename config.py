import os
from pathlib import Path

# 项目根目录（自动检测）
PROJECT_ROOT = Path(__file__).resolve().parent

# 数据目录
DATA_DIR = PROJECT_ROOT / 'data'
TEMPLATE_DIR = PROJECT_ROOT / 'templates'
STATIC_DIR = PROJECT_ROOT / 'src' / 'static'

# 数据库配置（优先读环境变量，否则使用默认值）
DB_HOST = os.environ.get('DB_HOST', '127.0.0.1')
DB_NAME = os.environ.get('DB_NAME', 'communicate_sql')
DB_USER = os.environ.get('DB_USER', 'root')
DB_PASSWORD = os.environ.get('DB_PASSWORD', 'lx102326')

# Flask 配置
SECRET_KEY = os.environ.get('SECRET_KEY', 'your_secret_key')

# Redis 配置
REDIS_SERVER_PATH = os.environ.get(
    'REDIS_SERVER_PATH',
    r"D:\work software\redis\Redis\redis-server.exe",
)
REDIS_CONF_PATH = os.environ.get(
    'REDIS_CONF_PATH',
    r"D:\work software\redis\Redis\redis.windows.conf",
)
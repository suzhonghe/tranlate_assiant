"""
配置文件
"""
import os
from dotenv import load_dotenv

load_dotenv()

# DeepSeek API配置
DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY", "")
DEEPSEEK_API_URL = os.getenv("DEEPSEEK_API_URL", "https://api.deepseek.com/v1/chat/completions")

# 模型配置
MODEL_NAME = "deepseek-chat"
MAX_TOKENS = 4000
TEMPERATURE = 0.7

# 服务器配置
HOST = "0.0.0.0"
PORT = 8000


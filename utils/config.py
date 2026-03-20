import os
from dotenv import load_dotenv

load_dotenv()


class Settings:
    PROJECT_NAME = "Intel Agent Platform"
    PROJECT_VERSION = "0.1.0"

    DASHSCOPE_API_KEY = os.getenv("DASHSCOPE_API_KEY", "")
    MODEL_NAME = os.getenv("MODEL_NAME", "qwen-turbo")

    DATA_DIR = "data"
    RAW_DATA_DIR = os.path.join(DATA_DIR, "raw")
    PROCESSED_DATA_DIR = os.path.join(DATA_DIR, "processed")
    REPORTS_DIR = os.path.join(DATA_DIR, "reports")

    DEBUG = os.getenv("DEBUG", "true").lower() == "true"

    WEB_SEARCH_MODE = os.getenv("WEB_SEARCH_MODE", "mock").lower()
    KB_SEARCH_MODE = os.getenv("KB_SEARCH_MODE", "mock").lower()

    # 先预留，后面接真实服务时再用
    SERPAPI_API_KEY = os.getenv("SERPAPI_API_KEY", "")
    RAG_BACKEND = os.getenv("RAG_BACKEND", "mock").lower()


settings = Settings()
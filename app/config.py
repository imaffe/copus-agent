from pydantic_settings import BaseSettings
from functools import lru_cache
import os

class Settings(BaseSettings):
    mongodb_connection_string: str
    mongodb_db_name: str
    mongodb_collection_name: str
    openai_api_key: str

    class Config:
        env_file = ".env"

@lru_cache()
def get_settings():
    return Settings() 
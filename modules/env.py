import os
from dotenv import load_dotenv

def read_env(key: str) -> str:
    load_dotenv('.env')
    value = os.getenv(key)
    return value if value else None
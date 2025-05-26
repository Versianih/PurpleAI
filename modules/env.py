import os
from dotenv import load_dotenv

def read_env(key):
    load_dotenv()
    try:
        value = os.getenv(key)
    except:
        return None
    finally:
        return value
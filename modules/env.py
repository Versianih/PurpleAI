import os
import requests
from dotenv import load_dotenv

def read_env(key: str) -> str:
    load_dotenv('.env')
    value = os.getenv(key)
    return value if value else None

def validate_api_key(key):
    url = "https://api.groq.com/openai/v1/models" 
    headers = {
        "Authorization": f"Bearer {key}"
    }
    
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return True
        else:
            return False
    except Exception as e:
        return False
import os
import requests
from dotenv import load_dotenv, set_key
from path import P


class Env:
    @staticmethod
    def read_env(key: str) -> str:
        load_dotenv(P.env_path)
        value = os.getenv(key)
        return value if value else None

    @staticmethod
    def write_env(key: str, value: str) -> None:
        set_key(P.env_path, key, value)

    @staticmethod
    def validate_api_key(key: str) -> bool:
        url = "https://api.groq.com/openai/v1/models" 
        headers = {
            "Authorization": f"Bearer {key}"
        }

        try:
            response = requests.get(url, headers=headers, timeout=10)
            return response.status_code == 200
        except Exception as e:
            print(f"[ERRO] Falha ao validar API Key: {e}")
            return False

    @staticmethod
    def check_env(self) -> None:
        for i in range(5):
            key_name = f'API_KEY_{i+1}'
            current_key = Env.read_env(key_name)
            if not current_key or not Env.validate_api_key(current_key):
                print(f"❌ - A chave {key_name} está ausente ou inválida.")
                new_key = input(f'Insira a chave de API Groq válida para {key_name}: ')
                while not Env.validate_api_key(new_key):
                    new_key = input(f'Chave inválida. Insira novamente para {key_name}: ')
                Env.write_env(key_name, new_key)
                print(f"{key_name} atualizada com sucesso.")
            else:
                print(f'✅ | {key_name} - {current_key}')
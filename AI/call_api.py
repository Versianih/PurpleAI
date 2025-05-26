from groq import Groq
from pathlib import Path

def call_api(prompt:str, API_KEY:str, model:str):
        client = Groq(api_key=API_KEY)
        try:
            response = client.chat.completions.create(
                messages=[
                    {
                        "role": "user",
                        "content": prompt,
                    }
                ],
                model=model,
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"Error connecting to model: {e}"
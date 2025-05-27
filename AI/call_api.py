from groq import Groq
from pathlib import Path
from prompt import PURPLE_COMET_PROMPT


class QuestionSolver:
    def __init__(self, question, key):
        self.key = key

    def solve_question(self, question:str, model:str = "llama3-70b-8192"):
        prompt = PURPLE_COMET_PROMPT.format(question_text=question)
        client = Groq(api_key=self.key)
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
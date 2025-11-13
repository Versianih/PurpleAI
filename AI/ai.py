from groq import Groq
from AI.prompt import Prompt


class AI:
    def __init__(
            self,
            ai_type: str = 'SOLVER',
            api_key: str = ''
        ):
        
        self.ai_type = ai_type
        self.api_key = api_key

    def call(
        self,
        api_key: str,
        content: str = ''
        ) -> str | Exception:
        
        prompt = Prompt.get_prompt(self.ai_type, content)
        client = Groq(api_key=api_key)
        try:
            response = client.chat.completions.create(
                messages=[
                    {
                        "role": "user",
                        "content": prompt,
                    }
                ],
                model=self._get_model(),
            )
            return response.choices[0].message.content
        except Exception as error:
            return error

    def _get_model(self) -> str:
        match self.ai_type:
            case 'SOLVER':
                return 'openai/gpt-oss-120b'
            case 'CONVERTER':
                return ''
            case _:
                return
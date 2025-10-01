from groq import Groq
from AI.prompt import PURPLE_COMET_PROMPT

class AI:
    def __init__(self, type_call: str):
        self.type_call = type_call
        self.prompt = ''
        self.model = ''

    def call(self, key: str, content: str) -> str:
        method = self._set_method()
        response = method(key=key, content=content)

        return response
    
    def _set_method(self) -> function | RuntimeError:
        match self.type_call:
            case 'solver':
                return self._call_solver
            case 'transcribe':
                return self._call_transcribe
            case _:
                raise RuntimeError('Método de chamada de IA desconhecido')

    def _call_solver(self, key: str, content: str) -> str:
        prompt = PURPLE_COMET_PROMPT.format(question_text=content)
        client = Groq(api_key=key)

        response = self.__call_llm(client, prompt)
        
    def _call_transcribe() -> str:
        ...

    def __call_llm(self, client: Groq, prompt: str):
        try:
            response = client.chat.completions.create(
                messages=[
                    {
                        "role": "user",
                        "content": prompt,
                    }
                ],
                model=self.model,
            )
            return response.choices[0].message.content
        except Exception as e:
            error_msg = f"Error connecting to model: {e}"
            return error_msg
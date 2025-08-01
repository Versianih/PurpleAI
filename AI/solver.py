import concurrent.futures
from groq import Groq
from AI.prompt import PURPLE_COMET_PROMPT
from modules.env import Env
from typing import List, Dict
from time import sleep, perf_counter


class QuestionSolver:
    def __init__(self, questions: List[str], seasons: int = 5, parallel: bool = False, model: str = "llama3-70b-8192", debug: bool = False) -> None:
        self.model = model
        self.seasons = seasons
        self.parallel = parallel
        self.questions = questions
        self.debug = debug
        self.answers = {}
        self.time_solver = 0
        
        self.API_KEYS = [
            Env.read_env('API_KEY_1'), 
            Env.read_env('API_KEY_2'),
            Env.read_env('API_KEY_3'), 
            Env.read_env('API_KEY_4'), 
            Env.read_env('API_KEY_5')
        ]
        
        if not self.API_KEYS:
            raise ValueError("Nenhuma chave de API válida encontrada!")


    def solve(self) -> None:
        """
        Método para iniciar a resolução das questões
        """
        if not self.parallel: self.distribute_questions()
        else: self.distribute_questions_parallel()

        self.final_answer()



    def distribute_questions(self) -> None:
        """
        Distribui as questões entre as APIs e resolve todas em múltiplas seasons
        """
        questions_distribution = {
            0: [1, 6, 11, 16, 21, 26],   # API_KEY_1
            1: [2, 7, 12, 17, 22, 27],   # API_KEY_2  
            2: [3, 8, 13, 18, 23, 28],   # API_KEY_3
            3: [4, 9, 14, 19, 24, 29],   # API_KEY_4
            4: [5, 10, 15, 20, 25, 30]   # API_KEY_5
        }
        
        print(f"Iniciando {self.seasons} seasons de processamento...\n")
        start_solver = perf_counter()
        
        for season in range(self.seasons):
            print(f"Season {season + 1}/{self.seasons}")
            season_answers = {}
            start_season = perf_counter()

            for i in range(len(self.questions) // 5):
                for api_index, question_numbers in questions_distribution.items():
                    if api_index >= len(self.API_KEYS):
                        continue

                    if question_numbers[i] <= len(self.questions):
                        question_text = self.questions[question_numbers[i] - 1]
                        
                        print(f"  | ⏳ Processando questão {question_numbers[i]}", end="", flush=True)
                        answer = self.call_api(self.API_KEYS[api_index], question_text)
                        answer = '-' if not answer.isdigit() else answer
                        season_answers[question_numbers[i]] = answer
                        print('\r' + ' ' * 100 + '\r', end='', flush=True)
                        print(f"  | {'✅' if answer != '-' else '❌'} Questão {question_numbers[i]} processada")
                        sleep(0.1)

            self.answers[f'season_{season + 1}'] = dict(sorted(season_answers.items()))
            
            print(f"Season {season + 1} completa.")
            print(f"Tempo de execução da Season: {round(perf_counter() - start_season, 4)}s\n")

        end_solver = perf_counter()
        exec_time_solver = round(end_solver - start_solver, 4)
        
        self.time_solver = exec_time_solver


    def distribute_questions_parallel(self) -> None:
        """
        Versão paralela da distribuição.
        (Método não testado, pode apresentar falhas)
        """
        questions_distribution = {
            0: [1, 6, 11, 16, 21, 26],
            1: [2, 7, 12, 17, 22, 27],
            2: [3, 8, 13, 18, 23, 28],
            3: [4, 9, 14, 19, 24, 29],
            4: [5, 10, 15, 20, 25, 30]
        }

        print(f"Iniciando {self.seasons} seasons de processamento em paralelo...\n")
        start_solver = perf_counter()
        
        for season in range(self.seasons):
            print(f"Season {season + 1}/{self.seasons}")
            start_season = perf_counter()
            season_answers = {}
            tasks = []

            for api_index, question_numbers in questions_distribution.items():
                if api_index >= len(self.API_KEYS):
                    continue

                api_key = self.API_KEYS[api_index]
                for question_num in question_numbers:
                    if question_num <= len(self.questions):
                        question_text = self.questions[question_num - 1]
                        tasks.append((api_key, question_text, question_num))

            with concurrent.futures.ThreadPoolExecutor(max_workers=len(self.API_KEYS)) as executor:
                future_to_question = {}
                batch_size = 2

                for i in range(0, len(tasks), batch_size):
                    batch = tasks[i:i+batch_size]
                    for task in batch:
                        future_to_question[executor.submit(self.call_api, task[0], task[1])] = task[2]
                    
                    if i + batch_size < len(tasks):
                        sleep(1)

                for future in concurrent.futures.as_completed(future_to_question):
                    question_num = future_to_question[future]
                    try:
                        answer = future.result()
                        answer = '-' if not answer.isdigit() else answer
                        season_answers[question_num] = answer
                        print(f"  | {'✅' if answer != '-' else '❌'} Questão {question_num} processada")
                    except Exception as exc:
                        print(f"  | ❌ Erro na questão {question_num}")
                        season_answers[question_num] = "-"

            self.answers[f'season_{season + 1}'] = dict(sorted(season_answers.items()))
            print(f"Season {season + 1} completa.")
            print(f"Tempo de execução da Season: {round(perf_counter() - start_season, 4)}s\n")

        exec_time_solver = round(perf_counter() - start_solver, 4)
        print(f'Tempo de execução total em paralelo: {exec_time_solver}s\n')
        
        self.time_solver = exec_time_solver


    def call_api(self, key: str, question: str) -> str:
        """
        Resolve uma questão individual
        """
        prompt = PURPLE_COMET_PROMPT.format(question_text=question)
        client = Groq(api_key=key)
        
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
            print(f"  | {error_msg}") if self.debug == True else None
            return error_msg

    
    def final_answer(self) -> None:
        """
        Cria uma season final com as respostas final.
        Se mais da metade das seasons conter a mesma resposta, logo
        essa resposta será a resposta final, caso contrário a resposta
        final será '-'
        """
        
        final_answers = {}
        total_seasons = len(self.answers)
        
        for question_num in range(1, 31):
            answers_for_question = []
            
            for season_data in self.answers.values():
                if question_num in season_data:
                    answer = season_data[question_num]
                    # Ignora respostas vazias, erros ou '-'
                    if answer and answer != '-':
                        answers_for_question.append(answer.strip())
            
            if not answers_for_question:
                final_answers[question_num] = '-'
                continue
            
            answer_counts = {}
            for answer in answers_for_question:
                answer_counts[answer] = answer_counts.get(answer, 0) + 1
            
            most_common_answer = max(answer_counts.items(), key=lambda x: x[1])
            most_common_count = most_common_answer[1]
            most_common_text = most_common_answer[0]
            
            required_consensus = total_seasons / 2
            
            if most_common_count > required_consensus:
                final_answers[question_num] = most_common_text
            else:
                final_answers[question_num] = '-'
        
        self.answers['final_season'] = dict(sorted(final_answers.items()))


    def get_season_answers(self, season: int = None) -> Dict[str, Dict[int, int]]:
        """
        Retorna as respostas de uma season específica 
        ou todas caso não especificado uma season.
        """
        if season is None:
            return self.answers
        
        season_key = f'season_{season}'
        return self.answers.get(season_key, {})


    def get_exec_time(self) -> float:
        """
        Retorna o tempo de execução do último solve
        """
        return self.time_solver
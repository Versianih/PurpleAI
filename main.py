from AI.solver import QuestionSolver
from test import questions
from modules.data import collect_data
from modules.results import Results

# seasons, exam_path = collect_data()

solver = QuestionSolver(questions=questions, seasons=int(input('Número de seasons: ')), parallel=False)
results = Results(solver.get_season_answers(), solver.get_exec_time())
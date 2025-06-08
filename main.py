import sys
from AI.solver import QuestionSolver
from test import questions
from modules.data import Data
from modules.results import Results

data = Data.exec()

if data:

    line_command = sys.argv
    parallel = True if '-p' in line_command else False

    questions_list = []

    solver = QuestionSolver(questions=questions, seasons=data['seasons'], parallel=parallel)

    results = Results(solver.get_season_answers(), solver.get_exec_time(), show = True, save=True)
import sys
from pathlib import Path
from AI.solver import QuestionSolver
from modules.data import Data
from modules.results import Results
from modules.converter import Converter
from path import P

window = Data()
data = window.exec()

if data:

    line_command = sys.argv
    parallel = True if '-p' in line_command else False

    converter = Converter(data['exam_path'])
    questions_list = converter.get_problem_list()

    solver = QuestionSolver(questions=questions_list, seasons=data['seasons'], parallel=parallel)

    results = Results(solver.get_season_answers(), solver.get_exec_time(), show = True, save=True, save_filename=input('Digite o nome do arquivo a ser salvo: '))
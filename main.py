import sys
from AI.solver import QuestionSolver
from modules.data import Data
from modules.results import Results
from modules.converter import Converter

window = Data()
data = window.exec()

if data:

    line_command = sys.argv
    parallel = '-p' in line_command

    converter = Converter(data['exam_path'])
    questions_list = converter.get_problem_list()

    solver = QuestionSolver(
        questions = questions_list, 
        seasons = data['seasons'], 
        parallel = parallel
        )
    solver.solve()

    results = Results(
        object_solver = solver, 
        object_converter = converter,
        pre_data = data, 
        show = True, 
        save = True
        )
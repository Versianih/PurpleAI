import sys, os, shutil
from path import P
from modules.env import Env

line_command = sys.argv

try:
    if line_command[1] == '-h':
        print('Help')

    if line_command[1] == '-e' and line_command[2] == 'check':
        Env.check_env()

    if line_command[1] == '-c' and line_command[2] == 'output':
        if os.path.isdir(P.output_path):
            shutil.rmtree(P.output_path)
            os.makedirs('outputs')
            print(f"Outputs limpos com sucesso.")
        else:
            os.makedirs('outputs')
            print(f"Diretório de output não encontrado.")
except:
    print("\ntry: tools.py -h, for help.")
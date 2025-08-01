import sys, os, shutil
from path import P
from modules.env import Env

line_command = sys.argv

def help():
    help = """
    Uso: tools.py [opções]

    Opções:
      -help, --help    Mostra esta mensagem de ajuda.
      --setup          Cria o diretório de saída.
      --clear-output   Limpa os arquivos de saída.
    """
    print(help)


if __name__ == '__main__':
    try:
        if line_command[1] in ['-help', '--help', 'help']:
            help()

        if line_command[1] == '--setup':
            if not os.path.isdir(P.output_path):
                os.makedirs('output')
                print("Diretório de output criado com sucesso.")
            else: print("Diretório de output já existente.")

            Env.check_env()

        if line_command[1] == '--clear-output':
            if os.path.isdir(P.output_path):
                shutil.rmtree(P.output_path)
                print(f"Outputs limpos com sucesso.")
            else:
                print(f"Diretório de output não encontrado.")
            os.makedirs('output') if not os.path.isdir(P.output_path) else None
    except:
        print("\ntry: tools.py -h, for help.")
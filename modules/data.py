import os
import tkinter as tk
from tkinter.filedialog import askopenfilename

def open_file_select() -> str:
    tk.Tk().withdraw()
    file_path = askopenfilename()
    
    return file_path

def collect_data():
    """
    Função que coleta e valida os dados do usuário (número de seasons e caminho do arquivo)
    com possibilidade de edição até a confirmação final.
    Retorna (seasons, exam_path) após confirmação.
    """
    while True:
        os.system('cls' if 'nt' in os.name else 'clear')

        seasons = input('Digite o número de seasons: ')
        while not seasons.isdigit() or int(seasons) <= 0:
            seasons = input('Digite um número válido de seasons: ')
        seasons = int(seasons)

        print('Selecione o arquivo da Prova...')
        exam_path = open_file_select()

        if exam_path is None:
            print('\nNenhum arquivo selecionado. Operação cancelada.')
            return None, None

        while True:
            os.system('cls' if 'nt' in os.name else 'clear')
            print('Dados Confirmados:')
            print(f'  | Número de seasons: {seasons}')
            print(f'  | Caminho do arquivo da prova: {exam_path}\n')

            option = input('Deseja alterar algum dado? (s/n): ').strip().lower()
            if option == 'n':
                return seasons, exam_path
            elif option == 's':
                break
            else:
                print('⚠️ Opção inválida. Digite "s" para sim ou "n" para não.\n')
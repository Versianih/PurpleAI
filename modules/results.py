import os
from AI.solver import QuestionSolver
from typing import Dict
from pathlib import Path
from path import P
from tabulate import tabulate


class Results:
    def __init__(self, object_solver: QuestionSolver, save_filename: str = 'results', save: bool = False, show: bool = False):
        self.data = object_solver.get_season_answers()
        self.time = object_solver.get_exec_time()
        self.show = show
        self.save = save
        self.save_filename = f'{save_filename}.md'
        self.save_path = Path(P.output_path) / save_filename

        if self.save and self.save_path:
            self.save_results()
        if self.show:
            self.show_results()


    def show_results(self) -> str:
        """
        Printa no terminal as respostas de cada season estruturadas
        em uma tabela juntamente com resultado final e tempo de execução.
        """
        header_labels = [""]
        for key in self.data.keys():
            if key == "final_season":
                header_labels.append("R.F.")
            elif key.startswith("season_"):
                try:
                    num = int(key.split("_")[1])
                    header_labels.append(f"S{num}")
                except (IndexError, ValueError):
                    header_labels.append(key)
            else:
                header_labels.append(key)

        headers = header_labels

        table_data = []
        for questao in range(1, 31):
            linha = [questao]
            for season in self.data:
                resposta = self.data[season].get(questao, "")
                linha.append(resposta)
            table_data.append(linha)

        table = tabulate(table_data, headers=headers, tablefmt="grid")
        
        print(f'\n{table}\n')
        print(f'  | ⏰ Tempo de execução total: {self.time}s')


    def save_results(self) -> None:
        """
        Salva os resultados em um arquivo .md com formato Markdown.
        Exemplo do nome do arquivo: results.md
        """
        if not os.path.exists(self.save_path):
            os.makedirs(self.save_path)

        # Cabeçalho da tabela
        headers = ["Questão"]
        season_keys = []
        final_key = None

        for key in self.data.keys():
            if key == "final_season":
                headers.append("Resposta Final")
                final_key = key
            elif key.startswith("season_"):
                try:
                    num = int(key.split("_")[1])
                    headers.append(f"Season {num}")
                    season_keys.append(key)
                except (IndexError, ValueError):
                    headers.append(key)
                    season_keys.append(key)

        header_line = "|" + "|".join(headers) + "|"
        separator_line = "|" + "-|" * (len(headers) - 1) + "-|"

        # Linhas da tabela
        table_lines = []
        for questao in range(1, 31):
            linha = [f"Questão {questao}"]
            for season in season_keys:
                resposta = self.data[season].get(questao, "")
                linha.append(str(resposta) if resposta is not None else "")
            if final_key and questao in self.data[final_key]:
                linha.append(str(self.data[final_key][questao]))
            else:
                linha.append("")
            table_lines.append("|" + "|".join(linha) + "|")

        # Conteúdo completo do arquivo
        content_file = [header_line, separator_line] + table_lines

        caminho_arquivo = os.path.join(self.save_path, self.save_filename)
        with open(caminho_arquivo, 'w', encoding='utf-8') as file:
            file.write("\n".join(content_file))
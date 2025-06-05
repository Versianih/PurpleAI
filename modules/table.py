from typing import Dict
from tabulate import tabulate


class Results:
    def __init__(self, data:Dict, save:bool = True, show: bool = True):
        self.data = data
        self.show = show
        self.save = save

        if self.save:
            self.save_results()
        if self.show:
            self.show_results()


    @staticmethod
    def show_results(self) -> str:
        header_labels = []
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

        headers = [""] + header_labels

        table_data = []
        for questao in range(1, 31):
            linha = [questao]
            for season in self.data:
                resposta = self.data[season].get(questao, "")
                linha.append(resposta)
            table_data.append(linha)

        table = tabulate(table_data, headers=headers, tablefmt="grid")
        
        print(f'\n{table}')


    @staticmethod
    def save_results(self):
        pass
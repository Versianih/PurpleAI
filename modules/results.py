from typing import Dict
from tabulate import tabulate


class Results:
    def __init__(self, data:Dict[str, dict], time:float, save:bool = False, show: bool = False):
        self.data = data
        self.time = time
        self.show = show
        self.save = save

        if self.save:
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


    def save_results(self, file_name:str = None) -> None:
        """
        file_name = (id)_(seasons)_(parallel)_(date)
        ex: 2_5_0_06062025.md
        """
        pass
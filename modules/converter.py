import re
from path import P
from PyPDF2 import PdfReader

class Converter:
    """
    Testing class
    """
    def __init__(self, pdf_path):
        self.pdf_path = pdf_path
        self.raw_text = ""
        self.problems = []

        self.parse_problems()

    def extract_text(self):
        reader = PdfReader(self.pdf_path)
        text = ""
        for page in reader.pages:
            text += page.extract_text() + "\n"
        self.raw_text = text

    def parse_problems(self):
        # Garante que o texto foi extraído
        if not self.raw_text:
            self.extract_text()
        
        # Remove quebras excessivas e junta linhas quebradas no meio de frases
        clean_text = re.sub(r'\n(?=\S)', ' ', self.raw_text)
        
        # Expressão regular que encontra os enunciados dos problemas
        problem_split = re.split(r'(?=Problema\s+\d+)', clean_text)

        # Remove qualquer texto antes do primeiro problema e após o problema 30
        problems = [p.strip() for p in problem_split if p.strip().startswith("Problema")]
        
        # Garante que temos 30 problemas
        if len(problems) != 30:
            raise ValueError(f"Erro: esperados 30 problemas, mas foram encontrados {len(problems)}.")
        
        self.problems = problems

    def get_problem_list(self):
        if not self.problems:
            self.parse_problems()
        return self.problems

    def save_as_markdown(self, output_path):
        if not self.problems:
            self.parse_problems()
        with open(output_path, "w", encoding="utf-8") as f:
            for i, problem in enumerate(self.problems, start=1):
                f.write(f"## Problema {i}\n\n{problem}\n\n---\n\n")
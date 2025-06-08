import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import os

class Data:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("PurpleAI")
        self.root.geometry("400x320")
        self.root.resizable(False, False)
        
        self.arquivo_selecionado = ""
        self.seasons = tk.StringVar()
        self.seasons.trace('w', self.validar_campos)
        self.dados_salvos = None
        
        self.criar_interface()
        self.centralizar_janela()
        
    def criar_interface(self):
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)

        titulo = ttk.Label(main_frame, text="PurpleAI", font=("Arial", 16, "bold"))
        titulo.pack(pady=(0, 20))

        seasons_frame = ttk.Frame(main_frame)
        seasons_frame.pack(fill=tk.X, pady=(0, 15))
        
        ttk.Label(seasons_frame, text="Número de Seasons:").pack(anchor=tk.W)
        self.entry_seasons = ttk.Entry(seasons_frame, textvariable=self.seasons)
        self.entry_seasons.pack(fill=tk.X, pady=(5, 0))

        self.label_erro_seasons = ttk.Label(seasons_frame, text="", foreground="red", font=("Arial", 8))
        self.label_erro_seasons.pack(anchor=tk.W)

        arquivo_frame = ttk.Frame(main_frame)
        arquivo_frame.pack(fill=tk.X, pady=(0, 15))
        
        ttk.Label(arquivo_frame, text="Arquivo da Prova:").pack(anchor=tk.W)

        arquivo_input_frame = ttk.Frame(arquivo_frame)
        arquivo_input_frame.pack(fill=tk.X, pady=(5, 0))
        
        self.entry_arquivo = ttk.Entry(arquivo_input_frame, state="readonly")
        self.entry_arquivo.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        self.btn_selecionar = ttk.Button(arquivo_input_frame, text="Procurar...", command=self.selecionar_arquivo)
        self.btn_selecionar.pack(side=tk.RIGHT, padx=(5, 0))
        
        self.label_erro_arquivo = ttk.Label(arquivo_frame, text="", foreground="red", font=("Arial", 8))
        self.label_erro_arquivo.pack(anchor=tk.W, pady=(2, 0))
        
        btn_frame = ttk.Frame(main_frame)
        btn_frame.pack(fill=tk.X, pady=(25, 0))
        
        self.btn_salvar = ttk.Button(btn_frame, text="Salvar", command=self.salvar, state="disabled")
        self.btn_salvar.pack(fill=tk.X)

        self.validar_campos()
        
    def centralizar_janela(self):
        self.root.update_idletasks()
        x = (self.root.winfo_screenwidth() // 2) - (self.root.winfo_width() // 2)
        y = (self.root.winfo_screenheight() // 2) - (self.root.winfo_height() // 2)
        self.root.geometry(f"+{x}+{y}")
        
    def validar_seasons(self):
        valor = self.seasons.get().strip()
        
        if not valor:
            self.label_erro_seasons.config(text="Campo obrigatório")
            return False
            
        try:
            num = int(valor)
            if num <= 0:
                self.label_erro_seasons.config(text="Deve ser um número inteiro positivo")
                return False
            else:
                self.label_erro_seasons.config(text="")
                return True
        except ValueError:
            self.label_erro_seasons.config(text="Deve ser um número inteiro válido")
            return False
            
    def validar_arquivo(self):
        if not self.arquivo_selecionado or not os.path.exists(self.arquivo_selecionado):
            self.label_erro_arquivo.config(text="Selecione um arquivo válido")
            return False
        else:
            self.label_erro_arquivo.config(text="")
            return True
            
    def validar_campos(self, *args):
        seasons_valido = self.validar_seasons()
        arquivo_valido = self.validar_arquivo()
        
        if seasons_valido and arquivo_valido:
            self.btn_salvar.config(state="normal")
        else:
            self.btn_salvar.config(state="disabled")
            
    def selecionar_arquivo(self):
        arquivo = filedialog.askopenfilename(
            title="Selecionar Arquivo da Prova",
            filetypes=[
                ("Todos os arquivos", "*.*"),
                ("Arquivos de texto", "*.txt"),
                ("Arquivos PDF", "*.pdf"),
                ("Arquivos Word", "*.docx"),
                ("Arquivos Excel", "*.xlsx")
            ]
        )
        
        if arquivo:
            self.arquivo_selecionado = arquivo

            nome_arquivo = os.path.basename(arquivo)
            self.entry_arquivo.config(state="normal")
            self.entry_arquivo.delete(0, tk.END)
            self.entry_arquivo.insert(0, nome_arquivo)
            self.entry_arquivo.config(state="readonly")
            
        self.validar_campos()
        
    def salvar(self):
        seasons = int(self.seasons.get())
        arquivo = self.arquivo_selecionado

        self.dados_salvos = {
            'seasons': seasons,
            'exam_path': arquivo,
        }

        mensagem = f"Dados salvos com sucesso!\n\n"
        mensagem += f"Número de Seasons: {seasons}\n"
        mensagem += f"Arquivo: {os.path.basename(arquivo)}"

        messagebox.showinfo("Sucesso", mensagem)

        self.root.quit()
        
    def exec(self):
        self.root.mainloop()
        return self.dados_salvos
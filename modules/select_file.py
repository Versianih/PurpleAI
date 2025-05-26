import tkinter as tk
from tkinter.filedialog import askopenfilename
import datetime

def open_file_select() -> str:
    tk.Tk().withdraw()
    file_path = askopenfilename()
    
    return file_path
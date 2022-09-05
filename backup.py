import os
import time
from tkinter import messagebox


def backup():
    user = os.getlogin()

    curr_time = time.localtime()
    horario = time.strftime("%d-%b-%Y", curr_time)

    diretorio = f'C:\\Users\\{user}\\Desktop\\Backup'  # Check se pasta existe
    existe = os.path.exists(diretorio)

    os.system(f"cd C:\\Program Files (x86)\\GerenciamentoSunga")

    if existe:
        os.system(f"copy database.db C:\\Users\\{user}\\Desktop\\Backup\\{horario}.db")
    else:
        os.system(f"mkdir C:\\Users\\{user}\\Desktop\\Backup")
        os.system(f"copy database.db C:\\Users\\{user}\\Desktop\\Backup\\{horario}.db")

    messagebox.showinfo("showmessage", "Backup criado com sucesso na area de trabalho!")

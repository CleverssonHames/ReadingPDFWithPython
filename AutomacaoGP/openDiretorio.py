import tkinter as tk
from tkinter import ttk
from tkinter import filedialog

def selecionar_diretorio():
    diretorio = filedialog.askdirectory()
    if diretorio:
        entry_diretorio.delete(0, tk.END)
        entry_diretorio.insert(0, diretorio)

# Cria a janela principal
root = tk.Tk()
root.title("Selecionar Diretório")

# Cria um frame para organizar os widgets
frame = ttk.Frame(root, padding="10")
frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

# Cria um campo de entrada (Entry)
entry_diretorio = ttk.Entry(frame, width=40)
entry_diretorio.grid(row=0, column=0, padx=(0, 10))

# Cria um botão para abrir o diálogo de seleção de diretório
botao_selecionar = ttk.Button(frame, text="Selecionar Diretório", command=selecionar_diretorio)
botao_selecionar.grid(row=0, column=1)

# Inicia o loop principal da interface gráfica
root.mainloop()
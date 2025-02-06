from  PyPDF2 import PdfReader
import re
from pathlib import Path
import shutil
import os
from tkinter import *
from tkinter import filedialog

class Application:
    def __init__(self, master=None):

        self.padrao_cpf = re.compile(r'\b\d{3}\.\d{3}\.\d{3}-\d{2}\b')
        self.cpf_final = ""
        self.erros = 0
        
        self.fonte = ("Verdana", "8")

        self.container1 = Frame(master)
        self.container1["pady"] = 10
        self.container1.pack()

        self.container2 = Frame(master)
        self.container2["padx"] = 20
        self.container2["pady"] = 5
        self.container2.pack()

        self.container3 = Frame(master)
        self.container3["padx"] = 20
        self.container3["pady"] = 5
        self.container3.pack()

        self.container4 = Frame(master)
        self.container4["padx"] = 20
        self.container4["pady"] = 5
        self.container4.pack()

        # Container 1
        self.titulo = Label(self.container1, text="Renomear arquivos de IRRF")
        self.titulo["font"] = ("Calibri", "9", "bold")
        self.titulo.pack ()

        # Container 2
        self.lbpastaorigem = Label(self.container2,
        text="Pasta origem:", font=self.fonte, width=15)
        self.lbpastaorigem.pack(side=LEFT)

        self.txtpastaorigem = Entry(self.container2)
        self.txtpastaorigem["width"] = 30
        self.txtpastaorigem["font"] = self.fonte
        self.txtpastaorigem.pack(side=LEFT)

        def selecionar_diretorio():
            pasta_origem = filedialog.askdirectory()
            if pasta_origem:
                self.txtpastaorigem.delete(0, END)
                self.txtpastaorigem.insert(0, pasta_origem)
                self.txtpastaorigem.config(state='readonly')

        self.btnBuscar = Button(self.container2, text="🔎 Selecionar pasta",
        font=self.fonte, width=16)
        self.btnBuscar["command"] = selecionar_diretorio
        self.btnBuscar.pack(side=RIGHT)

        # Container 3
        def extrai_cpf(path):
            with open(path, 'rb') as arq:
                read_pdf = PdfReader(arq)
                texto = ""
                for pag in  read_pdf.pages:
                    texto += pag.extract_text()
                    if texto:
                        cpf_formatado = self.padrao_cpf.findall(texto)

            return cpf_formatado

        def start_rename():
            
            pasta_origem = Path(f'{self.txtpastaorigem.get()}')
            pasta_destino = Path(f'{pasta_origem}/arquivos_renomeados/')

            pdfs = list(pasta_origem.glob("*.pdf"))
            self.lbtotalarquivos['text'] = f"Arquivos encontrados: {len(pdfs)}"

            contador_arq = 0

            for item in pdfs:

                self.lista.insert(END, f"Extraindo pdf do arquivo: {item}")
                self.lista.see(END)
                root.update()

                # limpar o cpf extraido para não correr o risco de entrar com o mesmo CPF
                cpf_extraido = ""

                try:
                    cpf_extraido = extrai_cpf(item)
                except:
                    self.lista.insert(END,f"Ocorreu um erro na extração do cpf arquivo: {item}")
                    self.lista.see(END)
                    root.update()
                    self.erros += 1

                if cpf_extraido:

                    cpf_final = [re.sub(r'\D', '', cpf) for cpf in cpf_extraido]

                    if (len(cpf_final[0]) == 11):
                        
                        self.lista.insert(END,f"Renomeando arquivo: {item}")
                        self.lista.see(END)
                        root.update()

                        try:
                            pasta_destino_final = f"{pasta_destino}/{cpf_final[0]}{contador_arq}.pdf"
                            os.makedirs(os.path.dirname(pasta_destino_final), exist_ok=True)
                            shutil.copy2(item, pasta_destino_final)
                            contador_arq += 1 
                            self.lbtotalalterados['text'] = f"Arquivos alterados: {contador_arq}"
                        except:
                            self.lista.insert(END,f"Ocorreu um erro na renomeação do arquivo: {item}")
                            self.lista.see(END)
                            root.update()
                            self.erros += 1

                    else:
                        self.lista.insert(END,f"CPF inválido para o arquivo: {item}")
                        self.lista.see(END)
                        root.update()
                        self.erros += 1

                else:

                    self.lista.insert(END,f"Ocorreu um erro na extração do cpf arquivo: {item}")
                    self.lista.see(END)
                    root.update()

            if (self.erros > 0):
                self.lista.insert(END,f" 🔴 Ocorreu um ou mais erros ao renomear os arquivos, confira ")
                self.lista.see(END)
                root.update()
            else:
                self.lista.insert(END,f"🟢 Todos os arquivos foram alterados com sucesso!")
                self.lista.see(END)
                root.update()

                
                    

        self.btnIniciar = Button(self.container3, text="🙈 Iniciar alterações",
        font=self.fonte)
        self.btnIniciar["command"] = start_rename
        self.btnIniciar.pack(expand=True)

        # Container 4
        self.lbtotalarquivos = Label(self.container4, text=f"Todal de arquivos: {0}")
        self.lbtotalarquivos.pack()

        self.lista = Listbox(self.container4, width=700)
        self.lista.pack()

        self.lbtotalalterados = Label(self.container4, text=f"Todal de alterados: {0}")
        self.lbtotalalterados.pack()


root = Tk()
root.title('Read PDF 2')
root.maxsize(800, 600)
Application(root)
root.mainloop()




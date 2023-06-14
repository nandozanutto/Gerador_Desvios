import threading
from logModule import LogModule
import tkinter as tk
import tkinter.ttk as ttk
from tkinter.ttk import *
from ttkthemes import ThemedTk
from tkinter import filedialog
import os
import customtkinter
import gerador as desvio

class main():
    __root = tk.Tk()

    def __init__(self):
        self.setup()
        self.__root.after(100, self.__loadTable())

    def __loadTable(self):
        self.__log.readQueue()
        self.__root.after(150, self.__loadTable)

    def run(self):
        self.__root.mainloop()

    def setup(self):

        self.__root.title('Gerador de palavras')
        # self.nwords_label = customtkinter.CTkLabel(master=self.__root, text="Número de palavras:")
        # self.nwords_label.grid(column=0, row=0, sticky=tk.EW, padx=5, pady=5)
        self.omissao = customtkinter.CTkEntry(master=self.__root, placeholder_text="Omissões")
        self.omissao.grid(sticky=tk.EW, column=0, row=0, padx=5, pady=5)
        self.nfonologica = customtkinter.CTkEntry(master=self.__root, placeholder_text="Subs. não fonológica")
        self.nfonologica.grid(sticky=tk.EW, column=0, row=1, padx=5, pady=5)
        self.fonologica = customtkinter.CTkEntry(master=self.__root, placeholder_text="Subs. intra classe")
        self.fonologica.grid(sticky=tk.EW, column=0, row=2, padx=5, pady=5)
        self.transposicao = customtkinter.CTkEntry(master=self.__root, placeholder_text="Transposição")
        self.transposicao.grid(sticky=tk.EW, column=0, row=3, padx=5, pady=5)
        # run button

        self.words_box = customtkinter.CTkTextbox(master=self.__root, corner_radius=20)
        self.words_box.grid(column=0, row=5, sticky=tk.NS, padx=5, pady=5)

        self.run_button = customtkinter.CTkButton(master=self.__root, text="Gerar palavras", command=self.runScript)
        self.run_button.grid(column=0, row=4, sticky=tk.EW, padx=5, pady=5)

        self.__log = LogModule()
        self.__log.createStructure(master=self.__root, sticky=tk.EW, row = 5, column = 1, labelText='Informações ao usuário',rowspan = 5, rootFrameSpan=((3, 3), (10, 10)))
        self.__log.write("Bem vindo ao gerador de palavras!")
        
        self.check_var = customtkinter.StringVar(value="on")
        self.checkbox = customtkinter.CTkCheckBox(master=self.__root, text="Gerar arquivo excel?", variable=self.check_var, onvalue="on", offvalue="off")
        self.checkbox.grid(column=1, row=0, sticky=tk.EW, padx=5, pady=5)

    def runScript(self):
        omissao = self.omissao.get()
        nfonologica = self.nfonologica.get()
        fonologica = self.fonologica.get()
        transposicao = self.transposicao.get()

        try:
            omissao = int(omissao) if omissao != "" else 0
            nfonologica = int(nfonologica) if nfonologica != "" else 0
            fonologica = int(fonologica) if fonologica != "" else 0
            transposicao = int(transposicao) if transposicao != "" else 0
        except:
            self.__log.write("Digite números nos campos de desvios!")

        text = self.words_box.get("0.0", "end")
        list_of_words = text.split()
        self.gerador = desvio.Gerador(self.__log.write, self.check_var.get())
        dict_input = {"omissao":omissao, "nao fonologica": nfonologica, "fonologica":fonologica, "transposicao": transposicao}

        if(list_of_words):
            self.tUpdate = threading.Thread(target=self.gerador.gerar_desvios, kwargs={'list_word':list_of_words})
        else:  
            self.tUpdate = threading.Thread(target=self.gerador.gerar_desvios_categorias, kwargs={'dict_categorias':dict_input})
        
        self.tUpdate.daemon = True
        self.tUpdate.start()

if __name__ == "__main__":
    app = main()
    app.run()

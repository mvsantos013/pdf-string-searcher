# -*- coding: utf-8 -*-
import os
import time
import utils.network as network
import utils.util as util
from pdf.pdfstringsearcher import PdfStringSearcher
from tkinter import *


class Application:
    def __init__(self, master=None):
        self.master = master
        self.master.grid_columnconfigure(6, weight=1)
        self.master.resizable(width=False, height=False)
        self.width = 800
        self.height = 650
        self.master.minsize(self.width, self.height - 200)
        self.master.geometry("%dx%d" % (self.width, self.height))
        self.master.title("Pdf String Searcher")

        self.default_font = ("Arial", "12")

        self.titulo = Label(self.master, text="Pesquisar expressão em PDFs online", font=("Arial", 12, "bold"))
        self.titulo.grid(row=0, pady=25, columnspan=7)

        self.link_label = Label(self.master, text="Link", font=self.default_font)
        self.link_label.grid(row=1, sticky=W, ipadx=0.1*self.width, pady=10)

        self.link = Entry(self.master, width=50, font=self.default_font)
        self.link.grid(row=1, column=1, sticky=W)

        self.expressao_label = Label(self.master, text="Expressão", font=self.default_font)
        self.expressao_label.grid(row=2, sticky=W, ipadx=0.1*self.width)

        self.expressao = Entry(self.master, width=50, font=self.default_font)
        self.expressao.grid(row=2, column=1, sticky=W)

        self.pesquisar_button = Button(self.master, text="Pesquisar", font=self.default_font, width=14, command=self.verifica_inputs)
        self.pesquisar_button.grid(row=3, pady=15, columnspan=7)

        self.text_pad = Frame(self.master)
        self.text_area = Text(self.text_pad, height=27, width=110)

        scroll = Scrollbar(self.text_pad)
        self.text_area.tag_config('success', foreground="green")
        self.text_area.configure(yscrollcommand=scroll.set, state=DISABLED, bg="black", fg="white", font=("Arial", "10"))

        self.text_area.pack(side=LEFT)
        scroll.pack(side=RIGHT, fill=Y)
        self.text_pad.grid(row=4, columnspan=7)

        self.pdfs_links = []
        self.pdf_index = 0
        self.log = None

    def append_to_text_area(self, string, clean=False, tag=None, log=False):
        self.text_area.configure(state=NORMAL)
        if clean:
            self.text_area.delete(1.0, END)
        self.text_area.insert(END, string, tag)
        self.text_area.see(END)
        self.text_area.configure(state=DISABLED)
        if log:
            self.log.write(string)

    def verifica_inputs(self):
        self.link.configure(state=DISABLED)
        self.expressao.configure(state=DISABLED)
        input_link = self.link.get()
        input_expressao = self.expressao.get()

        if not input_link or not input_expressao:
            self.append_to_text_area("Preencha os campos obrigatórios e tente novamente.", True)
            return
        if not network.is_valid_url(input_link.strip()):
            self.append_to_text_area("Link inválido, tente novamente. (Verifique se há http:// ou https:// no início)", True)
            return
        self.append_to_text_area("", True)

        self.pesquisar_button["text"] = "Aguarde..."
        self.pesquisar_button.configure(state=DISABLED)

        timestamp = time.strftime("%Y%m%d-%H%M%S") + ".log.txt"
        self.log = open(timestamp, "w")
        self.log.write("Resultados da busca\n")
        self.log.write("Expressão: " + input_expressao + "\n")
        self.log.write("Link: " + input_link + "\n")
        self.log.write("-------------------\n\n")

        self.master.after(200, self.pesquisa_url)

    def pesquisa_url(self):
        self.pdfs_links = []
        self.pdf_index = 0
        link = self.link.get().strip()
        expression = self.expressao.get()

        response = network.get_response_from_url(link)
        if network.is_response_pdf_file(response):
            self.pdfs_links.append(link)
        else:
            self.pdfs_links = network.extract_pdfs_links(response)

        if len(self.pdfs_links) == 0:
            self.append_to_text_area("Nenhum aquivo PDF foi encontrado no link fornecido.", True)
            return

        self.append_to_text_area("Estas informações estão sendo salvas na pasta: %s\\\n\n" % os.getcwd(), True)
        self.append_to_text_area("(%d) PDFs encontrados no link fornecido.\n" % len(self.pdfs_links), log=True)
        self.append_to_text_area("Começando busca pela expressão '" + expression + "'.\n\n", log=True)
        self.master.after(100, self.verifica_pdf_list)

    def verifica_pdf_list(self):
        if self.pdf_index < len(self.pdfs_links):
            link = self.pdfs_links[self.pdf_index]
            expression = self.expressao.get()
            response = network.get_response_from_url(link)
            self.append_to_text_area("(%d/%d) Verificando '%s'.\n" % (self.pdf_index+1, len(self.pdfs_links), network.get_filename_from_url(link)), log=True)
            if network.is_response_pdf_file(response):
                f = util.binary_to_file(network.extract_content_from_response(response))
                pdf = PdfStringSearcher(f)
                has_string = pdf.contains_substring(expression)
                f.close()
                if has_string:
                    self.append_to_text_area(">>> Expressão encontrada em '" + str(network.get_url(response)) + "'\n", tag='success', log=True)
            self.pdf_index += 1
            self.master.after(100, self.verifica_pdf_list)

        else:
            self.append_to_text_area("\nBusca completa.\n", log=True)
            self.link.configure(state=NORMAL)
            self.expressao.configure(state=NORMAL)
            self.pesquisar_button.configure(state=NORMAL)
            self.pesquisar_button["text"] = "Pequisar"
            self.log.close()


if __name__ == '__main__':
    root = Tk()
    Application(root)
    root.mainloop()

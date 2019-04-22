# -*- coding: utf-8 -*-
import os
import time
import utils.network as network
import utils.util as util
import Queue
import threading
from pdf.pdfstringsearcher import PdfStringSearcher
from tkinter import messagebox
import tkinter.scrolledtext as tkst
from tkinter import *


class Application:
    def __init__(self, master=None):
        """
        This method is resposible for setting up the interface.

        :param master: Tk instance
        """
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
        self.titulo.grid(row=0, columnspan=3, pady=15, padx=20)

        self.guia_button = Button(self.master, text="Guia", font=self.default_font, command=guia)
        self.guia_button.grid(row=0, column=2, ipadx=12)

        self.link_label = Label(self.master, text="Link", font=self.default_font)
        self.link_label.grid(row=1, sticky=W, ipadx=0.1*self.width, pady=10)

        self.link_input = Entry(self.master, width=50, font=self.default_font)
        self.link_input.grid(row=1, column=1, sticky=W)

        self.expression_label = Label(self.master, text="Expressão", font=self.default_font)
        self.expression_label.grid(row=2, sticky=W, ipadx=0.1*self.width)

        self.expression_input = Entry(self.master, width=50, font=self.default_font)
        self.expression_input.grid(row=2, column=1, sticky=W)

        self.pesquisar_button = Button(self.master, text="Pesquisar", font=self.default_font, width=14, command=self.verify_inputs)
        self.pesquisar_button.grid(row=3, column=0, columnspan=2, pady=15)

        self.cancelar_button = Button(self.master, text="Parar", state=DISABLED, font=self.default_font, width=10, command=self.cancel_search)
        self.cancelar_button.grid(row=3, column=1, padx=50)

        self.text_pad = Frame(master=self.master)
        self.text_area = tkst.ScrolledText(master=self.text_pad, wrap=WORD, height=28, width=110, state=NORMAL, bg="black", fg="white", font=("Arial", "10"))
        self.text_area.tag_config('success', foreground="green")
        self.text_area.pack(ipady=5, fill=BOTH, expand=True)
        self.text_pad.grid(row=4, columnspan=7)

        self.pdfs_links = []
        self.pdf_index = 0
        self.log = None
        self.queue = None
        self.searching = False
        self.links = []
        self.expressions = []

    def append_to_text_area(self, string, clean=False, tag=None, log=False):
        """
        Quick way to write to the console.

        :param string: text to be written
        :param clean: boolean, if needs to clear the console
        :param tag: tag color, this change the color of the string
        :param log: boolean, write or not to the log file
        """
        self.text_area.configure(state=NORMAL)
        if clean:
            self.text_area.delete(1.0, END)
        self.text_area.insert(END, string, tag)
        self.text_area.see(END)
        self.text_area.configure(state=DISABLED)
        if log:
            self.log.write(string)

    def verify_inputs(self):
        """
        Verify inputs before initiating search.
        """
        self.links = list(set(map(str.strip, self.link_input.get().encode('utf-8').split(';'))))
        self.expressions = list(set(map(str.strip, self.expression_input.get().encode('utf-8').split(';'))))

        if self.links == [''] or self.expressions == ['']:
            self.append_to_text_area("Preencha os campos obrigatórios e tente novamente.", True)
            return
        for link in self.links:
            if not network.is_valid_url(link):
                self.append_to_text_area("Link inválido: " + link, True)
                self.append_to_text_area("Link inválido, tente novamente. (Verifique se há http:// ou https:// no início)")
                return
        self.append_to_text_area("", True)

        self.prepare_to_search()

    def prepare_to_search(self):
        """
        Blocks inputs, set log file and initiate url search.
        """
        self.pesquisar_button.configure(state=DISABLED)
        self.cancelar_button.configure(state=NORMAL)
        self.link_input.configure(state=DISABLED)
        self.expression_input.configure(state=DISABLED)
        self.searching = True

        timestamp = time.strftime("%Y%m%d-%H%M%S") + ".log.txt"
        self.log = open('log/' + timestamp, "w")
        self.log.write("Resultados da busca\n")
        self.log.write("Expressão/Expressões: " + ', '.join(self.expressions) + "\n")
        self.log.write("Link(s): " + ', '.join(self.links) + "\n")
        self.log.write("-------------------\n\n")

        self.master.after(200, self.search_url)

    def search_url(self):
        """
        Search for pdfs in the url and start string search.
        """
        self.pdfs_links = []
        self.pdf_index = 0

        # Return if url response error
        for link in self.links:
            try:
                response = network.get_response_from_url(link)
                # Check if url is already a pdf, if not search for all pdfs in the url.
                if network.is_response_pdf_file(response):
                    self.pdfs_links.append(link)
                else:
                    self.pdfs_links.extend(network.extract_pdfs_links(response))
            except Exception:
                self.append_to_text_area("Não foi possível pesquisar neste link: " + link + "\n", True)
                self.append_to_text_area("Tente estas instruções:\n")
                self.append_to_text_area("  - Verificar a conexão com a internet.\n")
                self.append_to_text_area("  - Tentar um novo link.\n\n")
                continue

        if len(self.pdfs_links) == 0:
            self.append_to_text_area("\nNenhum PDF encontrado.\n")
            self.end_search()
            return

        self.append_to_text_area("Estas informações serão salvas na pasta: %s\\log\\\n\n" % os.getcwd(), True)
        self.append_to_text_area("(%d) PDFs encontrados.\n" % len(self.pdfs_links), log=True)
        self.append_to_text_area("Começando busca pela expressão/expressões:\n", log=True)
        for expression in self.expressions:
            self.append_to_text_area("    " + expression + "\n", tag='success', log=True)
        self.append_to_text_area("Nos links:\n", log=True)
        for link in self.links:
            self.append_to_text_area("    " + link + "\n", tag='success', log=True)
        self.append_to_text_area("\n", log=True)

        self.queue = Queue.Queue()
        PdfStringSearcherTask(self.queue, self.pdf_index, self.pdfs_links, self.expressions).start()

        self.master.after(100, self.process_queue)

    def process_queue(self):
        """
        The current search thread task is checked each time this method is called. This method is important for
        not freezing GUI. A search thread task is a running function looking for string in a pdf.
        """
        try:
            if not self.searching:
                self.end_search()
            else:
                task_result = self.queue.get(0)
                if task_result != 'end_of_list':
                    link = network.get_filename_from_url(self.pdfs_links[self.pdf_index])
                    self.append_to_text_area("(%d/%d) Verificando '%s'.\n" % (self.pdf_index + 1, len(self.pdfs_links), link), log=True)
                    if task_result[0]:
                        self.append_to_text_area(">>> '" + ', '.join(task_result[0]) + "' encontrado em '" + str(task_result[1]) + "'\n", tag='success', log=True)
                    self.pdf_index += 1

                    PdfStringSearcherTask(self.queue, self.pdf_index, self.pdfs_links, self.expressions).start()
                    self.master.after(100, self.process_queue)
                else:
                    self.end_search()
        except Queue.Empty:
            self.master.after(100, self.process_queue)

    def end_search(self):
        """
        Reopen inputs and close log file.
        """
        self.searching = False
        self.append_to_text_area("\nBusca completa.\n", log=True)
        self.link_input.configure(state=NORMAL)
        self.expression_input.configure(state=NORMAL)
        self.pesquisar_button.configure(state=NORMAL)
        self.cancelar_button.configure(state=DISABLED)
        self.log.close()

    def cancel_search(self):
        """
        Force search to stop
        """
        self.append_to_text_area("\nParada forçada.\n", log=True)
        self.searching = False


class PdfStringSearcherTask(threading.Thread):
    """
    This class takes care of pdf string search, it runs in a separated thread so it doesn't freeze the GUI.
    """
    def __init__(self, queue, pdf_index, pdfs_links, expressions):
        threading.Thread.__init__(self)
        self.queue = queue
        self.pdf_index = pdf_index
        self.pdfs_links = pdfs_links
        self.expressions = expressions
        self.strings_found = []
        self.pdf_url = ""

    def run(self):
        if self.pdf_index < len(self.pdfs_links):
            # This algorithm is explained in src/example.py
            link = self.pdfs_links[self.pdf_index]
            response = network.get_response_from_url(link)
            if network.is_response_pdf_file(response):
                f = util.binary_to_file(network.extract_content_from_response(response))
                pdf = PdfStringSearcher(f)
                self.strings_found = pdf.search_substrings(self.expressions)
                if self.strings_found:
                    self.pdf_url = str(network.get_url(response))
                f.close()
            self.queue.put([self.strings_found, self.pdf_url])
        else:
            self.queue.put("end_of_list")


def guia():
    """
    Guide message
    """
    message = "Este simples programa verifica se há arquivos PDF no link fornecido, se sim, procura por uma " +\
              "expressão fornecida e avisa se o(s) PDF(s) contém a expressão (Internet é necessária)\n\n" + \
              "Campo Link: link de um PDF ou de uma página que contenha links de PDFs. ex: http://www.google.com.br\n\n" +\
              "Campo Expressão: Expressão a ser buscada, letras maiúsculas não diferem das minúsculas (EXPRESSÃO" + \
              " = ExPrEsSãO)\n\nAmbos os campos aceitam mais de um argumento, basta separa-los por ';'. ex: Pedro; Hugo; Vitor." + \
              "\n\nAs informações são salvas dentro da pasta log.\n\n" + \
              "Código fonte do projeto:\n    https://github.com/mvsantos013/pdf-string-searcher"
    messagebox.showinfo("Guia de uso", message)


if __name__ == '__main__':
    if not os.path.exists('log'):
        os.makedirs('log')
    root = Tk()
    Application(root)
    root.mainloop()

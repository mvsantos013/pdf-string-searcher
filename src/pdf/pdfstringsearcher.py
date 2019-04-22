# -*- coding: utf-8 -*-
from StringIO import StringIO
from pdfminer.pdfparser import PDFParser, PDFDocument
from pdfminer.pdfinterp import PDFResourceManager
from pdfminer.converter import TextConverter
from pdfpageinterpreter import PDFPageInterpreter
import re


class PdfStringSearcher(list):
    """
    This class is responsable for handling the pdf file and search for the string

    :param pdf_file: instance of pdf file
    :return: nothing
    """
    def __init__(self, pdf_file, password=''):
        self.parser = PDFParser(pdf_file)
        self.doc = PDFDocument()
        self.parser.set_document(self.doc)
        self.doc.set_parser(self.parser)
        self.doc.initialize(password)
        if self.doc.is_extractable:
            self.resmgr = PDFResourceManager()
            self.device = TextConverter(self.resmgr, outfp=StringIO())
            self.interpreter = PDFPageInterpreter(self.resmgr, self.device)

    def search_substrings(self, list_substrings):
        """
        Search for the string in each page, if it contains the string

        :param list_substrings: list of strings to be searched
        :return: list of expressions found
        """
        found = []
        for page in self.doc.get_pages():
            if found == list_substrings:
                break
            page_text = self.interpreter.process_page(page)
            for string in list_substrings:
                has_string = re.search(string, page_text, re.IGNORECASE)
                if has_string and string not in found:
                    found.append(string)
        self._cleanup()
        return found

    def _cleanup(self):
        del self.device
        del self.doc
        del self.parser
        del self.resmgr
        del self.interpreter

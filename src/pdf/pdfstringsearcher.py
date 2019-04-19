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

    def contains_substring(self, search_string):
        """
        Search for the string in each page, if it contains the string

        :param search_string: Substring to be searched
        :return: Boolean, True if contains, False if not
        """
        for page in self.doc.get_pages():
            page_text = self.interpreter.process_page(page)
            has_string = re.search(search_string, page_text, re.IGNORECASE)
            if has_string:
                self._cleanup()
                return True
        self._cleanup()
        return False

    def _cleanup(self):
        del self.device
        del self.doc
        del self.parser
        del self.resmgr
        del self.interpreter

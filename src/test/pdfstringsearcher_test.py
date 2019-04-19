# -*- coding: utf-8 -*-
import os
import sys
import unittest
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from pdf.pdfstringsearcher import PdfStringSearcher


class TestPdfStringSearcher(unittest.TestCase):

    def test_class(self):
        f = open("test.pdf", "rb")
        doc = PdfStringSearcher(f)
        self.assertTrue(doc.contains_substring("professor"))
        f.close()


if __name__ == '__main__':
    unittest.main()

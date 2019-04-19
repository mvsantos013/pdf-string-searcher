# -*- coding: utf-8 -*-
import os
import sys
import unittest
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from pdf.pdfstringsearcher import PdfStringSearcher
import utils.util as util
import utils.network as network


class TestPdfStringSearcher(unittest.TestCase):

    def test_class(self):
        """
        Tests if pdf parser is working as expected
        """
        pdf_url = "http://www.africau.edu/images/default/sample.pdf"
        response = network.get_response_from_url(pdf_url)
        f = util.binary_to_file(network.extract_content_from_response(response))
        doc = PdfStringSearcher(f)
        self.assertTrue(doc.contains_substring("Boring"))
        f.close()


if __name__ == '__main__':
    unittest.main()

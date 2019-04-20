# -*- coding: utf-8 -*-
import utils.network as network
import utils.util as util
from pdf.pdfstringsearcher import PdfStringSearcher


if __name__ == '__main__':
    # Defines url
    # It can be a pdf link or a link containing several links to pdfs
    url = "http://www.africau.edu/images/default/sample.pdf"

    # Expression to be searched
    expression = "Boring"

    # Get response from url
    response = network.get_response_from_url(url)

    # Verifies if response is a pdf file, if not, tries to extract all pdfs links from response content
    if network.is_response_pdf_file(response):
        # Parses the pdf file from web
        # It can be a local file: f = open('sample.pdf', 'rb')
        f = util.binary_to_file(network.extract_content_from_response(response))
        pdf = PdfStringSearcher(f)
        # Search for expression in pdf, this might take some time
        has_string = pdf.contains_substring(expression)
        # closes file after search
        f.close()

        if has_string:
            print ("Expression '" + expression + "' found at: " + network.get_url(response))
        else:
            print "Expression not found"
    else:
        # Get all pdf links from response content
        pdfs_links = network.extract_pdfs_links(response)
        print ("List of pdfs found:\n" + '\n'.join(pdfs_links))

        # Repeat the if above for each pdf
        for pdf_link in pdfs_links:
            print ("Searching '" + network.get_filename_from_url(pdf_link) + "'")
            response = network.get_response_from_url(pdf_link)
            if network.is_response_pdf_file(response):
                f = util.binary_to_file(network.extract_content_from_response(response))
                pdf = PdfStringSearcher(f)
                has_string = pdf.contains_substring(expression)
                f.close()
                if has_string:
                    print ("Expression '" + expression + "' found at: " + network.get_url(response))

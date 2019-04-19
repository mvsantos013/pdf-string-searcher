# -*- coding: utf-8 -*-
import re
from urllib2 import Request, urlopen
from BeautifulSoup import BeautifulSoup

regex_url = re.compile(
        r'^(?:http|ftp)s?://'
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|'
        r'localhost|'
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'
        r'(?::\d+)?'
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)


def is_valid_url(url):
    """
    Checks if url is valid

    :param url: string that represents url
    :return: Boolean, True if valid url
    """
    return re.match(regex_url, url) is not None


def get_response_from_url(url):
    """
    Get content from webpage

    :param url: string that represents url
    :return: Object response
    """
    return urlopen(Request(url))


def get_header_content_type(response):
    """
    Checks the Content-Type header from the response

    :param response: urlopen result as response
    :return: string Content-Type
    """
    return response.info()['Content-Type']


def get_url(response):
    """
    Get url from response

    :param response: urlopen result as response
    :return: string Content-Type
    """
    return response.geturl()


def is_response_pdf_file(response):
    """
    Checks if the Content-Type header from the response is pdf

    :param response: urlopen result as response
    :return: Boolean, True if response is a pdf file
    """
    if get_header_content_type(response) == 'application/pdf':
        return True
    return False


def extract_content_from_response(response):
    """
    Extract content from webpage

    :param response: urlopen result as response
    :return: String content
    """
    return response.read()


def extract_pdfs_links(response):
    """
    Extract all pdf links in webpage

    :param response: urlopen result as response
    :return: List of pdf links
    """
    link = get_url(response)
    base_link = link[: link.find('/', 8)]
    soup = BeautifulSoup(response)
    pdfs_links = []

    for a in soup.findAll('a'):
        href = a.get('href')
        if href and '.pdf' in href:
            if 'http' in href:
                pdfs_links.append(href)
            else:
                pdfs_links.append(base_link + href)
    return pdfs_links

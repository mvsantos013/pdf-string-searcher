# -*- coding: utf-8 -*-
import re
from urllib2 import Request, urlopen

regex_url = re.compile(
        r'^(?:http|ftp)s?://'
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|'
        r'localhost|'
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'
        r'(?::\d+)?'
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)


def is_valid_url(url):
    return re.match(regex_url, url) is not None


def get_content_from_url(url):
    try:
        content = urlopen(Request(pdf_url))
        return content
    except Exception:
        return None

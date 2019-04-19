# -*- coding: utf-8 -*-
import re

regex_url = re.compile(
        r'^(?:http|ftp)s?://'
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|'
        r'localhost|'
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'
        r'(?::\d+)?'
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)


def trim_whitespace(s):
    """
    Returns a string that has at most one whitespace
    character between non-whitespace characters.

    >>> trim_whitespace(' hi   there')
    'hi there'
    """
    bf = ''
    for i, letter in enumerate(s):
        if letter.isspace():
            try:
                if s[i + 1].isspace():
                    continue
            except IndexError:
                pass
        bf = bf + letter

    return bf.strip()


def is_valid_url(url):
    return re.match(regex_url, url) is not None


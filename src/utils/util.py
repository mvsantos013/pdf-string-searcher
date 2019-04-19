# -*- coding: utf-8 -*-
from io import BytesIO

def trim_whitespace(string):
    """
    Returns a string that has at most one whitespace
    character between non-whitespace characters.

    :param string: string to be cleaned
    :return: string cleaned

    >>> trim_whitespace(' hi   there')
    'hi there'
    """
    bf = ''
    for i, letter in enumerate(string):
        if letter.isspace():
            try:
                if string[i + 1].isspace():
                    continue
            except IndexError:
                pass
        bf = bf + letter

    return bf.strip()


def binary_to_file(data):
    """
    Parses binary data to file

    :param data:
    :return: file
    """
    return BytesIO(data)

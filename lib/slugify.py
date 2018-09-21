#!/usr/bin/env python
# -*- coding: utf-8 -*-
# The line above is to signify that the script contains utf-8 encoded characters.

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# Adapted from https://github.com/un33k/python-slugify/blob/master/slugify/slugify.py

# This file contains common utility functions to slugify strings

__author__ = 'John Wieczorek'
__contributors__ = "Val Neekman, John Wieczorek"
__copyright__ = "Copyright 2016 vertnet.org"
__version__ = "slugify.py 2016-07-26T14:03-03:00"

import re
import unicodedata
import types
import sys

try:
    from htmlentitydefs import name2codepoint
    _unicode = unicode
    _unicode_type = types.UnicodeType
except ImportError:
    from html.entities import name2codepoint
    _unicode = str
    _unicode_type = str
    unichr = chr

# need to install unidecode for this to be used
# pip install unidecode
# jython pip install unidecode for use in workflows

import unidecode

__all__ = ['slugify']

CHAR_ENTITY_PATTERN = re.compile('&(%s);' % '|'.join(name2codepoint))
DECIMAL_PATTERN = re.compile('&#(\d+);')
HEX_PATTERN = re.compile('&#x([\da-fA-F]+);')
QUOTE_PATTERN = re.compile(r'[\']+')
ALLOWED_CHARS_PATTERN = re.compile(r'[^-a-z0-9]+')
DUPLICATE_DASH_PATTERN = re.compile('-{2,}')
NUMBERS_PATTERN = re.compile('(?<=\d),(?=\d)')

def smart_truncate(string, max_length=0, word_boundaries=False, separator=' ', save_order=False):
    """
    Truncate a string.
    :param string (str): string for modification
    :param max_length (int): output string length
    :param word_boundaries (bool):
    :param save_order (bool): if True then word order of output string is like input string
    :param separator (str): separator between words
    :return:
    """

    string = string.strip(separator)

    if not max_length:
        return string

    if len(string) < max_length:
        return string

    if not word_boundaries:
        return string[:max_length].strip(separator)

    if separator not in string:
        return string[:max_length]

    truncated = ''
    for word in string.split(separator):
        if word:
            next_len = len(truncated) + len(word)
            if next_len < max_length:
                truncated += '{0}{1}'.format(word, separator)
            elif next_len == max_length:
                truncated += '{0}'.format(word)
                break
            else:
                if save_order:
                    break
    if not truncated:
        truncated = string[:max_length]
    return truncated.strip(separator)

def slugify(text, entities=True, decimal=True, hexadecimal=True, max_length=0, word_boundary=False,
            separator='-', save_order=False, stopwords=()):
    """
    Make a slug from the given text.
    :param text (str): initial text
    :param entities (bool):
    :param decimal (bool):
    :param hexadecimal (bool):
    :param max_length (int): output string length
    :param word_boundary (bool):
    :param save_order (bool): if parameter is True and max_length > 0 return whole words in the initial order
    :param separator (str): separator between words
    :param stopwords (iterable): words to discount
    :return (str):
    """

    # ensure text is unicode
    if not isinstance(text, _unicode_type):
        text = _unicode(text, 'utf-8', 'ignore')

    # replace quotes with dashes - pre-process
    text = QUOTE_PATTERN.sub('-', text)

    # decode unicode
    text = unidecode.unidecode(text)

    # ensure text is still in unicode
    if not isinstance(text, _unicode_type):
        text = _unicode(text, 'utf-8', 'ignore')

    # character entity reference
    if entities:
        text = CHAR_ENTITY_PATTERN.sub(lambda m: unichr(name2codepoint[m.group(1)]), text)

    # decimal character reference
    if decimal:
        try:
            text = DECIMAL_PATTERN.sub(lambda m: unichr(int(m.group(1))), text)
        except:
            pass

    # hexadecimal character reference
    if hexadecimal:
        try:
            text = HEX_PATTERN.sub(lambda m: unichr(int(m.group(1), 16)), text)
        except:
            pass

    # translate
    text = unicodedata.normalize('NFKD', text)
    if sys.version_info < (3,):
        text = text.encode('ascii', 'ignore')

    # make the text lowercase
    text = text.lower()

    # remove generated quotes -- post-process
    text = QUOTE_PATTERN.sub('', text)

    # replace unwanted characters
    text = NUMBERS_PATTERN.sub('', text)
    text = ALLOWED_CHARS_PATTERN.sub('-', text)

    # remove redundant -
    text = DUPLICATE_DASH_PATTERN.sub('-', text).strip('-')

    # remove stopwords
    if stopwords:
        stopwords_lower = [s.lower() for s in stopwords]
        words = [w for w in text.split('-') if w not in stopwords_lower]
        text = '-'.join(words)

    # smart truncate if requested
    if max_length > 0:
        text = smart_truncate(text, max_length, word_boundary, '-', save_order)

    if separator != '-':
        text = text.replace('-', separator)

    return text

def main():
    if len(sys.argv) < 2:
        print("Usage %s TEXT TO SLUGIFY" % sys.argv[0])
    else:
        text = ' '.join(sys.argv[1:])
        print(slugify(text))
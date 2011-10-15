# -*- coding: utf-8 -*-

"""
parser = wiki_converter.parser.create_parser('pukiwiki')
converter = wiki_converter.parser.ConfluecenConverter()
parser.parse(file, converter)
text = converter.converted_text()
"""

import re


class BaseParser(object):
    def __init__(self):
        pass

    def parse_text(self, text, handler):
        pass

    def set_handler(self, handler):
        self.handler = handler

class PukiwikiParser(BaseParser):

    def __init__(self):
        self.regex = re.compile(r'^\*{1,[\w]*')
        super(PukiwikiParser, self).__init__()
        
    def parse_text(self, text, handler):
        self.set_handler(handler)
        for line in text.split('\n'):
            self.parse_line(line.rstrip(), handler)

    def parse_line(self, line, handler):
        char1, char2, char3 = line[0:1], line[0:2], line[0:3]

        is_heading = False
        text = None
        level = 1
        if char1 == '*':
            is_heading, text, level = True, line[1:], 1
        elif char2 == '**':
            is_heading, text, level = True, line[2:], 2
        elif char3 == '***':
            is_heading, text, level = True, line[2:], 2
        if is_heading:
            handler.start_heading(text, level)
            handler.end_heading(text, level)


type2parser = {
    'pukiwiki': PukiwikiParser,
}

def create_parser(wiki_type):
    ParserClass = type2parser[wiki_type]
    if ParserClass is None:
        raise ValueError("Unknown wiki_type:" + wiki_type)
    return ParserClass()


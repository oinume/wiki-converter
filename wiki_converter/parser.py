# -*- coding: utf-8 -*-

"""
parser = wiki_converter.parser.create_parser('pukiwiki')
converter = wiki_converter.parser.ConfluecenConverter()
parser.parse(file, converter)
text = converter.converted_text()
"""

import re

class BaseParser(object):
    def __init__(self, patterns):
        self.__handler = None
        for pattern in patterns:
            pattern['regexp'] = re.compile(pattern['pattern'])
        self.__patterns = patterns

    def parse_text(self, text, handler):
        pass

    def get_handler(self):
        return self.__handler

    def set_handler(self, handler):
        self.__handler = handler

    @property
    def patterns(self):
        return self.__patterns

    handler = property(get_handler, set_handler)

class PukiwikiParser(BaseParser):
    def __init__(self):
        patterns = [
            { 'pattern': r'^(\*+)(.*)', 'callback': self.heading },
            { 'pattern': r"'''(.*)'''(.*)", 'callback': self.italic },
            { 'pattern': r"''(.*)''(.*)", 'callback':  self.strong },
        ]
        super(PukiwikiParser, self).__init__(patterns)
        
    def parse_text(self, text, handler):
        self.handler = handler
        for line in text.split('\n'):
            self.parse_line(line.rstrip(), handler)

    def parse_line(self, line, handler):
        text = line
        while len(text) != 0:
            matched = None
            for pattern in self.patterns:
                pattern, regexp, callback = pattern['pattern'], pattern['regexp'], pattern['callback']
                if regexp is None:
                    print "[warn] regexp is None"
                    continue
                if callback is None:
                    print "[warn] callback is None"
                    continue

                matched = regexp.match(text)
                if matched:
                    # TODO: logger
                    print "[debug] `%s` matched for `%s`" % (pattern, text)
                    groups = matched.groups()
                    text = callback(groups)
                    break

            if matched is None:
                text = self.normal_text(text)

    def normal_text(self, text):
        self.handler.at_normal_text(text)
        return ''

    def heading(self, groups):
        self.handler.at_heading(groups[1], len(groups[0]))
        return ''

    def italic(self, groups):
        self.handler.at_italic(groups[0])
        return groups[1]

    def strong(self, groups):
        self.handler.at_strong(groups[0])
        return groups[1]

type2parser = {
    'pukiwiki': PukiwikiParser,
}

def create_parser(wiki_type):
    ParserClass = type2parser[wiki_type]
    if ParserClass is None:
        raise ValueError("Unknown wiki_type:" + wiki_type)
    return ParserClass()

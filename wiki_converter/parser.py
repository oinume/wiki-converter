# -*- coding: utf-8 -*-

"""
parser = wiki_converter.parser.create_parser('pukiwiki')
converter = wiki_converter.parser.ConfluecenConverter()
parser.parse(file, converter)
text = converter.converted_text()
"""

# blocks
#  heading
#  list
#  table
#
# text effects
#  italic
#  strong
#  strike_through
#  link

import re
from wiki_converter.common import ParseError
from wiki_converter.log import create_logger
from wiki_converter.handler import LIST_TYPE_BULLET, LIST_TYPE_NUMBERED

class BaseParser(object):
    def __init__(self, patterns, log):
        self.__log = log
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
    def log(self):
        return self.__log

    @property
    def patterns(self):
        return self.__patterns

    handler = property(get_handler, set_handler)

class PukiwikiParser(BaseParser):
    def __init__(self, log=create_logger()):
        patterns = [
            ##############
            # blocks
            ##############
            { 'pattern': r'^(\*+)(.*)', 'callback': self.heading },
            { 'pattern': r'^([\-\+]+)(.*)', 'callback': self.list },
            { 'pattern': r'^#contents', 'callback': self.toc },
            { 'pattern': r"^\|(.*)\|h$", 'callback': self.table_header_columns },
            { 'pattern': r"^\|(.*)\|$", 'callback': self.table_columns },

            ##############
            # text effects
            ##############
            { 'pattern': r"'''(.*)'''(.*)", 'callback': self.italic },
            { 'pattern': r"''(.*)''(.*)", 'callback':  self.strong },
            { 'pattern': r"%%(.*)%%(.*)", 'callback':  self.strike_through },
            { 'pattern': r"\[\[(.*)\]\](.*)", 'callback': self.link },

            # no underline
            
        ]
        super(PukiwikiParser, self).__init__(patterns, log)

    def normal_text(self, text):
        self.handler.at_normal_text(text)
        return ''

    def heading(self, groups):
        self.handler.at_heading(groups[1], len(groups[0]))
        return ''

    def toc(self, groups):
        self.handler.at_toc()
        return ''

    def list(self, groups):
        types = []
        for char in groups[0]:
            if char == '-':
                types.append(LIST_TYPE_BULLET)
            elif char == '+':
                types.append(LIST_TYPE_NUMBERED)
            else:
                raise ParseError("Invalid list character: '%s'" % char)

        self.handler.at_list(groups[1], types)
        return ''

    def table_columns(self, groups):
        line = groups[0]
        self.log.debug("line = `%s`" % (line))
        self.handler.at_table_columns(line.split('|'))
        return ''

    def table_header_columns(self, groups):
        line = groups[0]
        self.log.debug("line = `%s`" % (line))
        self.handler.at_table_header_columns(line.split('|'))
        return ''

    def italic(self, groups):
        self.handler.at_italic(groups[0])
        return groups[1]

    def strong(self, groups):
        self.handler.at_strong(groups[0])
        return groups[1]

    def strike_through(self, groups):
        self.handler.at_strike_through(groups[0])
        return groups[1]

    def link(self, groups):
        self.log.debug("link = `%s`" % (groups[0]))
        link = groups[0]
        array = re.split('[\|:>]?', link)
        text = array[0]
        url = ''.join(array[1:])
        self.log.debug("text = `%s`, url = `%s`" % (text, url))
        self.handler.at_link(text, url)
        return groups[1]

    def parse_text(self, text, handler):
        self.handler = handler
        for line in text.split('\n'):
            self.parse_line(line.rstrip(), handler)

    def parse_line(self, line, handler):
        # textにパースする文字列を入れる。これが空になるまでループする
        text = line
        while len(text) != 0:
            matched = None

            for pattern in self.patterns:
                pattern, regexp, callback = pattern['pattern'], pattern['regexp'], pattern['callback']
                if regexp is None:
                    self.log.error("regexp is None for `%s`" % pattern)
                    continue
                if callback is None:
                    self.log.error("callback is None for `%s`" % pattern)
                    continue

                matched = regexp.match(text)
                if matched:
                    self.log.debug("`%s` matched for `%s`" % (pattern, text))
                    groups = matched.groups()
                    text = callback(groups)
                    break

            if matched is None:
                self.log.debug("normal text = `%s`" % (text))
                text = self.normal_text(text)



type2parser = {
    'pukiwiki': PukiwikiParser,
}

def create_parser(wiki_type):
    ParserClass = type2parser[wiki_type]
    if ParserClass is None:
        raise ValueError("Unknown wiki_type:" + wiki_type)
    return ParserClass()

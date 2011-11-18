# -*- coding: utf-8 -*-

from wiki_converter.handler import (
    DefaultHandler,
    LIST_TYPE_NUMBERED,
    LIST_TYPE_BULLET
)
from wiki_converter.log import create_logger

class ConfluecenConverter(DefaultHandler):
    def __init__(self, log=create_logger()):
        self.__log = log
        self.__converted_text = ''
        self.__current_converted_text = ''

    @property
    def log(self):
        return self.__log

    def at_normal_text(self, text):
        self.log.debug("at_normal_text = `%s`" % (text))
        return text
    
    def at_heading(self, text, level):
        heading = "h1."
        if level == 1:
            heading = "h2."
        elif level == 2:
            heading = "h3."
        elif level == 3:
            heading = "h4."
        elif level == 4:
            heading = "h5."
        elif level == 5:
            heading = "h6."
        return heading + text

    def at_toc(self):
        return u'{toc}'

    def at_list(self, types):
        self.log.debug("types = `%s`", str(types))
        s = ''
        for i, type in enumerate(types):
            if type == LIST_TYPE_BULLET:
                s += '*'
            elif type == LIST_TYPE_NUMBERED:
                s += '#'
        return s

    def at_table_columns(self, columns):
        self.log.debug("columns = %s" % (str(columns)))
        return '|' + '|'.join(columns) + '|'

    def at_table_header_columns(self, columns):
        self.log.debug("columns = %s" % (str(columns)))
        return '||' + '||'.join(columns) + '||'

    def at_formatted_lines(self, lines):
        self.log.debug("lines = `%s`" % (lines))
        return '{code}\n' + lines + '{code}\n'

    def at_strong(self, text):
        return '*' + text + '*'

    def at_italic(self, text):
        return '_' + text + '_'

    def at_strike_through(self, text):
        return '-' + text + '-'

    def at_underlines(self, text):
        return '+' + text + '+'

    def at_superscript(self, text):
        return '^' + text + '^'

    def at_subscript(self, text):
        return '~' + text + '~'

    def at_monospaced(self, text):
        pass
    def at_block_quote(self, text):
        pass

    def at_line_break(self):
        pass

    def at_link(self, text, url):
        if url:
            return '[%s|%s]' % (text, url)
        else:
            return '[%s]' % (text)

    def at_new_line(self):
        return '\n'

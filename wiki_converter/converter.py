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

    def get_converted_text(self):
        return self.__converted_text

    def set_converted_text(self, text):
        self.__converted_text = text

    def get_current_converted_text(self):
        return self.__current_converted_text

    def set_current_converted_text(self, text):
        self.__current_converted_text = text

    converted_text = property(get_converted_text, set_converted_text)
    current_converted_text = property(get_current_converted_text, set_current_converted_text)

    def append_text(self, text):
        self.current_converted_text = text
        self.converted_text += text

    def append_text_with_line(self, text):
        self.current_converted_text = text + '\n'
        self.converted_text += text + '\n'

    def append_line(self):
        self.current_converted_text += '\n'
        self.converted_text += '\n'

    def reset_converted_text(self):
        self.current_converted_text = ''
        self.converted_text = ''
    
    def at_normal_text(self, text):
        self.log.debug("at_normal_text = `%s`" % (text))
        self.append_text(text)
    
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
        self.append_text_with_line(heading + text)

    def at_toc(self):
        self.append_text_with_line('{toc}')

    def at_list(self, text, types):
        self.log.debug("text = `%s`, types = `%s`", text, str(types))
        for i, type in enumerate(types):
            if type == LIST_TYPE_BULLET:
                self.append_text('*')
            elif type == LIST_TYPE_NUMBERED:
                self.append_text('#')
            
            if i == len(types) - 1:
                self.append_text_with_line(text)

    def at_table_columns(self, columns):
        self.log.debug("columns = %s" % (str(columns)))
        self.append_text_with_line('|' + '|'.join(columns) + '|')

    def at_table_header_columns(self, columns):
        self.log.debug("columns = %s" % (str(columns)))
        self.append_text_with_line('||' + '||'.join(columns) + '||')

    def at_formatted_lines(self, lines):
        self.log.debug("lines = `%s`" % (lines))
        self.append_text_with_line('{code}')
        self.append_text(lines)
        self.append_text_with_line('{code}')

    def at_strong(self, text):
        self.append_text('*' + text + '*')

    def at_italic(self, text):
        self.append_text('_' + text + '_')

    def at_strike_through(self, text):
        self.append_text('-' + text + '-')

    def at_underlines(self, text):
        self.append_text('+' + text + '+')

    def at_superscript(self, text):
        self.append_text('^' + text + '^')

    def at_subscript(self, text):
        self.append_text('~' + text + '~')

    def at_monospaced(self, text):
        pass
    def at_block_quote(self, text):
        pass

    def at_line_break(self):
        pass

    def at_link(self, text, url):
        if url:
            self.append_text('[%s|%s]' % (text, url))
        else:
            self.append_text('[%s]' % (text))


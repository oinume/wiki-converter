# -*- coding: utf-8 -*-

from wiki_converter.handler import DefaultHandler

class ConfluecenConverter(DefaultHandler):
    def __init__(self):
        self.__converted_text = ''
        self.__current_converted_text = ''

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
        print "at_normal_text:" + text
        self.append_text(text)
    
    def at_heading(self, text, level):
        heading = "h1."
        if level == 1:
            heading = "h1."
        elif level == 2:
            heading = "h2."
        elif level == 3:
            heading = "h3."
        elif level == 4:
            heading = "h4."
        elif level == 5:
            heading = "h5."
        self.append_text_with_line(heading + text)

    def at_strong(self, text):
        print "at_strong:" + text
        self.append_text('*' + text + '*')

    def at_italic(self, text):
        self.append_text('_' + text + '_')

    def at_strike_through(self, text):
        self.append('-' + text + '-')

    def at_underlines(self, text):
        self.append('+' + text + '+')

    def at_superscript(self, text):
        self.append('^' + text + '^')

    def at_subscript(self, text):
        self.append('~' + text + '~')

    def at_monospaced(self, text):
        pass
    def at_block_quote(self, text):
        pass

    def at_line_break(self):
        pass

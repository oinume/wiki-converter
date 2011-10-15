# -*- coding: utf-8 -*-

from wiki_converter.handler import DefaultHandler

class ConfluecenConverter(DefaultHandler):
    def __init__(self):
        self.converted_text = ''
        self.current_converted_text = ''

    def get_converted_text(self):
        return self.converted_text

    def get_current_converted_text(self):
        return self.current_converted_text

    def append_converted_text(self, text):
        self.current_converted_text = text
        self.converted_text += '\n' + text

    def end_heading(self, text, level):
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
        self.append_converted_text(heading + text)


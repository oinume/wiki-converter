# -*- coding: utf-8 -*-

LIST_TYPE_BULLET = 1
LIST_TYPE_NUMBERED = 2

class DefaultHandler(object):
    def __init__():
        pass
    def start_document(self):
        pass
    def end_document(self):
        pass

    def at_comment(self, text):
        pass

    #
    # heading
    #
    def at_heading(self, text, level):
        pass

    #
    # text effects
    #
    def at_strong(self, text):
        pass
    def at_italic(self, text):
        pass
    def at_strike_through(self, text):
        pass
    def at_underlines(self, text):
        pass
    def at_superscript(self, text):
        pass
    def at_subscript(self, text):
        pass
    def at_monospaced(self, text):
        pass
    def at_block_quote(self, text):
        pass

    def at_line_break(self):
        pass


    #
    # lists
    #
    def at_list(self, text, types):
        pass
    
    #
    # tables
    #
    def start_table(self):
        pass
    def end_table(self):
        pass
    def at_table_header(self, columns):
        pass
    def at_table_row(self, columns):
        pass
    def at_table_footer(self, columns):
        pass

    #
    # other block elements
    #
    def at_toc(self):
        pass

#    def start_element():
#        pass
#    
#    def end_element():
#        pass
#
#    def characters(text):
#        pass

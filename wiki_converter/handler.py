# -*- coding: utf-8 -*-

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
    def at_bullet_list(self, text, level):
        pass
    def end_bullet_list(self, text, level):
        pass
    def at_numbered_list(self, text, level):
        pass
    def end_numbered_list(self, text, level):
        pass
    def at_mixed_list(self, text, level, *args):
        # TODO: どうやって情報を渡す？
        pass
    def end_mixed_list(self, text, level, *args):
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

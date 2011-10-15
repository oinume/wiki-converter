# -*- coding: utf-8 -*-

class DefaultHandler(object):
    def __init__():
        pass
    def start_document(self):
        pass
    def end_document(self):
        pass
    def start_comment(self, text):
        pass
    def end_comment(self, text):
        pass

    #
    # heading
    #
    def start_heading(self, text, level):
        pass
    def end_heading(self, text, level):
        pass

    #
    # text effects
    #
    def start_strong(self, text):
        pass
    def end_strong(self, text):
        pass
    def start_italic(self, text):
        pass
    def end_italic(self, text):
        pass
    def start_strike_through(self, text):
        pass
    def end_strike_through(self, text):
        pass
    def start_underlines(self, text):
        pass
    def end_underlines(self, text):
        pass
    def start_superscript(self, text):
        pass
    def end_superscript(self, text):
        pass
    def start_subscript(self, text):
        pass
    def end_subscript(self, text):
        pass
    def start_monospaced(self, text):
        pass
    def end_monospaced(self, text):
        pass
    def start_block_quote(self, text):
        pass
    def end_block_quote(self, text):
        pass

    def start_line_break(self):
        pass
    def end_line_break(self):
        pass

    #
    # lists
    #
    def start_bullet_list(self, text, level):
        pass
    def end_bullet_list(self, text, level):
        pass
    def start_numbered_list(self, text, level):
        pass
    def end_numbered_list(self, text, level):
        pass
    def start_mixed_list(self, text, level, *args):
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
    def start_table_header(self, columns):
        pass
    def end_table_header(self, columns):
        pass
    def start_table_row(self, columns):
        pass
    def end_table_row(self, columns):
        pass
    def start_table_footer(self, columns):
        pass
    def end_table_footer(self, columns):
        pass

    #
    # other block elements
    #
    def start_toc(self):
        pass
    def end_toc(self):
        pass

#    def start_element():
#        pass
#    
#    def end_element():
#        pass
#
#    def characters(text):
#        pass

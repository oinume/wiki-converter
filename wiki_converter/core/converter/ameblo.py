# -*- coding: utf-8 -*-

from ..converter import (
    BaseConverter,
    ConvertError,
)

class AmebloConverter(BaseConverter):
    def __init__(self, options={}, log=None):
        super(AmebloConverter, self).__init__(options, log)

    def at_heading(self, text, level):
        l = level + 3 # アメブロは<h4>から始める必要がある
        return "<h%d>%s</h%d>" % (l, text.strip(), l)

    def at_toc(self):
        return ''

    def at_list(self, types):
        self.log.debug("list = %s" % (str(types)))
        pass

    def at_table_columns(self, columns):
        # TODO: 実装
        self.log.debug("columns = %s" % (str(columns)))
        return '|' + '|'.join(columns) + '|'

    def at_table_header_columns(self, columns):
        # TODO: 実装
        self.log.debug("columns = %s" % (str(columns)))
        return '||' + '||'.join(columns) + '||'

    def at_formatted_lines(self, lines):
        # TODO: rename to at_formatted_text
        self.log.debug("lines = `%s`" % (lines))
        return '<pre>' + lines + '</pre>\n'

    def at_strong(self, text):
        return '<strong>' + text + '</strong>'

    def at_italic(self, text):
        return '<i>' + text + '</i>'

    def at_strike_through(self, text):
        return '<s>' + text + '</s>'

    def at_underlines(self, text):
        return '<u>' + text + '</u>'

    def at_superscript(self, text):
        return '<sup>' + text + '</sup>'

    def at_subscript(self, text):
        return '<sub>' + text + '</sub>'

    def at_monospaced(self, text):
        pass

    def at_block_quote(self, text):
        pass

    def at_line_break(self):
        pass

    def at_link(self, text, url):
        if not url:
            raise ConvertError("url is required in at_link()")
        return '<a href="%s">%s</a>' % (url, text)

    def at_new_line(self):
        # アメブロは改行入れると<br>に置換されてしまうのであえて改行しない
        return ''
#        return '\n'

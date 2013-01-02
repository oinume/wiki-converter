# -*- coding: utf-8 -*-

from ..converter import (
    BaseConverter,
    LIST_TYPE_NUMBERED,
    LIST_TYPE_BULLET
)

class ConflueceConverter(BaseConverter):
    def __init__(self, options={}, log=None):
        super(ConflueceConverter, self).__init__(options, log)

    @property
    def log(self):
        return self._log

    def at_normal_text(self, text):
        self.log.debug("at_normal_text = `%s`" % (text))
        return text
    
    def at_heading(self, text, level):
        plus = 1
        if self._options.get('prefer_h1'):
            plus = 0
        return "h%d.%s" % (level + plus, text)

    def at_toc(self):
        return u'{toc}'

    def at_list(self, types):
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
        # TODO: rename to at_formatted_text
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

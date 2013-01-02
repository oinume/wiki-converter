# -*- coding: utf-8 -*-
import re
from ..converter import LIST_TYPE_BULLET, LIST_TYPE_NUMBERED
from ..parser import BaseParser, ParseError

class PukiwikiParser(BaseParser):

    def __init__(self, log=None):
        patterns = [
            ##############
            # blocks
            ##############
            { 'pattern': r'^(\*+)(.*)',     'callback': self.heading },
            { 'pattern': r'^#contents',     'callback': self.toc },
            { 'pattern': r"^\|(.*)\|h$",    'callback': self.table_header_columns },
            { 'pattern': r"^\|(.*)\|$",     'callback': self.table_columns },
            { 'pattern': r"^ (.+)$",        'callback': self.formatted_text, 'formatted_text': True },
            { 'pattern': r'^([\-\+]+)(.*)', 'callback': self.list },

            ##############
            # inline
            ##############
            { 'pattern': r"'''(.*?)'''(.*)",   'callback': self.italic, 'inline': True },
            { 'pattern': r"''(.*?)''(.*)",     'callback': self.strong, 'inline': True },
            { 'pattern': r"%%(.*?)%%(.*)",     'callback': self.strike_through, 'inline': True },
            { 'pattern': r"\[\[(.*?)\]\](.*)", 'callback': self.link, 'inline': True  },

            # no underline
            
        ]
        super(PukiwikiParser, self).__init__(patterns, log)

    def heading(self, groups):
        #text = groups[1]
        text = re.sub(r'\[#[\w]+\]', '', groups[1])
        self.log.debug("heading = {%s}" % (text))
        s = self.handler.at_heading(text, len(groups[0]))
        return s, ''

    def toc(self, groups):
        s = self.handler.at_toc()
        return s, ''

    def list(self, groups):
        types = []
        for char in groups[0]:
            if char == '-':
                types.append(LIST_TYPE_BULLET)
            elif char == '+':
                types.append(LIST_TYPE_NUMBERED)
            else:
                raise ParseError("Invalid list character: '%s'" % char)

        s = self.handler.at_list(types)
        if not re.match('^ ', groups[1]):
            s += ' '
        self._inline_only = True
        return s, groups[1]

    def table_header_columns(self, groups):
        line = groups[0]
        self.log.debug("line = `%s`" % (line))

        columns = []
        self._append_enabled = False
        for text in line.split('|'):
            text = text.strip()
            if text:
                columns.append(self.parse_line(text))
        self._append_enabled = True

        s = self.handler.at_table_header_columns(columns)
        return s, ''

    def table_columns(self, groups):
        line = groups[0]
        self.log.debug("line = `%s`" % (line))

        columns = []
        self._append_enabled = False
        for text in line.split('|'):
            text = text.strip()
            if text:
                self._append_enabled = False
                columns.append(self.parse_line(text))
        self._append_enabled = True
        s = self.handler.at_table_columns(columns)
        return s, ''

    def formatted_text(self, groups):
        if self.in_formatted_text() == False:
            # 始まり
            self._in_formatted_text = True
        self._formatted_text_buffer.append(groups[0])
        # 整形済みテキストの場合は現在の行の残りの部分はパースしない
        return '', ''

    def italic(self, groups):
        s = self.handler.at_italic(groups[0])
        return s, groups[1]

    def strong(self, groups):
        s = self.handler.at_strong(groups[0])
        return s, groups[1]

    def strike_through(self, groups):
        s = self.handler.at_strike_through(groups[0])
        return s, groups[1]

    def link(self, groups):
        #self.log.debug("link = `%s`" % (groups[0]))
        link = groups[0]
        array = re.split('[\|:>]?', link, 1)
        text = array[0]
        url = ''.join(array[1:])
        self.log.debug("text = `%s`, url = `%s`" % (text, url))
        s = self.handler.at_link(text, url)
        return s, groups[1]

    def parse_line_started(self, line):
        if not self._previous_line:
            return
        formatted_text_pattern = None
        for p in self._patterns:
            if p.get('callback') == self.formatted_text:
                formatted_text_pattern = p
                break
        regexp = formatted_text_pattern['regexp']
        if self.in_formatted_text() and not regexp.match(line):
            # 直前の行がスペースで始まるformatted textの場合で、
            # 現在の行がformatted textではない場合
            # →formatted textが終わったとみなしてhandlerのメソッドを呼び出す
            self.finish_formatted_text()

    def parse_line_finished(self, line):
        # 1行パースし終わったら改行を入れる
        if not line:
            return
        if self.in_formatted_text():
            if len(self._formatted_text_buffer.value) != 0:
                # 整形済みテキストの場合は、バッファが空ではない場合のみ改行を追加
                self.append(self.handler.at_new_line())
        else:
            self.append(self.handler.at_new_line())

    def parse_finished(self, text):
        if self.in_formatted_text():
            # 直前の行がスペースで始まるformatted textの場合で、
            # パースが終わった場合
            # →formatted textが終わったとみなしてhandlerのメソッドを呼び出す
            self.finish_formatted_text()

    def finish_formatted_text(self):
        self._in_formatted_text = False
        s = self.handler.at_formatted_lines(self._formatted_text_buffer.value)
        self.append(s)
        # 整形済みテキストのバッファをクリア
        self._formatted_text_buffer.reset()

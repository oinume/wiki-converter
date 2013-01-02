# -*- coding: utf-8 -*-

import re
from ..converter import LIST_TYPE_BULLET, LIST_TYPE_NUMBERED
from ..parser import BaseParser, ParseError

class ConfluenceParser(BaseParser):
    def __init__(self, log=None):
        patterns = [
            ##############
            # blocks
            ##############
            { 'pattern': r'^h([0-9]+)\.(.*)',   'callback': self.heading },
            { 'pattern': r'^{toc}(.*)',         'callback': self.toc },
            { 'pattern': r"^\|\|(.*)\|\|$",     'callback': self.table_header_columns },
            { 'pattern': r"^\|(.*)\|$",         'callback': self.table_columns },
            { 'pattern': r"^(.*)\{code\}(.*)$", 'callback': self.formatted_text, 'formatted_text': True },
            { 'pattern': r'^([\*\#]+) (.*)',    'callback': self.list },

            ##############
            # inline
            ##############
            { 'pattern': r"_(.*?)_(.*)",   'callback': self.italic, 'inline': True },
            { 'pattern': r"-(.*?)-(.*)",   'callback': self.strike_through, 'inline': True },
            { 'pattern': r"\[(.*?)\](.*)", 'callback': self.link, 'inline': True  },
            { 'pattern': r"\*(.*?)\*(.*)", 'callback': self.strong, 'inline': True },

            # no underline
        ]
        super(ConfluenceParser, self).__init__(patterns, log)

    def heading(self, groups):
        level, text = int(groups[0]), groups[1]
        self.log.debug("heading = {%s}" % (text))
        s = self.handler.at_heading(text, level)
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
        columns = []
        self._append_enabled = False
        for text in line.split('||'):
            text = text.strip()
            if text:
                columns.append(self.parse_text(text))
        self._append_enabled = True

        s = self.handler.at_table_header_columns(columns)
        return s, ''

    def table_columns(self, groups):
        line = groups[0]
        columns = []
        self._append_enabled = False
        for text in line.split('|'):
            text = text.strip()
            if text:
                columns.append(self.parse_text(text))
        self._append_enabled = True
        s = self.handler.at_table_columns(columns)
        return s, ''

    def formatted_text(self, groups):
        s = ''
        if self.in_formatted_text() == False:
            # {code}の始まり
            self._in_formatted_text = True
            self._formatted_text_buffer.append(groups[1])
        else:
            # {code}の終わり
            self._in_formatted_text = False
            self._formatted_text_buffer.append(groups[0])
            s = self.handler.at_formatted_lines(self._formatted_text_buffer.value)
            # 整形済みテキストのバッファをクリア
            self._formatted_text_buffer.reset()
        # 整形済みテキストの場合は現在の行の残りの部分はパースしない
        return s, ''

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
        self.log.debug("link = `%s`" % (groups[0]))
        link = groups[0]
        array = re.split('[\|]?', link, 1)
        text, url = None, None
        if len(array) == 1:
            text, url = array[0], array[0]
        else:
            text, url = array[0], ''.join(array[1:])
        self.log.debug("text = `%s`, url = `%s`" % (text, url))
        s = self.handler.at_link(text, url)
        return s, groups[1]

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

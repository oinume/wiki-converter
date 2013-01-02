# -*- coding: utf-8 -*-

#import re
from ..converter import LIST_TYPE_BULLET, LIST_TYPE_NUMBERED
from ..parser import ParseError
from .confluence import ConfluenceParser

class ConfluenceAmebloParser(ConfluenceParser):

    def __init__(self, log=None):
        super(ConfluenceAmebloParser, self).__init__(log)
        self._in_list_type = None
        

    def list(self, groups):
        list_types = groups[0]
        if len(list_types) > 1:
            raise ParseError("Nested list is not supported.")
        self._inline_only = True
        if list_types.startswith('*'):
            if not self._in_list_type:
                self.append("<ul>")
            self.append("<li>")
            self._in_list_type = LIST_TYPE_BULLET
        elif list_types.startswith('#'):
            if not self._in_list_type:
                self.append("<ol>")
            self.append("<li>")
            self._in_list_type = LIST_TYPE_NUMBERED
        else:
            raise ParseError("Unknown list type: " + list_types)
        # このメソッド内でappendしているので、最初のreturn値は空の文字列を返す
        return '', groups[1]

    """
    リストのパースの方法
    <ソース>
    * hoge
    * fuga
    <変換後>
    <ul> <-- 前の行がlistでない、かつ今の行がlist
    <li>hoge</li> <-- <li>タグは self.listでappend。</li>のタグはfinish_listでappend
    <li>fuga</li>
    </ul> <-- 前の行がlistで、かつ今の行がlistでない
    """
    # 行のパースが始まった時に呼び出される
    def parse_line_started(self, line):
#        if not self._previous_line:
#            return
        list_pattern, table_header_columns_pattern, table_columns_pattern = None, None, None

        for p in self._patterns:
            if p.get('callback') == self.list:
                list_pattern = p
            elif p.get('callback') == self.table_header_columns:
                table_header_columns_pattern = p
            elif p.get('callback') == self.table_columns:
                table_columns_pattern = p

        list_regexp = list_pattern['regexp']
        if self._in_list_type and not list_regexp.match(line):
            self.finish_list()
#        elif self._in_table and not table_pattern['regexp'].match(line):
#            self.finish_table()

    def parse_line_finished(self, line):
        # 1行パースし終わったら改行を入れる
        if not line:
            return
        if self.in_formatted_text():
            if len(self._formatted_text_buffer.value) != 0:
                # 整形済みテキストの場合は、バッファが空ではない場合のみ改行を追加
                self.append(self.handler.at_new_line())
        if self._in_list_type:
            self.append("</li>")
            self._inline_only = False
        # アメブロで改行を入れると<br>に変換されてしまうのであえて改行入れない
        pass

    def finish_list(self):
        if self._in_list_type == LIST_TYPE_BULLET:
            self.append("</ul>")
        elif self._in_list_type == LIST_TYPE_NUMBERED:
            self.append("</ol>")
        self._in_list_type = None
        self._inline_only = False
        #self.log.debug("call handler.at_formatted_lines() --> %s" % (self._formatted_text_buffer.value))

    # パースが終わった時に呼び出される
    def parse_finished(self, text):
        if self._in_list_type:
            # 直前の行がlistの場合で、パースが終わった場合
            # →listが終わったとみなしてfinish_list()を呼ぶ
            self.finish_list()
#        if self._in_table:
#            # 直前の行がtableの場合で、パースが終わった場合
#            # →tableが終わったとみなしてfinish_table()を呼ぶ
#            self.finish_table()

    def finish_formatted_text(self):
        self._in_formatted_text = False
        s = self.handler.at_formatted_lines(self._formatted_text_buffer.value)
        self.append(s)
        #self.log.debug("call handler.at_formatted_lines() --> %s" % (self._formatted_text_buffer.value))
        # 整形済みテキストのバッファをクリア
        self._formatted_text_buffer.reset()

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


# -*- coding: utf-8 -*-

"""
from wiki_converter.function import create_parser, create_converter
parser = create_parser('pukiwki', logger)
converter = create_converter('confluence', logger)
parser.parse(file, converter)
# or parser.parse_text(text, converter)
text = parser.converted_text
"""

# TODO
# lsx -> sorted-children or pagetree2
# *の[#hash]は消していい
# -[Page]ほげ
# みたいなのを処理するとき、リストに入ったら__inline_onlyのフラグを立てて、インラインのパターンのみ実行する
# 行の最後まで来たら __inline_only のフラグを外す

# blocks
#  heading
#  list
#  table
#
# text effects
#  italic
#  strong
#  strike_through
#  link

import re
from wiki_converter.common import ParseError
from wiki_converter.log import create_logger
from wiki_converter.handler import LIST_TYPE_BULLET, LIST_TYPE_NUMBERED

class ConvertingBuffer(object):
    def __init__(self):
        self.__b = u''

    def append(self, text):
        if text is None:
            return
        self.__b += text

    def append_ln(self, text):
        if text is None:
            return
        self.__b += text + u'\n'

    def reset(self):
        self.__b = u''

    @property
    def value(self):
        return self.__b

    def __repr__(self):
        return self.value()

    def __str__(self):
        return self.value()

class BaseParser(object):
    def __init__(self, patterns, log):
        self.__log = log
        self.__handler = None
        self.__buffer = ConvertingBuffer()
        self.__append_enabled = True
        self.__inline_only = False

        for pattern in patterns:
            pattern['regexp'] = re.compile(pattern['pattern'])
        self.__patterns = patterns

    def parse_text(self, text, handler):
        pass

    def get_handler(self):
        return self.__handler

    def set_handler(self, handler):
        self.__handler = handler

    @property
    def log(self):
        return self.__log

    @property
    def patterns(self):
        return self.__patterns

    @property
    def buffer(self):
        return self.__buffer

    handler = property(get_handler, set_handler)

class PukiwikiParser(BaseParser):

    def __init__(self, log=create_logger()):
        patterns = [
            ##############
            # blocks
            ##############
            { 'pattern': r'^(\*+)(.*)',     'callback': self.heading },
            { 'pattern': r'^#contents',     'callback': self.toc },
            { 'pattern': r"^\|(.*)\|h$",    'callback': self.table_header_columns },
            { 'pattern': r"^\|(.*)\|$",     'callback': self.table_columns },
            { 'pattern': r"^ (.+)$",        'callback': self.formatted_text },
            { 'pattern': r'^([\-\+]+)(.*)', 'callback': self.list },

            ##############
            # inline
            ##############
            { 'pattern': r"'''(.*?)'''(.*)",   'callback': self.italic, 'inline': True },
            { 'pattern': r"''(.*?)''(.*)",     'callback':  self.strong, 'inline': True },
            { 'pattern': r"%%(.*?)%%(.*)",     'callback':  self.strike_through, 'inline': True },
            { 'pattern': r"\[\[(.*?)\]\](.*)", 'callback': self.link, 'inline': True  },

            # no underline
            
        ]
        super(PukiwikiParser, self).__init__(patterns, log)
        self.__append_enabled = True
        self.__inline_only = False
        self.formatted_text_buffer = ''

    def append(self, text):
        self.buffer.append(text)

    def normal_text(self, text):
        self.flush_buffers()
        if len(text) == 0:
            return ''
        # 1文字分切りだす
        s = self.handler.at_normal_text(text[0:1])
        if len(text) == 1:
            return s, ''
        else:
            # 残りの文字列を次に処理させる
            return s, text[1:]

    def heading(self, groups):
        s = self.handler.at_heading(groups[1], len(groups[0]))
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
        self.__inline_only = True
        return s, groups[1]

    def table_header_columns(self, groups):
        line = groups[0]
        self.log.debug("line = `%s`" % (line))

        columns = []
        self.__append_enabled = False
        for text in line.split('|'):
            text = text.strip()
            if text:
                columns.append(self.parse_line(text, self.handler))
        self.__append_enabled = True

        s = self.handler.at_table_header_columns(columns)
        return s, ''

    def table_columns(self, groups):
        line = groups[0]
        self.log.debug("line = `%s`" % (line))

        columns = []
        self.__append_enabled = False
        for text in line.split('|'):
            text = text.strip()
            if text:
                self.__append_enabled = False
                columns.append(self.parse_line(text, self.handler))
        self.__append_enabled = True
        s = self.handler.at_table_columns(columns)
        return s, ''

    def formatted_text(self, groups):
        text = groups[0]
        self.formatted_text_buffer += text + '\n'
        self.__append_enabled = False
        # 整形済みテキストの場合は現在の行はパースしない
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
        self.log.debug("link = `%s`" % (groups[0]))
        link = groups[0]
        array = re.split('[\|:>]?', link)
        text = array[0]
        url = ''.join(array[1:])
        self.log.debug("text = `%s`, url = `%s`" % (text, url))
        s = self.handler.at_link(text, url)
        return s, groups[1]

    def flush_buffers(self):
        if self.formatted_text_buffer:
            s = self.handler.at_formatted_lines(self.formatted_text_buffer)
            self.append(s)
            # 整形済みテキストが終わったのでバッファクリア
            self.formatted_text_buffer = ''
            self.__append_enabled = True


    def parse_text(self, text, handler):
        self.handler = handler
        for line in text.split('\n'):
            self.parse_line(line.rstrip(), handler)
            if self.__append_enabled:
                self.append(self.handler.at_new_line())
            self.__inline_only = False
        self.flush_buffers()

    def parse_line(self, line, handler):
        # textにパースする文字列を入れる。これが空になるまでループする
        text = line
        matched_count = 0
        result = ''

        while len(text) != 0:
            matched = None

            for p in self.patterns:
                pattern, regexp, callback, inline = p['pattern'], p['regexp'], p['callback'], p.get('inline')
                if regexp is None:
                    self.log.error("regexp is None for `%s`" % pattern)
                    continue
                if callback is None:
                    self.log.error("callback is None for `%s`" % pattern)
                    continue

                if self.__inline_only and not inline:
                    # インライン用のパターン以外は無視
                    self.log.debug("`%s` ignored. inline only." % pattern)
                    continue
                elif matched_count > 0 and not inline:
                    # 2回目以降はインラインではない場合スルー
                    self.log.debug("`%s` ignored. inline only." % pattern)
                    continue

                matched = regexp.match(text)
                self.log.debug("`%s` -> `%s`, matched = `%s`" % (pattern, text, matched))
                if matched:
                    # 正規表現にマッチしたら登録されているコールバックを呼ぶ
                    converted, text = callback(matched.groups())
                    if self.__append_enabled:
                        self.append(converted)
                    result += converted
                    self.log.debug("converted = `%s`, text = `%s`, buffer = `%s`, result = `%s`" % (converted, text, self.buffer.value, result))
                    matched_count += 1
                    break

            if matched is None:
                converted, t = self.normal_text(text)
                self.log.debug("normal_text(): `%s` -> `%s`, `%s`" % (text, converted, t))
                text = t
                if self.__append_enabled:
                    self.append(converted)
                result += converted
                self.log.debug("converted = `%s`, text = `%s`, buffer = `%s`, result = `%s`" % (converted, text, self.buffer.value, result))

        return result

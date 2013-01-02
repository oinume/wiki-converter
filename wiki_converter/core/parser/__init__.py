#
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
from wiki_converter.core.log import create_logger

class ParseError(Exception):
    pass

class ConvertingBuffer(object):
    def __init__(self):
        self._b = u''

    def append(self, text):
        if text is None:
            return
        self._b += text

    def append_ln(self, text):
        if text is None:
            return
        self._b += text + u'\n'

    def reset(self):
        self._b = u''

    @property
    def value(self):
        return self._b

    def __repr__(self):
        return self.value()

    def __str__(self):
        return self.value()

class BaseParser(object):
    def __init__(self, patterns, log=None):
        if log:
            self._log = log
        else:
            self._log = create_logger()
        self._handler = None
        self._append_enabled = True
        self._buffer = ConvertingBuffer()
        self._formatted_text_buffer = ConvertingBuffer()
        self._in_formatted_text = False
        self._inline_only = False
        self._previous_line = None
        self._line_number = 0

        # patternsの設定がちゃんとなっているかをチェック
        patterns_validation_errors = []
        for p in patterns:
            pattern, callback = p['pattern'], p['callback']
            if pattern is None:
                patterns_validation_errors.append("Key `pattern` is None for `%s`" % pattern)
            if callback is None:
                patterns_validation_errors.append("Key `callback` is None for `%s`" % pattern)
            p['regexp'] = re.compile(p['pattern'])
        if patterns_validation_errors:
            raise Exception("patterns configuration is invalid.\n" + "\n".join(patterns_validation_errors))
        self._patterns = patterns

    def get_handler(self):
        return self._handler

    def set_handler(self, handler):
        self._handler = handler

    handler = property(get_handler, set_handler)

    @property
    def log(self):
        return self._log

    @property
    def patterns(self):
        return self._patterns

    @property
    def buffer(self):
        return self._buffer

    def append(self, text):
        if not self._append_enabled:
            return
        if self.in_formatted_text():
            self._formatted_text_buffer.append(text)
        else:
            self._buffer.append(text)

    def in_formatted_text(self):
        return self._in_formatted_text

    def parse(self, text, handler):
        self.handler = handler
        
        # 1行ごとに処理する
        for line in text.split('\n'):
            self.log.debug("line = `%s`" % (line.rstrip()))
            self.parse_line(line.rstrip())
            self._inline_only = False
        self.parse_finished(text)

    def parse_line(self, line):
        #  hoge
        #  fuga
        # *h1
        # {code}
        # hoge
        # fuga{code}
        # h1.title
        self.parse_line_started(line)
        converted = self.parse_text(line)
        self.parse_line_finished(line)
        self._previous_line = line
        self._line_number += 1
        return converted

    def parse_text(self, text):
        # restにパースする文字列を入れる。これが空になるまでループする
        rest = text
        result = ''
        matched_count = 0
        while len(rest) > 0:
            matched = None
            self.log.debug("IN while len(rest) > 0")
            for p in self.patterns:
                pattern, regexp, callback, inline = p['pattern'], p['regexp'], p['callback'], p.get('inline')
                if self._inline_only and not inline:
                    # インライン用のパターン以外は無視
                    self.log.debug("`%s` ignored. inline only." % pattern)
                    continue
                elif matched_count > 0 and not inline:
                    # 2回目以降はインラインではない場合スルー
                    self.log.debug("`%s` ignored. inline only." % pattern)
                    continue

                matched = regexp.match(rest)
                self.log.debug(
                    "parse_text() %d: text = `%s` -> pattern = `%s`, matched = `%s`"
                    % (len(rest), text, pattern, matched))
                if matched:
                    # 正規表現にマッチしたら登録されているコールバックを呼ぶ
                    # converted: handlerを使ってフォーマット変換したテキスト
                    # rest     : フォーマット未変換の残りの文字列
                    converted, rest = callback(matched.groups(''))
                    self.append(converted)
                    result += converted
                    self.log.debug("converted = `%s`, rest = `%s`, result = `%s`, buffer = `%s`, formatted_text_buffer = `%s`" % (converted, rest, result, self.buffer.value, self._formatted_text_buffer.value))
                    matched_count += 1
                    break

            if matched is None:
                # どのパターンにもマッチしなかった場合は normal_text() を呼び出して
                # 通常のテキストとして処理させる
                #self.flush_buffers()
                converted, t = self.normal_text(rest)
                self.log.debug("normal_text(): `%s` -> `%s`, `%s`" % (text, converted, t))
                rest = t
                self.append(converted)
                result += converted
                matched_count += 1
                self.log.debug("converted = `%s`, rest = `%s`, result = `%s`, buffer = `%s`, formatted_text_buffer = `%s`" % (converted, rest, result, self.buffer.value, self._formatted_text_buffer.value))
        return result

    def normal_text(self, text):
        if len(text) == 0:
            return ''
        # 1文字分切りだす
        s = self.handler.at_normal_text(text[0:1])
        if len(text) == 1:
            return s, ''
        else:
            # 残りの文字列を次に処理させる
            return s, text[1:]

    # サブクラスでオーバライドされるべきメソッド
    def parse_finished(self, text):
        pass

    def parse_line_started(self, line):
        pass

    def parse_line_finished(self, line):
        pass

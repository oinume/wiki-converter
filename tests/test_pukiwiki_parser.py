# -*- coding: utf-8 -*-

import unittest
from nose.tools import eq_, ok_
from wiki_converter.log import create_logger
from wiki_converter.function import create_parser, create_converter

class TestPukiwikiParser(unittest.TestCase):
    def setUp(self):
        self.log = create_logger(True)
        self.p = create_parser('pukiwiki', self.log)
        self.c = create_converter('confluence', self.log)

    def testHeading(self):
        self.p.parse_text("* Heading1", self.c)
        eq_("h2. Heading1", self.p.buffer.value.rstrip(), 'heading1')

        self.p.buffer.reset()
        self.p.parse_text(u"***ヘッディング3", self.c)
        eq_(u"h4.ヘッディング3", self.p.buffer.value.rstrip(), "heading3")

    def testToc(self):
        self.p.parse_text(u"#contents", self.c)
        eq_(u"{toc}", self.p.buffer.value.rstrip(), "toc")

#    def testTableColumns(self):
#        self.converter.reset_converted_text()
#        self.parser.parse_text(u"| ほげ | ふが |", self.converter)
#        eq_(
#            u"| ほげ | ふが |\n",
#            self.converter.converted_text,
#            'table_columns'
#        )
#
#    def testHeaderTableColumns(self):
#        self.converter.reset_converted_text()
#        self.parser.parse_text(u"| これは | ヘッダー |h", self.converter)
#        eq_(
#            u"|| これは || ヘッダー ||\n",
#            self.converter.converted_text,
#            'table_header_columns'
#        )
#
#    def testTable(self):
#        self.converter.reset_converted_text()
#        self.parser.parse_text("""\
#| num | text |h
#| 1 | one |
#""".rstrip(), self.converter)
#
#        eq_("""\
#|| num || text ||
#| 1 | one |
#""".rstrip(),
#            self.converter.converted_text.rstrip(),
#            'table_header_columns'
#        )
#
#    def testFormattedText(self):
#        self.converter.reset_converted_text()
#        self.parser.parse_text(u"""\
# This is a
# formatted
# text.
#""".rstrip(), self.converter)
#        print self.converter.converted_text
#        eq_("""\
#{code}
#This is a
#formatted
#text.
#{code}
#""".rstrip(),
#            self.converter.converted_text.rstrip(),
#            'formatted_text'
#        )
#
    def testItalic(self):
        self.p.parse_text(u"'''Italic text.''' Normal text.", self.c)
        eq_(u"_Italic text._ Normal text.", self.p.buffer.value.rstrip(), "italic")

    def testStrong(self):
        self.p.parse_text(u"''Strong text.'' Normal text.", self.c)
        eq_(u"*Strong text.* Normal text.", self.p.buffer.value.rstrip(), "strong")

    def testLink(self):
        self.p.parse_text(u"[[リンクテスト|http://www.ameba.jp]]", self.c)
        self.log.debug("value : `%s`" % self.p.buffer.value)
        eq_(u"[リンクテスト|http//www.ameba.jp]", self.p.buffer.value.rstrip(), "link(with alias)")

        self.p.buffer.reset()
        self.p.parse_text(u"[[LinkPage]]", self.c)
        self.log.debug("value : `%s`" % self.p.buffer.value)
        eq_(u"[LinkPage]", self.p.buffer.value.rstrip(), "link(without alias)")

#    def testList(self):
#        self.converter.reset_converted_text()
#        self.parser.parse_text(u"""\
#- bullet1
#-- bullet2
#-+ bullet + number1
#-+ bullet + number2
#+ number1
#""", self.converter)
#
#        self.log.debug("converted : {%s}" % self.converter.converted_text)
#        eq_(u"""\
#* bullet1
#** bullet2
#*# bullet + number1
#*# bullet + number2
## number1
#""".rstrip(),
#            self.converter.converted_text.rstrip(),
#            'list'
#        )


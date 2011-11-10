# -*- coding: utf-8 -*-

import unittest
from nose.tools import eq_, ok_
from wiki_converter.log import create_logger
from wiki_converter.parser import PukiwikiParser
from wiki_converter.converter import ConfluecenConverter

class TestPukiwikiParser(unittest.TestCase):
    def setUp(self):
        self.log = create_logger(True)
        self.parser = PukiwikiParser(self.log)
        self.converter = ConfluecenConverter(self.log)

    def testHeading(self):
        self.converter.reset_converted_text()
        self.parser.parse_text(u"* ヘッディング1", self.converter)
        eq_(
            u"h2. ヘッディング1\n",
            self.converter.converted_text,
            'heading1'
        )
        
        self.converter.reset_converted_text()
        self.parser.parse_text(u"***ヘッディング3", self.converter)
        eq_(
            u"h4.ヘッディング3\n",
            self.converter.converted_text,
            'heading3'
        )

    def testToc(self):
        self.converter.reset_converted_text()
        self.parser.parse_text(u"#contents", self.converter)
        eq_(
            u"{toc}\n",
            self.converter.converted_text,
            'toc'
        )

    def testTableColumns(self):
        self.converter.reset_converted_text()
        self.parser.parse_text(u"| ほげ | ふが |", self.converter)
        eq_(
            u"| ほげ | ふが |\n",
            self.converter.converted_text,
            'table_columns'
        )

    def testHeaderTableColumns(self):
        self.converter.reset_converted_text()
        self.parser.parse_text(u"| これは | ヘッダー |h", self.converter)
        eq_(
            u"|| これは || ヘッダー ||\n",
            self.converter.converted_text,
            'table_header_columns'
        )

    def testTable(self):
        self.converter.reset_converted_text()
        self.parser.parse_text(
"""| num | text |h
| 1 | one |""", self.converter)

        eq_(
"""|| num || text ||
| 1 | one |\n""",
            self.converter.converted_text,
            'table_header_columns'
        )

    def testItalic(self):
        self.converter.reset_converted_text()
        self.parser.parse_text(u"'''Italic text.''' Normal text.", self.converter)
        self.log.debug("converted : `%s`" % self.converter.converted_text)
        eq_(
            u"_Italic text._ Normal text.",
            self.converter.converted_text,
            'italic'
        )

    def testStrong(self):
        self.converter.reset_converted_text()
        self.parser.parse_text(u"''Strong text.'' Normal text.", self.converter)
        self.log.debug("converted : `%s`" % self.converter.converted_text)
        eq_(
            u"*Strong text.* Normal text.",
            self.converter.converted_text,
            'strong'
        )

    def testLink(self):
        self.converter.reset_converted_text()
        self.parser.parse_text(u"[[リンクテスト|http://www.ameba.jp]]", self.converter)
        self.log.debug("converted : `%s`" % self.converter.converted_text)
        eq_(
            u"[リンクテスト|http//www.ameba.jp]",
            self.converter.converted_text,
            'link'
        )

    def testList(self):
        self.converter.reset_converted_text()
        self.parser.parse_text(u"""\
- bullet1
-- bullet2
-+ bullet + number1
-+ bullet + number2
+ number1
""", self.converter)

        self.log.debug("converted : {%s}" % self.converter.converted_text)
        eq_(
            u"""\
* bullet1
** bullet2
*# bullet + number1
*# bullet + number2
# number1
""".strip(),
            self.converter.converted_text.strip(),
            'list'
        )

#    def testComplex(self):
#        self.converter.reset_converted_text()
#        self.parser.parse_text(
#            u"""
#* タイトル
#''強調'' ほげほげ
#""",
#            self.converter)
#        print "converted : {%s}" % self.converter.converted_text

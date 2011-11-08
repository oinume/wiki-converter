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
            u"h2. ヘッディング1\n",
            self.converter.converted_text,
            'heading1'
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

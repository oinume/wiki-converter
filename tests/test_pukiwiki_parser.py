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

    def testHeading01(self):
        self.p.parse_text("* Heading1", self.c)
        eq_("h2. Heading1", self.p.buffer.value.rstrip(), 'heading1')

    def testHeading02(self):
        self.p.parse_text(u"***ヘッディング3", self.c)
        eq_(u"h4.ヘッディング3", self.p.buffer.value.rstrip(), "heading3")

    def testHeading03(self):
        self.p.parse_text("* Heading1 [#12345d]", self.c)
        eq_("h2. Heading1", self.p.buffer.value.rstrip(), "heading1")

    def testToc(self):
        self.p.parse_text(u"#contents", self.c)
        eq_(u"{toc}", self.p.buffer.value.rstrip(), "toc")

    def testNormalText(self):
        self.p.parse_text(u"MHA. for quality campaing.", self.c)
        eq_("MHA. for quality campaing.", self.p.buffer.value.rstrip(), "normal text")

    def testTableColumns(self):
        self.p.parse_text(u"| Hoge | Fuga |", self.c)
        eq_(u"|Hoge|Fuga|", self.p.buffer.value.rstrip(), "table_columns")

        self.p.buffer.reset()
        self.p.parse_text(u"|ほげ|ふが|", self.c)
        eq_(u"|ほげ|ふが|", self.p.buffer.value.rstrip(), "table_columns")

    def testTableColumnsComplex(self):
        self.p.parse_text(u"| Col | [[Page]] |", self.c)
        eq_(u"|Col|[Page]|", self.p.buffer.value.rstrip(), "table_columns complex")

    def testHeaderTableColumns(self):
        self.p.parse_text(u"| Header1 | Header2 |h", self.c)
        eq_(u"||Header1||Header2||", self.p.buffer.value.rstrip(), "table_header_columns")

    def testTable(self):
        self.p.parse_text("""\
| num | text |h
| 1 | one |
""".rstrip(), self.c)

        eq_("""\
||num||text||
|1|one|
""".rstrip(),
            self.p.buffer.value.rstrip(),
            "table",
        )

    def testFormattedText(self):
        self.p.parse_text(u"""\
 This is a
 formatted
 text.
""".rstrip(), self.c)

        eq_("""\
{code}
This is a
formatted
text.
{code}
""".rstrip(),
            self.p.buffer.value.rstrip(),
            "formatted_text",
        )

    def testItalic(self):
        self.p.parse_text(u"'''Italic text.''' Normal text.", self.c)
        eq_(u"_Italic text._ Normal text.", self.p.buffer.value.rstrip(), "italic")

    def testStrong(self):
        self.p.parse_text(u"''Strong text.'' Normal text.", self.c)
        eq_(u"*Strong text.* Normal text.", self.p.buffer.value.rstrip(), "strong")

    def testLinkWithPort(self):
        self.p.parse_text(u"[[Link:http://www.mydomain.jp:8080/admin]]", self.c)
        eq_(u"[Link|http://www.mydomain.jp:8080/admin]", self.p.buffer.value.rstrip(), "link")

    def testLinkWithAlias(self):
        self.p.parse_text(u"[[リンクテスト|http://www.ameba.jp]]", self.c)
        eq_(u"[リンクテスト|http://www.ameba.jp]", self.p.buffer.value.rstrip(), "link with alias")

    def testLinkWithoutAlias(self):
        self.p.parse_text(u"[[LinkPage]]", self.c)
        eq_(u"[LinkPage]", self.p.buffer.value.rstrip(), "link without alias")

    def testLinkComplex(self):
        self.p.parse_text(u"[[Page1]] [[Page2]]", self.c)
        eq_(u"[Page1] [Page2]", self.p.buffer.value.rstrip(), "link complex")

    def testListSimple(self):
        self.p.parse_text(u"""\
- bullet1
-- bullet2
-+ bullet + number1
-+ bullet + number2
+ number1
""", self.c)

        self.log.debug("value: {%s}" % self.p.buffer.value)
        eq_(u"""\
* bullet1
** bullet2
*# bullet + number1
*# bullet + number2
# number1
""".rstrip(),
            self.p.buffer.value.rstrip(),
            "list"
        )

    def testListComplex(self):
        self.p.parse_text(u"- page:[[page1]]", self.c)
        eq_(u"* page:[page1]", self.p.buffer.value.rstrip(), "list with a link")

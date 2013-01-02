import pytest
import utils

from wiki_converter.core.log import create_logger
from wiki_converter.core.function import create_parser, create_converter

class TestPukiwikiParser(object):
    
    def setup_method(self, method):
        self.log = create_logger(True)
        self.p = create_parser('pukiwiki', {}, self.log)
        self.c = create_converter('confluence', {}, self.log)

    def teardown_method(self, method):
        pass

    def test_heading_01(self):
        self.p.parse("* Heading1", self.c)
        assert "h2. Heading1" == self.p.buffer.value.rstrip()

    def test_heading_02(self):
        self.p.parse(u"***ヘッディング3", self.c)
        assert u"h4.ヘッディング3" == self.p.buffer.value.rstrip()

    def test_heading_03(self):
        self.p.parse("* Heading1 [#12345d]", self.c)
        assert "h2. Heading1" == self.p.buffer.value.rstrip()

    def test_toc(self):
        self.p.parse(u"#contents", self.c)
        assert u"{toc}" == self.p.buffer.value.rstrip()

    def test_normal_text(self):
        self.p.parse(u"MHA. for quality campaing.", self.c)
        assert "MHA. for quality campaing." == self.p.buffer.value.rstrip()

    def test_table_columns(self):
        self.p.parse(u"| Hoge | Fuga |", self.c)
        assert u"|Hoge|Fuga|" == self.p.buffer.value.rstrip()

    def test_table_columns_complex(self):
        self.p.parse(u"| Col | [[Page]] |", self.c)
        assert u"|Col|[Page]|" == self.p.buffer.value.rstrip()

    def test_header_table_columns(self):
        self.p.parse(u"| Header1 | Header2 |h", self.c)
        assert u"||Header1||Header2||" == self.p.buffer.value.rstrip()

    def test_table(self):
        self.p.parse("""\
| num | text |h
| 1 | one |
""".rstrip(), self.c)

        assert """\
||num||text||
|1|one|
""".rstrip() == self.p.buffer.value.rstrip()

    def test_formatted_text_01(self):
        self.p.parse(u"""\
 This is a
 formatted
 text.
""".rstrip(), self.c)

        assert """\
{code}
This is a
formatted
text.
{code}
""".rstrip() == self.p.buffer.value.rstrip()

    def test_formatted_text_02(self):
        self.p.parse(u"""\
 test

** heading1
** heading2
""".rstrip(), self.c)

        assert u"""\
{code}
test
{code}
h3. heading1
h3. heading2
""".rstrip() == self.p.buffer.value.rstrip()

    def test_formatted_text_03(self):
        self.p.parse(u"""\
 test

hoge
""".rstrip(), self.c)
        
        assert u"""\
{code}
test
{code}
hoge
""".rstrip() == self.p.buffer.value.rstrip()

    def test_formatted_text_04(self):
        self.p.parse(u"""\
 test

''strong''
""".rstrip(), self.c)
        
        assert u"""\
{code}
test
{code}
*strong*
""".rstrip() == self.p.buffer.value.rstrip()

    def test_italic(self):
        self.p.parse(u"'''Italic text.''' Normal text.", self.c)
        assert u"_Italic text._ Normal text."  == self.p.buffer.value.rstrip()

    def test_strong(self):
        self.p.parse(u"''Strong text.'' Normal text.", self.c)
        assert u"*Strong text.* Normal text." == self.p.buffer.value.rstrip()

    def test_link_with_port(self):
        self.p.parse(u"[[Link:http://www.mydomain.jp:8080/admin]]", self.c)
        assert u"[Link|http://www.mydomain.jp:8080/admin]" == self.p.buffer.value.rstrip()

    def test_link_with_alias(self):
        self.p.parse(u"[[リンクテスト|http://www.ameba.jp]]", self.c)
        assert u"[リンクテスト|http://www.ameba.jp]"== self.p.buffer.value.rstrip()

    def test_link_without_alias(self):
        self.p.parse(u"[[LinkPage]]", self.c)
        assert u"[LinkPage]" == self.p.buffer.value.rstrip()

    def test_link_complex(self):
        self.p.parse(u"[[Page1]] [[Page2]]", self.c)
        assert u"[Page1] [Page2]" == self.p.buffer.value.rstrip()

    def test_list_simple(self):
        self.p.parse(u"""\
-bullet1
-- bullet2
-+ bullet + number1
-+ bullet + number2
+ number1
""", self.c)

        #self.log.debug("value: {%s}" % self.p.buffer.value)
        assert u"""\
* bullet1
** bullet2
*# bullet + number1
*# bullet + number2
# number1
""".rstrip() == self.p.buffer.value.rstrip()

    def test_list_complex(self):
        self.p.parse(u"- page:[[page1]]", self.c)
        assert u"* page:[page1]" == self.p.buffer.value.rstrip()

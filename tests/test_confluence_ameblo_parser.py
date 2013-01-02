# -*- coding: utf-8 -*-

import pytest
import utils

from wiki_converter.core.log import create_logger
from wiki_converter.core.function import create_parser, create_converter

class TestConfluenceAmebloParser(object):
    
    def setup_method(self, method):
        self.log = create_logger(True)
        self.p = create_parser('confluence_ameblo', {}, self.log)
        self.c = create_converter('ameblo', {}, self.log)

    def teardown_method(self, method):
        pass

    def test_heading_01(self):
        self.p.parse("h1. Heading1", self.c)
        assert "<h4>Heading1</h4>" == self.p.buffer.value.rstrip()

#    def test_normal_text(self):
#        self.p.parse(u"MHA. for quality campaing.", self.c)
#        assert "MHA. for quality campaing." == self.p.buffer.value.rstrip()
#
#    def test_table_columns(self):
#        self.p.parse(u"| Hoge | Fuga |", self.c)
#        assert u"|Hoge|Fuga|" == self.p.buffer.value.rstrip()
#
#    def test_table_columns_complex(self):
#        self.p.parse(u"|Col|[Page]|", self.c)
#        assert u"|Col|[Page]|" == self.p.buffer.value.rstrip()
#
#    def test_header_table_columns(self):
#        self.p.parse(u"||Header1||Header2||", self.c)
#        assert u"||Header1||Header2||" == self.p.buffer.value.rstrip()
#
#    def test_table(self):
#        self.p.parse("""\
#||num||text||
#|1|one|
#""".rstrip(), self.c)
#
#        assert """\
#||num||text||
#|1|one|
#""".rstrip() == self.p.buffer.value.rstrip()
#
#    def test_formatted_text_01(self):
#        self.p.parse(u"""\
#{code}
#formatted
#text.
#{code}
#""".rstrip(), self.c)
#
##        self.log.debug("================\n" + self.p.buffer.value.rstrip())
#        assert """\
#{code}
#formatted
#text.
#{code}
#""".rstrip() == self.p.buffer.value.rstrip()
#
#    def test_formatted_text_02(self):
#        self.p.parse(u"""\
#{code}
#test
#{code}
#
#h3. heading1
#h3. heading2
#""".rstrip(), self.c)
#
#        assert u"""\
#{code}
#test
#{code}
#
#h4. heading1
#h4. heading2
#""".rstrip() == self.p.buffer.value.rstrip()

    def test_italic(self):
        self.p.parse(u"_Italic text._ Normal text.", self.c)
        assert u"<i>Italic text.</i> Normal text."  == self.p.buffer.value.rstrip()

    def test_strong(self):
        self.p.parse(u"*Strong text.* Normal text.", self.c)
        assert u"<strong>Strong text.</strong> Normal text." == self.p.buffer.value.rstrip()

    def test_link_with_port(self):
        self.p.parse(u"[Link|http://www.mydomain.jp:8080/admin]", self.c)
        assert u'<a href="http://www.mydomain.jp:8080/admin">Link</a>' == self.p.buffer.value.rstrip()

    def test_link_with_alias(self):
        self.p.parse(u"[リンクテスト|http://www.ameba.jp]", self.c)
        assert u'<a href="http://www.ameba.jp">リンクテスト</a>' == self.p.buffer.value.rstrip()

    def test_link_without_alias(self):
        self.p.parse(u"[http://www.ameba.jp]", self.c)
        assert u'<a href="http://www.ameba.jp">http://www.ameba.jp</a>' == self.p.buffer.value.rstrip()

    def test_list_complex_01(self):
        self.p.parse(u"""\
# [ameblo|http://ameblo.jp/]
# [ameba|http://s.amebame.com/]
""", self.c)
        assert u"""\
<ol><li><a href="http://ameblo.jp/">ameblo</a></li><li><a href="http://s.amebame.com/">ameba</a></li></ol>
""".rstrip() == self.p.buffer.value.rstrip()

    def test_list_complex_02(self):
        self.p.parse(u"""\
* *item1* normal
* item2
""", self.c)
        assert u"""
<ul><li><strong>item1</strong> normal</li><li>item2</li></ul>
""".strip() == self.p.buffer.value.rstrip()

# -*- coding: utf-8 -*-

import pytest
import utils

from wiki_converter.core.log import create_logger
from wiki_converter.core.function import create_parser, create_converter

class TestConfluenceParser(object):
    
    def setup_method(self, method):
        self.log = create_logger(True)
        self.p = create_parser('confluence', {}, self.log)
        self.c = create_converter('confluence', {}, self.log)

    def teardown_method(self, method):
        pass

    def test_heading_01(self):
        self.p.parse("h1. Heading1", self.c)
        assert "h2. Heading1" == self.p.buffer.value.rstrip()

    def test_heading_02(self):
        self.p.parse(u"h2.ヘッディング3", self.c)
        assert u"h3.ヘッディング3" == self.p.buffer.value.rstrip()

    def test_toc(self):
        self.p.parse(u"{toc}", self.c)
        assert u"{toc}" == self.p.buffer.value.rstrip()

    def test_normal_text(self):
        self.p.parse(u"MHA. for quality campaing.", self.c)
        assert "MHA. for quality campaing." == self.p.buffer.value.rstrip()

    def test_table_columns(self):
        self.p.parse(u"| Hoge | Fuga |", self.c)
        assert u"|Hoge|Fuga|" == self.p.buffer.value.rstrip()

    def test_table_columns_complex(self):
        self.p.parse(u"|Col|[Page]|", self.c)
        assert u"|Col|[Page]|" == self.p.buffer.value.rstrip()

    def test_header_table_columns(self):
        self.p.parse(u"||Header1||Header2||", self.c)
        assert u"||Header1||Header2||" == self.p.buffer.value.rstrip()

    def test_table(self):
        self.p.parse("""\
||num||text||
|1|one|
""".rstrip(), self.c)

        assert """\
||num||text||
|1|one|
""".rstrip() == self.p.buffer.value.rstrip()

    def test_formatted_text_01(self):
        self.p.parse(u"""\
{code}
formatted
text.
{code}
""".rstrip(), self.c)

#        self.log.debug("================\n" + self.p.buffer.value.rstrip())
        assert """\
{code}
formatted
text.
{code}
""".rstrip() == self.p.buffer.value.rstrip()

    def test_formatted_text_02(self):
        self.p.parse(u"""\
{code}
test
{code}

h3. heading1
h3. heading2
""".rstrip(), self.c)

        assert u"""\
{code}
test
{code}

h4. heading1
h4. heading2
""".rstrip() == self.p.buffer.value.rstrip()

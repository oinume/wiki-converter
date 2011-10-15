# -*- coding: utf-8 -*-

import unittest
from wiki_converter.parser import PukiwikiParser
from wiki_converter.converter import ConfluecenConverter

class TestPukiwikiParser(unittest.TestCase):
    def setUp(self):
        self.parser = PukiwikiParser()
        self.converter = ConfluecenConverter()

    def testParse(self):
        self.parser.parse_text(u"* ヘッディング1", self.converter)
        print "converted: " + self.converter.get_current_converted_text()

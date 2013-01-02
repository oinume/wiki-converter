#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
from wiki_converter.core.log import create_logger
from wiki_converter.core.function import create_parser, create_converter

if __name__ == '__main__':
    l = create_logger(True)
    p = create_parser('pukiwiki', {}, l)
    c = create_converter('confluence', { 'prefer_h1': True }, l)
    input = sys.stdin.read()
    p.parse(input, c)
    print "=== input ==="
    print input
    print "=== output ==="
    print p.buffer.value
    print "=== end ==="
    # TODO: Airの/usr/local/share/python削除

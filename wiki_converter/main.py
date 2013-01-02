# -*- coding: utf-8 -*-
import os
import sys
def set_sys_path(file):
    parent, bin_dir = os.path.split(os.path.dirname(os.path.abspath(__file__)))
    sys.path.insert(0, parent)

set_sys_path(__file__)
#print sys.path

from bottle import run
from wiki_converter.webapp import app
from wiki_converter.config import config
from wiki_converter.views import root, confluence, ameblo

if __name__ == '__main__':
    #print config
    run(app,
        host=config['host'], port=config['port'],
        debug=config['debug'], reloader=config['reloader'],
        server=config['server'])

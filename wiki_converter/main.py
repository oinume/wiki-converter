# -*- coding: utf-8 -*-
import os
import sys
def set_sys_path(file):
    parent, bin_dir = os.path.split(os.path.dirname(os.path.abspath(__file__)))
    sys.path.insert(0, parent)

set_sys_path(__file__)
#print sys.path
from wiki_converter import app

if __name__ == '__main__':
    app.run(debug = app.config['DEBUG'])

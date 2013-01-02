# -*- coding: utf-8 -*-
from wiki_converter.webapp import app, template

@app.route('/confluence/pukiwiki')
def pukiwiki():
    return template(
        'index.html',
        parser='pukiwiki',
        converter='confluence',
    )

@app.route('/confluence/confluence')
def confluence():
    return template(
        'index.html',
        parser='confluence',
        converter='confluence',
    )


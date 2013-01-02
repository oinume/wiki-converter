# -*- coding: utf-8 -*-
from wiki_converter.webapp import app, template

@app.route('/ameblo/confluence')
def confluence():
    return template(
        'index.html',
        parser='confluence_ameblo',
        converter='ameblo',
    )

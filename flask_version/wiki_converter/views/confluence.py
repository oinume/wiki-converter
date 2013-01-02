# -*- coding: utf-8 -*-
from flask import (
    Blueprint,
    current_app,
    redirect,
    render_template,
    request,
    session,
    url_for,
)
#import wiki_converter
from wiki_converter.core.function import (
    create_parser, create_converter
)

app = Blueprint('confluence', __name__)

@app.route('/confluence/index')
def index():
    return render_template('confluence/index.html')

@app.route('/confluence/process', methods = [ 'POST' ])
def process():
    log = current_app.logger
    v = request.values
    source = v['source']
    if not source:
        return redirect('/confluence/index')

    parser = create_parser('pukiwiki', log)
    converter = create_converter('confluence', log)
    parser.parse_text(source, converter)

    return render_template(
        'confluence/complete.html',
        converted_text=parser.buffer.value
    )


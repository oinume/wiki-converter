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
import wiki_converter
import wiki_converter.function

app = Blueprint('pukiwki', __name__)

@app.route('/pukiwiki')
def index():
    return render_template('index.html', type='pukiwiki')

@app.route('/pukiwiki/process', methods = [ 'POST' ])
def process():
    log = current_app.logger
    v = request.values
    source = v['source']
    if not source:
        return redirect('/')

    parser = wiki_converter.function.create_parser('pukiwiki', log)
    converter = wiki_converter.function.create_converter('confluence', log)
    parser.parse_text(source, converter)

    return render_template(
        'complete.html',
        converted_text=parser.buffer.value
    )


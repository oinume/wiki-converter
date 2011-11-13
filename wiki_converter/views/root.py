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

#import config

app = Blueprint('root', __name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/process', methods = [ 'POST' ])
def process():
    log = current_app.logger
    v = request.values
    source = v['source']
    if not source:
        return redirect('/')

    parser = wiki_converter.create_parser('pukiwiki', log)
    converter = wiki_converter.create_converter('confluence', log)
    parser.parse_text(source, converter)
    log.debug('=== converted === \n%s' % (converter.converted_text))

    return render_template(
        'complete.html',
        converted_text=converter.converted_text
    )
    #return redirect('/complete')

@app.route('/complete')
def complete():
    return render_template('complete.html')

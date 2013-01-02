# -*- coding: utf-8 -*-
from bottle import request, redirect
from wiki_converter.webapp import app, template
from wiki_converter.core.function import create_parser, create_converter

@app.route('/')
def index():
    return 'hello world'

@app.route('/process', method='POST')
def process():
    source = request.params.source
    parser = request.params.parser or 'pukiwiki'
    converter = request.params.converter or 'confluence'
    prefer_h1 = bool(request.params.prefer_h1 or '')

    app.log.debug("parser = %s, prefer_h1 = %s" % (parser, prefer_h1))
    app.log.debug("===== source =====\n" + source)
    if not source:
        return redirect("/%s/%s" % (converter, parser))

    parser = create_parser(parser, {}, app.log)
    converter = create_converter(converter, { 'prefer_h1': prefer_h1 }, app.log)
    parser.parse(source, converter)

    return template(
        'complete.html',
        converter='confluence',
        converted_text=parser.buffer.value
    )

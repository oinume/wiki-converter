# -*- coding: utf-8 -*-
from flask import Flask
import wiki_converter.config
from wiki_converter.parser import *
from wiki_converter.converter import *

#from extensions import init_db

app = Flask(__name__)
app.config.from_object(config.object)
app.logger.info("config.object = %s" % wiki_converter.config.object)

from wiki_converter.views import root
app.register_blueprint(root.app)

type2parser = {
    'pukiwiki': PukiwikiParser,
}
type2converter = {
    'confluence': ConfluecenConverter,
}

def create_parser(wiki_type, log=None):
    ParserClass = type2parser[wiki_type]
    if ParserClass is None:
        raise ValueError("Unknown wiki_type:" + wiki_type)
    return ParserClass(log)

def create_converter(wiki_type, log=None):
    ConverterClass = type2converter[wiki_type]
    if ConverterClass is None:
        raise ValueError("Unknown wiki_type:" + wiki_type)
    return ConverterClass(log)

from wiki_converter.parser import *
from wiki_converter.converter import *

type2parser = {
    'pukiwiki': PukiwikiParser,
}
type2converter = {
    'confluence': ConfluecenConverter,
}

def create_parser(wiki_type, log=None):
    ParserClass = type2parser.get(wiki_type)
    if ParserClass is None:
        raise ValueError("Unknown wiki_type:" + wiki_type)
    return ParserClass(log)

def create_converter(wiki_type, log=None):
    ConverterClass = type2converter.get(wiki_type)
    if ConverterClass is None:
        raise ValueError("Unknown wiki_type:" + wiki_type)
    return ConverterClass(log)

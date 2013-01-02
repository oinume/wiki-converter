from .parser.confluence import ConfluenceParser
from .parser.confluence_ameblo import ConfluenceAmebloParser
from .parser.pukiwiki import PukiwikiParser
from .converter.confluence import ConflueceConverter
from .converter.ameblo import AmebloConverter

type2parser = {
    'pukiwiki': PukiwikiParser,
    'confluence': ConfluenceParser,
    'confluence_ameblo': ConfluenceAmebloParser,
}
type2converter = {
    'confluence': ConflueceConverter,
    'ameblo': AmebloConverter,
}

def create_parser(wiki_type, options={}, log=None):
    ParserClass = type2parser.get(wiki_type)
    if ParserClass is None:
        raise ValueError("Unknown wiki_type:" + wiki_type)
    return ParserClass(log)

def create_converter(wiki_type, options={}, log=None):
    ConverterClass = type2converter.get(wiki_type)
    if ConverterClass is None:
        raise ValueError("Unknown wiki_type:" + wiki_type)
    return ConverterClass(options, log)

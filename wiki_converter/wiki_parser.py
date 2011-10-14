"""
parser = wiki_parser.create_parser('pukiwiki')
converter = wiki_parser.ConfluecenConverter()
parser.parse(file, converter)
text = converter.converted_text()
"""

class BaseParser(object):
    def __init__():
        pass

    def parse_text(text, handler):
        pass

class PukiwikiParser(BaseParser):
    pass


type2parser = {
    'pukiwiki': PukiwikiParser,
}

def create_parser(wiki_type):
    ParserClass = type2parser[wiki_type]
    if ParserClass is None:
        raise ValueError("Unknown wiki_type:" + wiki_type)
    return ParserClass()


class DefaultHandler(object):
    def __init__():
        pass

    def start_document():
        pass

    def end_document():
        pass

    def start_element():
        pass
    
    def end_element():
        pass

    def characters(text):
        pass

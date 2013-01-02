#!/bin/sh

WIKI_CONVERTER_ENV=development python wiki_converter/main.py

#    _opt("--version", action="store_true", help="show version number.")
#    _opt("-b", "--bind", metavar="ADDRESS", help="bind socket to ADDRESS.")
#    _opt("-s", "--server", default='wsgiref', help="use SERVER as backend.")
#    _opt("-p", "--plugin", action="append", help="install additional plugin/s.")
#    _opt("--debug", action="store_true", help="start server in debug mode.")
#    _opt("--reload", action="store_true", help="auto-reload on file changes.")
#    _cmd_options, _cmd_args = _cmd_parser.parse_args()
#    if _cmd_options.server and _cmd_options.server.startswith('gevent'):
#        import gevent.monkey; gevent.monkey.patch_all()

# -*- coding: utf-8 -*-
from flask import Flask
import wiki_converter.config

#from extensions import init_db

app = Flask(__name__)
app.config.from_object(wiki_converter.config.object)
app.logger.info("config.object = %s" % wiki_converter.config.object)

# TODO: 自動でimport
from wiki_converter.views import root
from wiki_converter.views import confluence

app.register_blueprint(root.app)
app.register_blueprint(confluence.app)



# -*- coding: utf-8 -*-
from flask import Flask
import wiki_converter.config

#from extensions import init_db

app = Flask(__name__)
app.config.from_object(wiki_converter.config.object)
app.logger.info("config.object = %s" % wiki_converter.config.object)

from wiki_converter.views import root
app.register_blueprint(root.app)


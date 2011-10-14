# -*- coding: utf-8 -*-
from flask import Flask
import config
#from extensions import init_db

app = Flask(__name__)
#init_db(app)

app.config.from_object(config.object)
app.logger.info("config.object = %s" % config.object)

from views import root
app.register_blueprint(root.app)

if __name__ == '__main__':
    app.run(debug = app.config['DEBUG'])

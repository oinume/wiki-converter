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
import urllib
import urlparse

import config

# parse_qsl moved to urlparse module in v2.6
try:
    from urlparse import parse_qsl
except:
    from cgi import parse_qsl

app = Blueprint('root', __name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/process', methods = [ 'POST' ])
def process():
    return redirect('/complete')

@app.route('/complete')
def complete():
    return render_template('complete.html')

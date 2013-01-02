# -*- coding: utf-8 -*-
from flask import (
    Blueprint,
    redirect,
)

app = Blueprint('root', __name__)

@app.route('/')
def index():
    return redirect('/confluence/index')


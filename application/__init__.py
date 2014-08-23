# coding: utf-8
from flask import ( Flask, g, )
app = Flask(__name__)

@app.before_request
def before_request():
    pass

@app.after_request
def after_request(response):
    return response

import routes

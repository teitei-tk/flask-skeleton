# coding: utf-8
import simplejson as json
from flask import ( Flask, g, session, request, make_response, )

from lib.storage import Storage

app = Flask(__name__)

@app.before_request
def before_request():
    g.session       = session
    g.charset       = 'utf-8'
    g.content_type  = 'text/html;charset=utf-8'

    g.json          = json
    g.request       = request
    g.storage       = Storage()

@app.after_request
def after_request(response):
    response = make_response(response)
    if hasattr(g, "content_type"):
        response.headers['Content-Type'] = g.content_type
    return response

import routes

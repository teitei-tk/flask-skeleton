# coding: utf-8
import simplejson as json
import jinja2
from flask import ( Flask, g, session, request, make_response, )

app = Flask(__name__)
app.jinja_loader = jinja2.FileSystemLoader('application/views/')

class Storage(object):
    _storage = None

    def __init__(self):
        self._storage = dict()

    def get(self, key):
        return self._storage.get(key)

    def set(self, key, value):
        self._storage[key] = value

    def remove(self, key):
        if self.get(key):
            del self._storage[key]
            return True
        return False


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

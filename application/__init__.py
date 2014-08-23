# coding: utf-8
import jinja2
import simplejson as json
from flask import ( Flask, g, session, request, make_response, )
from lib.storage import ( DictStorage, MemcacheStorage, )

app = Flask(__name__)
app.config.from_object("config.memcache")
app.jinja_loader = jinja2.FileSystemLoader('application/views/')

@app.before_request
def before_request():
    g.session       = session
    g.charset       = 'utf-8'
    g.content_type  = 'text/html;charset=utf-8'

    g.json          = json
    g.request       = request
    g.storage       = DictStorage()
    g.memcache      = MemcacheStorage(app.config['MEMCACHE_SETTING'])

@app.after_request
def after_request(response):
    response = make_response(response)
    if hasattr(g, "content_type"):
        response.headers['Content-Type'] = g.content_type
    return response

import routes

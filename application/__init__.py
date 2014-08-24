# coding: utf-8
import jinja2
import simplejson as json
from flask import ( Flask, g, session, request, make_response, )
from lib.storage import ( DictStorage, MemcacheStorage, )

class BootStrap(object):
    """
    app bootstrap
    """
    def __init__(self, flask):
        self.flask = flask

    def run(self, config_paths):
        for path in config_paths:
            self.flask.config.from_object(path)

        self.flask.jinja_loader = jinja2.FileSystemLoader('application/views/')

    def before_request(self):
        g.session       = session
        g.charset       = 'utf-8'
        g.content_type  = 'text/html;charset=utf-8'

        g.json          = json
        g.request       = request
        g.config        = app.config

        g.storage       = DictStorage()
        g.memcache      = MemcacheStorage(app.config['MEMCACHE_SETTING'])

    def after_request(self, response):
        response = make_response(response)
        if hasattr(g, "content_type"):
            response.headers['Content-Type'] = g.content_type
        return response

app = Flask(__name__)
bootstrap = BootStrap(app)
bootstrap.run(["config.database", "config.memcache"])

@app.before_request
def before_request():
    return bootstrap.before_request()

@app.after_request
def after_request(response):
    return bootstrap.after_request(response)

# set routing
import routes

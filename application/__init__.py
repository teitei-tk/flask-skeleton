# coding: utf-8
import jinja2
import simplejson as json
from peewee import ( MySQLDatabase, )
from werkzeug import ( cached_property, )
from flask import ( Flask, g, session, request, make_response, )
from lib.storage import ( DictStorage, MemcacheStorage, )

class BootStrap(object):
    """
    app bootstrap
    """
    def __init__(self, flask):
        self._flask = flask

    def run(self, config_paths):
        self.load_config(config_paths)
        self._flask.jinja_loader = jinja2.FileSystemLoader('application/views/')

    def load_config(self, paths):
        if isinstance(paths, str):
            paths = [paths]

        for path in paths:
            self._flask.config.from_object(path)

    @cached_property
    def config(self):
        return self._flask.config

    @cached_property
    def db(self):
        return MySQLDatabase(self.config['DATABASE_SETTING']['db_name'])

    def before_request(self):
        g.session       = session
        g.charset       = 'utf-8'
        g.content_type  = 'text/html;charset=utf-8'

        g.json          = json
        g.request       = request
        g.config        = self.config

        g.db            = self.db
        g.storage       = DictStorage()
        g.memcache      = MemcacheStorage(self.config['MEMCACHE_SETTING'])

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

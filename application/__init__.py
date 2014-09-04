# coding: utf-8
import os
import jinja2
import simplejson as json
from peewee import ( MySQLDatabase, )
from werkzeug import ( cached_property, )
from flask import ( Flask, g, session, request, make_response, )

from lib.storage import ( DictStorage, MemcacheStorage, )
from routes import ROUTING_MODULES

class BootStrap(object):
    """
    app bootstrap
    """
    _db     = None
    _flask  = None

    def __init__(self, flask):
        if not isinstance(flask, Flask):
            raise Exception("arg variable object is not Flask instance")
        self._flask = flask

    def run(self, config_paths):
        self.load_config(config_paths)
        self._flask.jinja_loader = jinja2.FileSystemLoader('application/views/')

    def load_config(self, paths):
        if isinstance(paths, str):
            paths = [paths]

        for path in paths:
            self._flask.config.from_object(path)

    @property
    def flask(self):
        return self._flask

    @cached_property
    def config(self):
        return self._flask.config
    
    @cached_property
    def db(self):
        if not self._db:
            db_config_key = "DATABASE_SETTING"
            if os.environ.get("CI", False):
                db_config_key = "CI_DATABASE_SETTING"

            db_setting = self.config[db_config_key]
            self._db = MySQLDatabase(db_setting['db_name'], host=db_setting['host'], 
                    port=db_setting['port'], user=db_setting['user'], passwd=db_setting['password'])
        return self._db

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

        self.before_action()

    def before_action(self):
        self.db.connect()

    def after_request(self, response):
        response = make_response(response)
        return self.after_action(response)

    def after_action(self, response):
        if hasattr(g, "content_type"):
            response.headers['Content-Type'] = g.content_type
        self.db.close()
        return response

    def set_routing(self, routing_modules):
        if not isinstance(routing_modules, list):
            routing_modules = [routing_modules]
        return [self._flask.register_blueprint(module) for module in routing_modules]

"""
this secret_key is example change required try this command

$ python
>>> import os
>>> os.urandom(24)
"""
app = Flask(__name__)
app.secret_key = '\x96hy\x96\xd6\x86\xb8#\xf0\x17\x81\n\xd8\x8a\xd3kp\x9c\xfd\xf6\x97\xf0\x89\xc8'

bootstrap = BootStrap(app)
bootstrap.run(["config.database", "config.memcache", "config.ci_database"])

@app.before_request
def before_request():
    return bootstrap.before_request()

@app.after_request
def after_request(response):
    return bootstrap.after_request(response)

# set access routing
bootstrap.set_routing(ROUTING_MODULES)

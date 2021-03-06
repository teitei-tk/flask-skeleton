# coding: utf-8
import os
import collections
import jinja2
import simplejson as json
from peewee import ( MySQLDatabase, )
from werkzeug import ( cached_property, import_string )
from flask import ( Flask, g, session, request, make_response, )

from lib.storage import ( DictStorage, MemcacheStorage, )

from routes import ( ROUTING_MODULES, )
from config import ( PROJECT_DIR, )

class BootStrap(object):
    """
    app bootstrap
    """
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
        config_key = "DATABASE_SETTING"
        if os.environ.get("CI"):
            config_key = "CI_DATABASE_SETTING"

        db_setting = self.config[config_key]
        return MySQLDatabase(db_setting['db_name'], host=db_setting['host'], 
                port=db_setting['port'], user=db_setting['user'], passwd=db_setting['password'])

    def get_logger(self, key='console'):
        from lib.logger import get_logger

        logger = None

        try:
            logger = get_logger(key)
        except KeyError:
            logger = get_logger('file')

        return logger

    @cached_property
    def logger(self):
        logger = None
        try:
            if g.is_debug:
                logger = self.get_logger('console')
            else:
                logger = self.get_logger()
        except:
            logger = self.get_logger()

        return logger

    def before_request(self):
        g.is_debug      = app.debug
        g.session       = session
        g.charset       = 'utf-8'
        g.content_type  = 'text/html;charset=utf-8'

        g.json          = json
        g.request       = request
        g.config        = self.config

        g.db            = self.db
        g.logger        = self.logger
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
        for module in routing_modules:
            try:
                view = import_string(module.import_path)
                self._flask.add_url_rule(
                        module.url, module.endpoint, view_func=view.as_view(module.endpoint))

            except ImportError:
                pass


"""
this secret_key is example change required try this command

$ python
>>> import os
>>> os.urandom(24)
"""
app = Flask(__name__)
app.secret_key = '\x96hy\x96\xd6\x86\xb8#\xf0\x17\x81\n\xd8\x8a\xd3kp\x9c\xfd\xf6\x97\xf0\x89\xc8'

bootstrap = BootStrap(app)
bootstrap.run(["config.database", "config.memcache", "config.logging"])

@app.before_request
def before_request():
    return bootstrap.before_request()

@app.after_request
def after_request(response):
    return bootstrap.after_request(response)

# set access routing
bootstrap.set_routing(ROUTING_MODULES)

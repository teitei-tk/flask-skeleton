# coding: utf-8
import simplejson as json
from flask import ( g, redirect, render_template, session, request, abort, )

class BaseRender(object):
    pass

class JsonRender(BaseRender):
    def render_json(self, data):
        g.content_type  = "text/json;charset=utf-8"
        return json.dumps(data)

    def render_error_json(self, data={}):
        return self.render_json(data)

class HtmlRender(BaseRender):
    def render_template(self):
        return 

class BaseController(HtmlRender, JsonRender):
    """
    usage:
        app = Blueprint("index", __name__)

        @app.route("/")
        def index():
            class Index(BaseController):
                def prepare(self):
                    # do validation
                    return True

                def perform(self):
                    # do CRUD
                    self.storage.set("hoge", "fuga")
                    return True

                def preforward(self):
                    # do view render
                    value = self.storage.get("hoge")
                    return self.render_json({"value" : value})

            return Index.action()
    """

    @classmethod
    def action(cls):
        instance = cls()

        if not instance.authenticate():
            return instance.render_error()
        if not instance.prepare():
            return instance.render_error()
        if not instance.perform():
            return instance.render_error()
        return instance.preforward()

    """
    using authentication
    """
    def authenticate(self):
        return True

    """
    before action
    """
    def prepare(self):
        return True

    """
    do action
    """
    def perform(self):
        return True

    """
    after action
    """
    def preforward(self):
        pass

    def render_error(self):
        abort(404)

    @property
    def request(self):
        return g.request

    @property
    def storage(self):
        return g.storage

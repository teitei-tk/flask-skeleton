# coding: utf-8
import simplejson as json
from flask import ( g, redirect, render_template, session, request, abort, )

class BaseRender(object):
    pass

class JsonRender(BaseRender):
    """
    json renderer
    """
    def render_json(self, data):
        g.content_type  = "text/json;charset=utf-8"
        return json.dumps(data)

    def render_error_json(self, data={}):
        return self.render_json(data)

class TemplateRender(BaseRender):
    """
    template renderer
    """
    def render_template(self, template_path, values):
        return render_template(template_path, **values)

class BaseController(TemplateRender, JsonRender):
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

    """
    do controller action
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
    do validation & prepareAction
    """
    def prepare(self):
        return True

    """
    do action
    """
    def perform(self):
        return True

    """
    do render
    """
    def preforward(self):
        return self.render_json({})

    def render_error(self):
        abort(404)

    """
    http request

    usasge:
        http request : hoge=1
        print(self.request.values.get('hoge')) -> 1
    """
    @property
    def request(self):
        return g.request

    """
    stash storage
    """
    @property
    def storage(self):
        return g.storage

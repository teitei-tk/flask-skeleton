# coding: utf-8
import simplejson as json

from flask import ( 
    g, 
    redirect, 
    render_template, 
    session, 
    request, 
    abort, 
    )

from flask.views import ( 
    View, 
    )

from lib.util import ( 
    CsrfProtection, 
    )

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
    def render_template(self, template_path, values={}):
        return render_template(template_path, **values)

class BaseHandler(View):
    """
    ControllerRequest
    """
    def dispatch_request(self):
        if not self.authenticate():
            return self.render_error()
        if not self.prepare():
            return self.render_error()
        if not self.perform():
            return self.render_error()
        return self.preforward()

class BaseController(TemplateRender, JsonRender, BaseHandler):
    """BaseController class"""

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
        return self.render_error()

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

    """
    csrf validation class property
    """
    @property
    def csrf(self):
        return CsrfProtection

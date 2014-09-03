# coding: utf-8
import simplejson as json
from flask import ( g, Blueprint, make_response, request, )

from tests import ( TestBase, TestBaseController, )
from application import ( app, bootstrap, )

controller_module = Blueprint("controller", __name__)

class TestJsonRender(TestBaseController):
    def preforward(self):
        return self.render_json({"value" : 1})

@controller_module.route("/test")
def json_render():
    return TestJsonRender.action()

class TestController(TestBase):
    def initialize(self):
        super(TestController, self).initialize()
        bootstrap.set_routing(controller_module)

    def get_response(self, app):
        rv = app.preprocess_request()
        if rv != None:
            response = app.make_response(rv)
        else:
            rv = app.dispatch_request()
            response = app.make_response(rv)
            response = app.process_response(response)
        return response

    def test_json_render(self):
        with app.test_request_context("/test"):
            response = self.get_response(app)

            self.assertEqual(response.mimetype, "text/json")
            self.assertEqual(response.data.decode('utf-8'), json.dumps({"value" : 1}))

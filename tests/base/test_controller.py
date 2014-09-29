# coding: utf-8
import jinja2
import simplejson as json

from tests import ( TestBase, TestBaseController, )
from application import ( bootstrap, )
from routes import ( merge_routing_modules, )

class TestJsonRender(TestBaseController):
    def preforward(self):
        return self.render_json({"value" : 1})

class TestTemplateRender(TestBaseController):
    def preforward(self):
        return self.render_template("test.html")

TEST_VIEW_DATA = [
    ("/test_json_render", "tests.base.test_controller.TestJsonRender", "test_json_render"),
    ("/test_template_render", "tests.base.test_controller.TestTemplateRender", "test_template_render")
    ]
bootstrap.set_routing(merge_routing_modules(TEST_VIEW_DATA))

class TestController(TestBase):
    def initialize(self):
        super(TestController, self).initialize()
        app.jinja_loader = jinja2.FileSystemLoader("tests/base/template/")

    def test_json_render(self):
        with bootstrap.flask.test_request_context("/test_json_render"):
            response = self.get_response(bootstrap.flask)

            self.assertEqual(response.mimetype, "text/json")
            self.assertEqual(response.data.decode('utf-8'), json.dumps({"value" : 1}))

    def test_template_render(self):
        with bootstrap.flask.test_request_context("/test_template_render"):
            response = self.get_response(bootstrap.flask)

            self.assertEqual(response.mimetype, "text/html")
            self.assertEqual(response.data.decode('utf-8'), "")

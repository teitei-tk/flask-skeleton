# coding: utf-8
from flask import ( Blueprint, g, )

from lib.controller import BaseController
app = Blueprint("index", __name__)

class Index(BaseController):
    def preforward(self):
        return self.render_json(["Hello World"])

# coding: utf-8
from application import app

from application.c.root import index
app.register_blueprint(index.app)

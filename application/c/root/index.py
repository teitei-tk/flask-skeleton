# coding: utf-8
from flask import ( Blueprint, g, )
app = Blueprint("index", __name__)

@app.route("/")
def index():
    return "Hello world"

# coding: utf-8
from flask import Flask

app = Flask(__name__)

@app.after_request
def after_request():
    pass

@app.before_request
def before_request():
    pass

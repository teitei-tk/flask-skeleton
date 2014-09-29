# coding: utf-8

from collections import ( namedtuple, )

"""
Please add a tuple format the class you want to url management.

example: 
    stirng url
    string routing class path
    string endpoint name

    ("/", "application.c.hoge.Foo", "foo")
"""
# router class
Router = namedtuple('Router', ['url', 'import_path', 'endpoint'])

def merge_routing_modules(view_datas):
    from routes import Router
    return [Router(url=data[0], import_path=data[1], endpoint=data[2]) for data in view_datas]

VIEW_DATAS = [
    ("/", "application.c.root.index.Index", "index"),
    ]

# managements modules
ROUTING_MODULES = merge_routing_modules(VIEW_DATAS)

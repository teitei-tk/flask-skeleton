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
VIEW_DATAS = [
    ("/", "application.c.root.index.Index", "index"),
    ]

# router class
Router = namedtuple('Router', ['url', 'import_path', 'endpoint'])

# managements modules
ROUTING_MODULES = [
    Router(url=data[0], import_path=data[1], endpoint=data[2]) for data in VIEW_DATAS
    ]

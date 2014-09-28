# coding: utf-8
from collections import ( namedtuple, )

Router = namedtuple('Router', ['url', 'import_path', 'endpoint'])

VIEW_DATAS = [
    ("/", "application.c.root.index.Index", "index"),
    ]


ROUTING_MODULES = [
    Router(url=data[0], import_path=data[1], endpoint=data[2]) for data in VIEW_DATAS
    ]

# coding: utf-8
from application import bootstrap

class Migration(object):
    @classmethod
    def run(cls):
        from application.models import ( example, )
        bootstrap.db.create_tables([example.Example])

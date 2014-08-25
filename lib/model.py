# coding: utf-8
from peewee import ( Model,  )
from application import bootstrap

class BaseModelMixin(object):
    @property
    def db(self):
        return bootstrap.db

    @classmethod
    def find(cls, key, column=None):
        try:
            if not column:
                column = cls.id
            return cls.get(column == key)

        except cls.DoesNotExist:
            return None

class BaseModel(Model, BaseModelMixin):
    class Meta:
        database = bootstrap.db

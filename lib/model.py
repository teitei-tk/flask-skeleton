# coding: utf-8
from peewee import ( Model,  )
from application import bootstrap

class BaseModelMixin(object):
    @property
    def db(self):
        return bootstrap.db

    @classmethod
    def find(cls, key, column=None, offset=1, limit=10):
        try:
            if not column:
                column = cls.id

            result = [x for x in ( cls.select().where(column == key).
                        order_by(column == key).paginate(offset, limit).
                        aggregate_rows() ) ]
            next = None
            if result.__len__() == limit:
                next = offset + limit
            return result, next

        except cls.DoesNotExist:
            return [], None

        except ValueError:
            return [], None

class BaseModel(Model, BaseModelMixin):
    class Meta:
        database = bootstrap.db

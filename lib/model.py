# coding: utf-8
from peewee import ( Model,  )
from application import bootstrap

class BaseModelMixin(object):
    @property
    def db(self):
        return bootstrap.db

    @classmethod
    def get_by_column(cls, value, column=None):
        try:
            if not column:
                column = cls.id
            return cls.get(column == value)

        except cls.DoesNotExist:
            return None

        except ValueError:
            return None

    @classmethod
    def find(cls, value, column=None, offset=1, limit=10):
        try:
            if not column:
                column = cls.id

            result = [x for x in ( cls.select().where(column == value).
                        order_by(column == value).paginate(offset, limit).
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

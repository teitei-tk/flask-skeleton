# coding: utf-8
from peewee import ( Model, )
from application import bootstrap

class BaseModel(Model):
    class Meta:
        database = bootstrap.db

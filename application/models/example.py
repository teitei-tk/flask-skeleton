# coding: utf-8
from peewee import ( CharField, )
from lib.model import BaseModel

class Example(BaseModel):
    name = CharField()

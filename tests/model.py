# coding: utf-8
import unittest
from pymysql import ( connect, )
from peewee import ( CharField, )

from application import ( bootstrap, )
from lib.model import ( BaseModel, )

class TestDatabaseModel(BaseModel):
    name = CharField()

class TestModel(unittest.TestCase):
    def setUp(self):
        bootstrap.config['DATABASE_SETTING']['db_name'] = 'test_db'
        db_setting = bootstrap.config['DATABASE_SETTING']

        self.connection = connect(host=db_setting['host'], port=db_setting['port'], 
                user=db_setting['user'], passwd=db_setting['password'])

        self.initialize()

    def initialize(self):
        cursor = self.connection.cursor()
        cursor.execute("CREATE DATABASE test_db")
        cursor.close()

        bootstrap.db.connect()
        bootstrap.db.create_tables([TestDatabaseModel])

    def tearDown(self):
        bootstrap.db.drop_tables([TestDatabaseModel])
        bootstrap.db.close()

        cursor = self.connection.cursor()
        cursor.execute("DROP DATABASE test_db")
        cursor.close()
        self.connection.close()

    def test_get_by_column(self):
        # fail case
        result = TestDatabaseModel.get_by_column("test", TestDatabaseModel.name) 
        self.assertEqual(result, None)

        # success case
        TestDatabaseModel.create(name = "test")
        result = TestDatabaseModel.get_by_column("test", TestDatabaseModel.name)
        self.assertNotEqual(result, None)

    def test_find(self):
        # fail case
        result, next = TestDatabaseModel.find('test', TestDatabaseModel.name)
        self.assertFalse(result)
        self.assertFalse(next)

        # success case
        TestDatabaseModel.create(name = "test")
        result, next = TestDatabaseModel.find('test', TestDatabaseModel.name)
        self.assertNotEqual(result, [])
        self.assertEqual(next, None)

        # get next skip
        result, next = TestDatabaseModel.find('test', TestDatabaseModel.name, limit=1)
        self.assertNotEqual(result, [])
        self.assertNotEqual(next, None)

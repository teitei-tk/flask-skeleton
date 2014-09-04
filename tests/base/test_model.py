# coding: utf-8
from peewee import ( CharField, )

from tests import ( TestBase, )
from application import ( bootstrap, )
from lib.model import ( BaseModel, )

class TestDatabaseModel(BaseModel):
    name = CharField()

class TestModel(TestBase):
    def initialize(self):
        super(TestModel, self).initialize()

        bootstrap.db.connect()
        bootstrap.db.create_tables([TestDatabaseModel])

    def tearDown(self):
        bootstrap.db.drop_tables([TestDatabaseModel])
        bootstrap.db.close()

        super(TestModel, self).tearDown()

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

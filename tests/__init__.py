# coding: utf-8

import unittest
from pymysql import ( connect, )
from flask import ( request, )

from application import ( bootstrap, )
from lib.controller import ( BaseController, )
from lib.storage import ( DictStorage, )

class TestBase(unittest.TestCase):
    test_db_name = "test_db"

    def setUp(self):
        bootstrap.config['DATABASE_SETTING']['db_name'] = self.test_db_name
        db_setting = bootstrap.config['DATABASE_SETTING']

        self.connection = connect(host=db_setting['host'], port=db_setting['port'], 
                user=db_setting['user'], passwd=db_setting['password'])

        self.initialize()

    def initialize(self):
        cursor = self.connection.cursor()
        cursor.execute("CREATE DATABASE {0}".format(self.test_db_name))
        cursor.close()

    def tearDown(self):
        cursor = self.connection.cursor()
        cursor.execute("DROP DATABASE {0}".format(self.test_db_name))
        cursor.close()
        self.connection.close()


class TestBaseController(BaseController):
    dict_storage = None

    @property
    def request(self):
        return request

    @property
    def storage(self):
        if not self.dict_storage:
            self.dict_storage =  DictStorage()
        return self.dict_storage



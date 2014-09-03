# coding: utf-8

import unittest
from pymysql import ( connect, )

from application import ( bootstrap, )

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



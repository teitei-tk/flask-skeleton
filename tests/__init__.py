# coding: utf-8

import os
import unittest
from pymysql import ( connect, )
from flask import ( request, )

from application import ( bootstrap, )
from lib.controller import ( BaseController, )
from lib.storage import ( DictStorage, )

class TestBase(unittest.TestCase):
    test_db_name = "test_db"

    def setUp(self):
        self._database_setting()
        self.initialize()

    def _database_setting(self):
        config_key = 'DATABASE_SETTING'
        if os.environ.get('CI'):
            config_key = 'CI_DATABASE_SETTING'

        bootstrap.config[config_key]['db_name'] = self.test_db_name
        db_setting = bootstrap.config[config_key]

        self.connection = connect(host=db_setting['host'], port=db_setting['port'], 
                user=db_setting['user'], passwd=db_setting['password'])

    def initialize(self):
        cursor = self.connection.cursor()
        cursor.execute("CREATE DATABASE IF NOT EXISTS {0}".format(self.test_db_name))
        cursor.close()

    def tearDown(self):
        cursor = self.connection.cursor()
        cursor.execute("DROP DATABASE IF EXISTS  {0}".format(self.test_db_name))
        cursor.close()
        self.connection.close()

    def get_response(self, app):
        rv = app.preprocess_request()
        if rv != None:
            response = app.make_response(rv)
        else:
            rv = app.dispatch_request()
            response = app.make_response(rv)
            response = app.process_response(response)
        return response


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



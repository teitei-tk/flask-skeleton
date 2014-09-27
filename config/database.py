# coding: utf-8
import os

DATABASE_SETTING = dict(
    db_name  = "example",
    host     = "localhost",
    port     = 3306,
    user     = "test-user",
    password = "eWcsrLJsQq37dVJX"
    )

CI_DATABASE_SETTING = dict(
    db_name     = os.environ.get('WERCKER_MYSQL_DATABASE'),
    host        = os.environ.get('WERCKER_MYSQL_HOST'),
    port        = int(os.environ.get('WERCKER_MYSQL_PORT') or 3306),
    user        = os.environ.get('WERCKER_MYSQL_USERNAME'),
    password    = os.environ.get('WERCKER_MYSQL_PASSWORD'),
    )


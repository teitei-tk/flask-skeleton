import os

CI_DATABASE_SETTING = dict(
    db_name     = os.environ.get('WERCKER_MYSQL_DATABASE'),
    host        = os.environ.get('WERCKER_MYSQL_HOST'),
    port        = int(os.environ.get('WERCKER_MYSQL_PORT') or 0),
    user        = os.environ.get('WERCKER_MYSQL_USERNAME'),
    password    = os.environ.get('WERCKER_MYSQL_PASSWORD'),
    )


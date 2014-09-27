# coding: utf-8
import logging
from application import ( PROJECT_DIR, )

# see http://docs.python.jp/3/library/logging.html
LOG_FORMAT = '%(asctime)s - [%(levelname)s] -%(name)s %(module)s, $(filename)s,  %(lineno)s : %(message)s'
BASE_LEVEL = logging.DEBUG

LOGGING_SETTING = dict(
    file_logger = dict(
        logging_file    = "{0}/logs/logging.log".format(PROJECT_DIR.__str__()),
        logging_level   = BASE_LEVEL,
        mode            = "a",
        formatter       = LOG_FORMAT,
        ),
    console_logger = dict(
        formatter = LOG_FORMAT,
        )
    )

# coding: utf-8
import sys
import datetime
import traceback
from logging import ( getLogger, Formatter, FileHandler, )
from flask import ( g, )

from application import ( bootstrap, )

def get_logger(name=None):
    if not name:
        name = __name__
    return getLogger(name)

class Log(object):
    def __init__(self, message, code=1):
        self.message = message
        self.code    = code

    def to_string(self, now=None):
        if not now:
            now = datetime.datetime.now()
        return "{0} [{1}]:{2}".format(
                now.strftime("%Y-%m-%d %H:%m:%S"), self.code, self.message)

    def __str__(self):
        return self.to_string()

class LoggerMixin(object):
    logger          = None
    _instance       = None
    log_config_key  = None

    def __init__(self, force_logger=False):
        logger = None
        try:
            if not force_logger and g.logger:
                self.logger = logger
            else:
                self.logger = get_logger()
        except:
            self.logger = get_logger()

        logging_level = None
        config = self.get_config()
        if not "logging_level" in config:
            from config.logging import BASE_LEVEL
            logging_level = BASE_LEVEL
        else:
            logging_level = config['logging_level']

        self.logger.setLevel(logging_level)
        self.logger.addHandler(self.get_handler())

    @classmethod
    def get_config(cls):
        return bootstrap.config['LOGGING_SETTING'][cls.key()]

    @classmethod
    def get_handler(cls):
        NotImplementedError

    @classmethod
    def load(cls):
        NotImplementedError

    @classmethod
    def get(cls):
        NotImplementedError

    @classmethod
    def key(cls):
        return cls.log_config_key

    def get_stacktrace(self):
        """
        get error stack_trace
        """
        stack_trace = []
        traceback = traceback.format_exception(*sys.exc_info())
        for trace in traceback:
            for error in trace.rstrip().split('\n'):
                stack_trace += [error]
        return stack_trace

class FileLogger(LoggerMixin):
    """
    file logging
    """
    log_config_key = "file_logger"

    @classmethod
    def get_handler(cls):
        config = cls.get_config()
        handler = FileHandler(filename=config['logging_file'], mode=config['mode'])
        handler.setFormatter(Formatter(config['formatter']) )
        return handler

    @classmethod
    def get(cls):
        if not cls._instance:
            cls._instance = cls()
        return cls._instance.logger

class ConsoleLogger(LoggerMixin):
    """
    console logging
    """
    pass

# coding: utf-8
import sys
import datetime
import traceback
from logging import ( getLogger, Formatter, StreamHandler, FileHandler, )
from flask import ( g, )

from application import ( bootstrap, )

def get_logger(name=None):
    if not name:
        name = __name__
    return getLogger(name)

def get_stacktrace():
    """
    get error stack_trace
    """
    stack_trace = []
    traceback = traceback.format_exception(*sys.exc_info())
    for trace in traceback:
        for error in trace.rstrip().split('\n'):
            stack_trace += [error]
    return stack_trace

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

class BaseLogger(object):
    logger          = None
    _instance       = None
    log_config_key  = None

    def __init__(self, force_logger=False):
        logger = None
        try:
            if not force_logger and g.logger:
                self.logger = logger
            else:
                self.logger = get_logger(__name__)
        except:
            self.logger = get_logger(__name__)

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
        raise NotImplementedError()

    @classmethod
    def load(cls):
        raise NotImplementedError()

    @classmethod
    def get(cls, force_logger=False):
        if not cls._instance:
            cls._instance = cls(force_logger)
        return cls._instance.logger

    @classmethod
    def key(cls):
        return cls.log_config_key

class FileLogger(BaseLogger):
    """
    file logging
    """
    log_config_key = "file_logger"

    @classmethod
    def get_handler(cls):
        config = cls.get_config()
        handler = FileHandler(filename=config['logging_file'], mode=config.get('mode', 'a'))
        handler.setFormatter(Formatter(config['formatter']) )
        return handler

class ConsoleLogger(BaseLogger):
    """
    console logging
    """
    log_config_key = "console_logger"
    
    @classmethod
    def get_handler(cls):
        config = cls.get_config()
        handler = StreamHandler()
        handler.setFormatter(Formatter(config['formatter']))
        return handler

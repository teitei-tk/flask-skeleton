# coding: utf-8
import sys
import datetime
import traceback
from logging import ( getLogger, FileFileHandler, )
from flask import ( g, )

from application import ( bootstrap, )

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
    _instance = None
    log_config_key = None

    @classmethod
    def load(cls):
        NotImplementedError

    @classmethod
    def get(cls):
        NotImplementedError

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

    def __init__(self, config):
        pass

    @classmethod
    def load(cls):
        app_config = bootstrap.config
        cls._instance = cls(app_config['LOGGING_SETTING'][cls.log_config_key])

    @classmethod
    def get(cls):
        if not cls._instance:
            cls.load()
        return cls._instance

class ConsoleLogger(LoggerMixin):
    """
    console logging
    """
    pass

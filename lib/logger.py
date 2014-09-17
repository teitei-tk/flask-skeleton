# coding: utf-8
import datetime

class Log(object):
    def __init__(self, message, code=1):
        self.message = message
        self.code    = code

    def to_string(self, now=None):
        if not now:
            now = datetime.datetime.now()
        return "{0} [{1}]:{2}".format(
                now.strftime("%Y-%m-%d %H:%m:%S"), self.message, self.code)

    def __str__(self):
        return self.to_string()

class Logger(object):
    pass

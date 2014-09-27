# coding: utf-8
from flask import ( g, )

def random_string():
    import string
    import random
    return ''.join([random.choice(string.ascii_letters + string.digits) for i in range(50)])

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

class CsrfProtection(object):
    """
    csrf class
    """
    token_name = 'csrf_token' 

    @classmethod
    def set_csrf_token(cls):
        """
        set csrf_token at session
        """
        g.session[cls.token_name] = random_string()
        return True

    @classmethod
    def is_csrf_safe(cls):
        """
        Comparison session token and request token
        """
        return cls.get_csrf_token() == cls.get_csrf_token_by_request()

    @classmethod
    def get_csrf_token(cls):
        """
        get session token
        """
        return g.session.get(cls.token_name)

    @classmethod
    def get_csrf_token_by_request(cls):
        """
        get request token
        """
        return g.request.values.get(cls.token_name)

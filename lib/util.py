# coding: utf-8

def random_string():
    import string
    import random
    return ''.join([random.choice(string.ascii_letters + string.digits) for i in range(50)])

def secure_string():
    import hashlib
    return hashlib.sha256(random_string().encode('utf-8')).hexdigest()

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
        from flask import ( g, )
        g.session[cls.token_name] = secure_string()
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
        from flask import ( g, )
        return g.session.get(cls.token_name)

    @classmethod
    def get_csrf_token_by_request(cls):
        """
        get request token
        """
        from flask import ( g, )
        return g.request.values.get(cls.token_name)

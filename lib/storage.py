# coding: utf-8
import memcache

class BaseStorageMixin(object):
    _storage = None

    def __init__(self):
        pass

    def get(self, key):
        pass

    def set(self, key, value):
        pass

    def remove(self, key):
        pass

class DictStorage(BaseStorageMixin):
    def __init__(self):
        self._storage = dict()

    def get(self, key):
        return self._storage.get(key)

    def set(self, key, value):
        self._storage[key] = value

    def remove(self, key):
        if self.get(key):
            del self._storage[key]
            return True
        return False

class MemcacheStorage(BaseStorageMixin):
    def __init__(self, data):
        try:
            debug = 0
            if data.get('debug'):
                debug = 1

            servers = ["{0}:{1}".format(
                server.get('address'), server.get('port')) for server in data['servers']]

            self._storage = memcache.Client(servers, debug=debug)
        except:
            raise Exception("load memcache error")

    def get(self, key):
        return self._storage.get(key)

    def set(self, key, value, expire_secs=0):
        self._storage.set(key, value, expire_secs)
        return True

    def remove(self, key):
        self._storage.delete(key)
        return True


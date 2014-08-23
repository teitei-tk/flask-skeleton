# coding: utf-8

class BaseStorage(object):
    _storage = None

    def __init__(self):
        pass

    def get(self):
        pass

    def set(self):
        pass

    def remove(self):
        pass

class DictStorage(BaseStorage):
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

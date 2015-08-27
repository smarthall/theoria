from collections import namedtuple
from time import time
import cPickle as pickle
from copy import deepcopy

DEFAULT_TTL = 3600

CacheItem = namedtuple('CacheItem', ['value', 'expires'])

class MemoryCache(object):
    def __init__(self):
        self._storage = {}

    def __repr__(self):
        self.gc()
        return '<%s %s>' % (type(self).__name__, repr(self._storage))

    def __getitem__(self, key):
        item = self._storage[key]
        if item.expires > time():
            return deepcopy(item.value)
        else:
            raise KeyError("'%s' is expired" % key)

    def get(self, key, default=None):
        try:
            return deepcopy(self[key])
        except KeyError:
            return default

    def store_item(self, key, value, ttl=DEFAULT_TTL):
        item = CacheItem(value, time() + ttl)
        self._storage[key] = deepcopy(item)

    def gc(self):
        for key, item in self._storage.items():
            if item.expires < time():
                del self._storage[key]

class DiskBackedMemory(MemoryCache):
    def __init__(self, filename):
        super(DiskBackedMemory, self).__init__()

        self._filename = filename
        self.load()

    def store_item(self, *args, **kwargs):
        super(DiskBackedMemory, self).store_item(*args, **kwargs)

        self.save()

    def load(self):
        try:
            self._storage = pickle.load(open(self._filename, 'r'))
        except IOError:
            pass

    def save(self):
        self.gc()
        pickle.dump(self._storage, open(self._filename, 'w'), pickle.HIGHEST_PROTOCOL)


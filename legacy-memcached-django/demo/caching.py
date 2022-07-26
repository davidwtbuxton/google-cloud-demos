import logging

from django.core.cache.backends.memcached import BaseMemcachedCache
from google.appengine.api import memcache


logger = logging.getLogger(__name__)


class GoogleMemcachedCache(BaseMemcachedCache):
    def __init__(self, server, params):
        super().__init__(server, params, memcache, KeyError)

    def set(self, *args, **kwargs):
        # Ignore ValueError for > 1MB data.
        try:
            return super().set(*args, **kwargs)
        except ValueError as err:
            logger.error('Cache failure. %s', err)
            return False

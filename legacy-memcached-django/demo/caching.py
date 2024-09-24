# You need to enable `app_engine_apis: true` to use the built-in memcache
# service on App Engine standard.
# https://github.com/GoogleCloudPlatform/appengine-python-standard
#
# Then configure a custom cache backend.
# https://docs.djangoproject.com/en/5.1/ref/settings/#backend

import logging

from django.core.cache.backends.memcached import BaseMemcachedCache
from google.appengine.api import memcache

logger = logging.getLogger(__name__)


class GoogleMemcachedCache(BaseMemcachedCache):
    def __init__(self, server, params):
        super().__init__(server, params, memcache, KeyError)

    def set(self, key, *args, **kwargs):
        # Ignore ValueError for > 1MB data.
        try:
            return super().set(key, *args, **kwargs)
        except ValueError as err:
            logger.error("Cache failure for key %r: %s", key, err)
            return False

    def get(self, key, default=None, version=None):
        # App Engine's memcache returns None for missing keys, so you cannot
        # store None itself, and if you use the `default` argument, it gets
        # used as the `namespace` argument!
        result = super().get(key, version=version)

        if result is None:
            result = default

        return result

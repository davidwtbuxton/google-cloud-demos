DEBUG = True
ALLOWED_HOSTS = ['*']
ROOT_URLCONF = 'demo.urls'
WSGI_APPLICATION = 'demo.wsgi.application'
SECRET_KEY = 'not-secret'

# Use our custom memcache backend, which uses the legacy memcache service.
CACHES = {
    'default': {
        'BACKEND': 'demo.caching.GoogleMemcachedCache',
        'TIMEOUT': None,
    },
}

MIDDLEWARES = [
    'google.cloud.logging.handlers.middleware.RequestMiddleware',
]

from .base import *

DEBUG = True
SECRET_KEY = "secret"

EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"


try:
    from .local import *
except ImportError:
    pass

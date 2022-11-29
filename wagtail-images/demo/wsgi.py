import logging
import os

import google.cloud.logging
from django.core.wsgi import get_wsgi_application
from google.appengine.api import wrap_wsgi_app

google.cloud.logging.Client().setup_logging(log_level=logging.DEBUG)
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "demo.settings.dev")

application = wrap_wsgi_app(get_wsgi_application())

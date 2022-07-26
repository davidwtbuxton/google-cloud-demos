import logging
import os

import google.cloud.logging
from google.appengine.api import wrap_wsgi_app
from django.core.wsgi import get_wsgi_application

google.cloud.logging.Client().setup_logging(log_level=logging.DEBUG)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'demo.settings')

application = get_wsgi_application()
application = wrap_wsgi_app(application)

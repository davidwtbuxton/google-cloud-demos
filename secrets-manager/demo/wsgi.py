import logging
import os

import google.cloud.logging
from django.core.wsgi import get_wsgi_application

if os.environ.get("GAE_ENV") == "standard":
    google.cloud.logging.Client().setup_logging(log_level=logging.DEBUG)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'demo.settings')

application = get_wsgi_application()

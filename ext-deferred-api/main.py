import logging

import flask
import google.cloud.logging
from google.appengine.api import wrap_wsgi_app
from google.appengine.ext import deferred


google.cloud.logging.Client().setup_logging()
logger = logging.getLogger(__name__)

app = flask.Flask(__name__)
# The google.appengine.* APIs require this WSGI app wrapper. Passing
# `use_deferred=True` installs a task handler for /_ah/queue/deferred.
app.wsgi_app = wrap_wsgi_app(app.wsgi_app, use_deferred=True)


def do_processing(*args, **kwargs):
    """Do processing on a task queue."""
    # You cannot access flask.request in this task because the deferred API
    # request handler is not part of the Flask application instance.
    logger.info("do_processing(..) args %r kwargs %r", args, kwargs)


@app.route("/")
def home():
    task = deferred.defer(do_processing, "foo", bar="qux")
    return {"result": repr(task)}

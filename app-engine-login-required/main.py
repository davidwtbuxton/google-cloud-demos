import logging

import flask
import google.cloud.logging
from google.appengine.api import wrap_wsgi_app


google.cloud.logging.Client().setup_logging(log_level=logging.DEBUG)
app = flask.Flask(__name__)
app.config["JSONIFY_PRETTYPRINT_REGULAR"] = True


def request_headers():
    return dict(flask.request.headers)


@app.route("/admin")
def admin():
    return {'headers': request_headers()}


@app.route("/required")
def required():
    return {'headers': request_headers()}


@app.route("/")
def public():
    return {'headers': request_headers()}


app = wrap_wsgi_app(app)

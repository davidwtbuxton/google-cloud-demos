import logging

import flask
import google.cloud.logging
from google.appengine.api import wrap_wsgi_app


google.cloud.logging.Client().setup_logging(log_level=logging.DEBUG)
app = flask.Flask(__name__)
app.config["JSONIFY_PRETTYPRINT_REGULAR"] = True


@app.route("/admin")
@app.route("/required")
@app.route("/")
def public():
    return {'headers': dict(flask.request.headers)}


app = wrap_wsgi_app(app)

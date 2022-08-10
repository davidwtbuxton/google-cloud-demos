import logging
import os

import flask
import google.appengine.api
import google.cloud.logging
from google.appengine.api import mail


google.cloud.logging.Client().setup_logging(log_level=logging.DEBUG)
app = flask.Flask(__name__)


def sender_email():
    project_id = os.environ["GOOGLE_CLOUD_PROJECT"]

    return f"no-reply@{project_id}.appspotmail.com"


@app.route("/send", methods=["POST"])
def send():
    sender = sender_email()
    to = "[local]@[domain]"
    subject = "[google-cloud-demos] Hello!"
    body = "Hi, quick message sent using App Engine's mail API."
    mail.send_mail(sender=sender, to=to, subject=subject, body=body)

    return {"result": "OK"}


app = google.appengine.api.wrap_wsgi_app(app)

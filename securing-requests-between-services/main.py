import os

import flask
import google.auth.transport.requests
import requests
from google.oauth2 import id_token


app = flask.Flask(__name__)


def get_target_url():
    """Build the URL to use for a request.

    For this demo, we send a request to the same App Engine service.
    """
    url = flask.request.url_root + 'receive-signed-request'

    return url


def get_identity_token(audience):
    request = google.auth.transport.requests.Request()
    token = id_token.fetch_id_token(request, audience)

    return token


def verify_identity_token(token, audience=None):
    request = google.auth.transport.requests.Request()
    identity = id_token.verify_oauth2_token(token, request, audience=audience)

    return identity


def _authorized_request_identities():
    """DO NOT USE THIS CODE IN PRODUCTION."""
    # Don't use this code in production.
    # This demo code returns the App Engine default service account email.
    our_own_project_id = os.environ['GOOGLE_CLOUD_PROJECT']
    our_own_project_id += '@appspot.gserviceaccount.com'

    return {our_own_project_id}


@app.route('/')
def send_signed_request():
    """Send a request to an App Engine service, with signed identity token.

    This uses the metadata service to get a signed identity token for the
    default service account, with the target audience ("aud"). The token is
    added to a new request, and we show the response from the target service.
    """
    target_url = get_target_url()
    token = get_identity_token(audience=target_url)
    response = requests.get(target_url, headers={'Authorization': 'Bearer ' + token})
    response.raise_for_status()

    return response.json()


@app.route('/receive-signed-request')
def receive_signed_request():
    """Receive a request, validating the identity token (if present).

    The response shows the validated identity.
    """
    audience = flask.request.url
    auth_header = flask.request.headers.get('Authorization', '')

    if auth_header.startswith('Bearer '):
        _, _, token = auth_header.partition('Bearer ')

    try:
        identity = verify_identity_token(token, audience=audience)

        # Triple-checking things.
        if identity['iss'] != 'https://accounts.google.com':
            raise Exception('Invalid "iss" in identity token')

        # At this point the identity token looks good. Do we trust the caller?
        # You can use the email or sub fields to see who made the request.
        if identity['email'] not in _authorized_request_identities():
            raise Exception('Invalid "email" in identity token')

    except Exception as err:
        return {'error': str(err)}

    return {'identity': identity}

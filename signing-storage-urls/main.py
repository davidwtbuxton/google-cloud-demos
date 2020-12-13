import datetime
import os

import flask
import google.auth
import google.auth.compute_engine
import google.auth.transport.requests
import google.oauth2.service_account
from google.cloud import storage


app = flask.Flask(__name__)
app.config['JSON_PRETTYPRINT_REGULAR'] = True
EXPIRATION = datetime.timedelta(seconds=60)


def new_creds():
    """Create credentials that can sign blobs for a service account.

    You must have enabled the iamcredentials.googleapis.com API, and granted
    the default service account the token creator role for itself.
    """
    # Assumes we are running on App Engine.
    request = google.auth.transport.requests.Request()
    creds = google.auth.compute_engine.IDTokenCredentials(request, None)
    creds = google.oauth2.service_account.Credentials(
        creds.signer, creds.service_account_email, creds._token_uri)

    return creds


def get_bucket_name():
    """The default GCS bucket name."""
    project = os.environ['GOOGLE_CLOUD_PROJECT']

    return f'{project}.appspot.com'


@app.route('/')
def list_objects():
    """Show a list of objects in the default bucket, with signed URLs.

    Results are limited to 20 objects. The URLs are valid for 60 seconds.
    """
    creds = new_creds()
    client = storage.Client(credentials=creds)
    bucket = client.bucket(get_bucket_name())
    objects = []

    for blob in bucket.list_blobs(max_results=20):
        signed_url = blob.generate_signed_url(expiration=EXPIRATION, version='v4')
        objects.append({
            'name': blob.name,
            'signed_url': signed_url,
            'public_url': blob.public_url,
        })

    return {'objects': objects}

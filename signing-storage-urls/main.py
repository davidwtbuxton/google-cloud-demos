import datetime
import json
import os

import google.auth
import google.auth.transport.requests
from google.cloud import storage


EXPIRATION = datetime.timedelta(seconds=60)


def get_bucket_name():
    """The default GCS bucket name."""
    project = os.environ['GOOGLE_CLOUD_PROJECT']

    return f'{project}.appspot.com'


def list_objects():
    """Show a list of objects in the default bucket, with signed URLs.

    Results are limited to 20 objects. The URLs are valid for 60 seconds.
    """
    creds, _ = google.auth.default()
    # Here we fetch the service account email and a short-lived access token
    # from the metadata service. A more efficient implementation could check
    # `creds.token_state` to see if a refresh is needed.
    # https://googleapis.dev/python/google-auth/latest/reference/google.auth.credentials.html#google.auth.credentials.Credentials.token_state
    creds.refresh(google.auth.transport.requests.Request())

    client = storage.Client()
    bucket = client.bucket(get_bucket_name())
    objects = []

    for blob in bucket.list_blobs(max_results=20):
        signed_url = blob.generate_signed_url(
            expiration=EXPIRATION,
            version='v4',
            service_account_email=creds.service_account_email,
            access_token=creds.token,
        )
        objects.append({
            'name': blob.name,
            'signed_url': signed_url,
            'public_url': blob.public_url,
        })

    return {'objects': objects}


def app(environ, start_response):
    """The WSGI application entrypoint."""
    start_response('200 OK', [('content-type', 'application/json')])
    objects = list_objects()
    yield json.dumps(objects, indent=2, sort_keys=True).encode('utf-8')

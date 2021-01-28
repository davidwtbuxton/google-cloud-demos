import mimetypes
import os

import flask
from google.cloud import storage


app = flask.Flask(__name__)
PUBLIC_FOLDER = 'public/'
UNKNOWN_CONTENT_TYPE = 'application/octet-stream'


def get_storage_bucket_name():
    """Get the name for the default Cloud Storage bucket.

    Every App Engine project gets a bucket named "<project>.appspot.com".
    """
    project = os.environ['GOOGLE_CLOUD_PROJECT']
    bucket = project + '.appspot.com'

    return bucket


def choose_content_type(blob):
    content_type = blob.content_type

    if content_type == UNKNOWN_CONTENT_TYPE:
        content_type, _ = mimetypes.guess_type(blob.name, strict=False)

        if content_type == None:
            content_type = UNKNOWN_CONTENT_TYPE

    return content_type


@app.route('/')
def list_bucket():
    """List objects in the default storage bucket. Only for this demo.

    Only objects in a "public" folder are listed. Do not do this in a
    production project.
    """
    bucket_name = get_storage_bucket_name()
    client = storage.Client()
    blobs = client.list_blobs(bucket_name, prefix=PUBLIC_FOLDER, max_results=10)

    data = {'objects': []}

    for b in blobs:
        if not b.size:
            continue

        serve_url = flask.url_for('serve_object', filename=b.name, _external=True)
        data['objects'].append({
            'name': b.name,
            'content_type': b.content_type,
            'public_url': b.public_url,
            'size': b.size,
            'serve_url': serve_url,
        })

    return data


@app.route('/o/<path:filename>')
def serve_object(filename):
    """Get an object from Cloud Storage, serve it straight back.

    - Check the requested object is in the "public" folder.
    - If the object has the unknown content type, guess a better one.
    """
    if not filename.startswith(PUBLIC_FOLDER):
        flask.abort(404)

    bucket_name = get_storage_bucket_name()
    client = storage.Client()
    bucket = client.bucket(bucket_name)
    blob = bucket.get_blob(filename)

    if blob is None:
        flask.abort(404)

    content_type = choose_content_type(blob)
    response = flask.make_response(blob.download_as_bytes())
    response.headers['Content-Type'] = content_type

    return response

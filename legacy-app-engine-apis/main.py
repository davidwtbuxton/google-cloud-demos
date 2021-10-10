import functools
import mimetypes
import pathlib
import secrets

import flask
import flask_caching
from google.appengine.api import app_identity
from google.appengine.api import images
from google.appengine.api import wrap_wsgi_app
from google.cloud import storage


IMAGE_EXTENSIONS = ('.jpg', '.gif', '.png')

app = flask.Flask(__name__)
# The wrap_wsgi_app function sets up the request environ and stuff that the
# legacy App Engine APIs expect.
app.wsgi_app = wrap_wsgi_app(app.wsgi_app)
# flask_caching's memcached backend automatically uses the legacy memcache API.
cache = flask_caching.Cache(config={'CACHE_TYPE': 'MemcachedCache'})
cache.init_app(app)


@functools.cache
def get_bucket_name():
    # For a GCP project `foo`, the default bucket is `foo.appspot.com`
    return app_identity.get_default_gcs_bucket_name()


def get_uploaded_file(request, form_field='file'):
    """The uploaded file object and a random destination path in storage."""
    file = request.files[form_field]
    ext = pathlib.Path(file.filename).suffix

    if ext not in IMAGE_EXTENSIONS:
        raise ValueError

    filename = 'legacy-demo-uploads/' + secrets.token_urlsafe(8) + ext

    return file, filename


@cache.memoize(timeout=None)
def make_url_for_blob(blob):
    """The public URL for an image file in Cloud Storage."""
    # Images API works with files in cloud storage, but you need to reference
    # a file as '/gs/[bucket]/[path]'.
    filename = f'/gs/{blob.bucket.name}/{blob.name}'
    url = images.get_serving_url(None, filename=filename, secure_url=True)

    return url


@app.route('/upload', methods=['POST'])
def upload():
    """Save an image to the default bucket."""
    client = storage.Client()

    try:
        upload_file, upload_name = get_uploaded_file(flask.request)
    except ValueError:
        return {'error': f'Allowed extensions are {IMAGE_EXTENSIONS}'}, 400

    content_type, _ = mimetypes.guess_type(upload_name)
    blob = client.bucket(get_bucket_name()).blob(upload_name)
    blob.upload_from_file(upload_file, client=client, content_type=content_type)

    return {'self_link': blob.self_link}


@app.route('/')
@cache.cached(timeout=60)
def home():
    """Show public URLs for images in a private storage bucket."""
    # The response is cached using App Engine's memcache service.
    bucket = get_bucket_name()
    client = storage.Client()
    blobs = client.list_blobs(bucket, max_results=20)
    results = []

    for b in blobs:
        if pathlib.Path(b.name).suffix in IMAGE_EXTENSIONS:
            url = make_url_for_blob(b)
        else:
            url = None

        results.append({'name': b.name, 'url': url})

    return {'results': results}

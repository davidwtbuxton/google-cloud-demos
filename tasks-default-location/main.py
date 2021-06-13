"""Demo for getting the project ID and location when running on Google App
Engine or Cloud Run.

This demo shows 2 different ways to get the project ID and location.

See blog post https://buxty.com/b/2021/06/finding-the-cloud-tasks-location/
"""
import os

import flask
import google.auth.transport.requests
import googleapiclient.discovery
import googleapiclient.errors
from google.auth.compute_engine import _metadata


app = flask.Flask(__name__)
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True


APPENGINE_PREFIXES_LOCATIONS = {
    # An App Engine prefix code, e.g. "s" in "s~example", and a tasks location.
    'zde': 'asia-east1',
    'n': 'asia-east2',
    'b': 'asia-northeast1',
    'u': 'asia-northeast2',
    'v': 'asia-northeast3',
    'j': 'asia-south1',
    'zas': 'asia-southeast1',
    'zet': 'asia-southeast2',
    'f': 'australia-southeast',
    'zlm': 'europe-central2',
    'e': 'europe-west1',  # europe-west region.
    'g': 'europe-west2',
    'h': 'europe-west3',
    'o': 'europe-west6',
    'k': 'northamerica-northeast1',
    'i': 'southamerica-east1',
    's': 'us-central1',  # us-central region.
    'p': 'us-east1',
    'd': 'us-east4',
    'zuw': 'us-west1',
    'm': 'us-west2',
    'zwm': 'us-west3',
    'zwn': 'us-west4',
}


def get_project_and_location_for_tasks_from_env():
    """Determine the project ID and location from the App Engine environment.

    This will return None on Cloud Run. This will work even if the Cloud Tasks
    API is not enabled on the project.
    """
    try:
        app_id = os.environ['GAE_APPLICATION']
    except KeyError:
        return None

    prefix, _, project_id = app_id.partition('~')

    return project_id, APPENGINE_PREFIXES_LOCATIONS[prefix]


def get_project_and_location_for_tasks_from_api():
    """Determine the project ID and location from the API + metadata service.

    Works on Cloud Run and App Engine (probably Compute Engine and Cloud
    Functions too). This will fail if the Cloud Tasks API is not enabled on
    the project.
    """
    _, project_id = google.auth.default()

    name = f'projects/{project_id}'
    service = googleapiclient.discovery.build('cloudtasks', 'v2')
    request = service.projects().locations().list(name=name)
    # Fails if the Cloud Tasks API is not enabled.
    response = request.execute()

    # Grab the first location. Example location:
    # {'labels': {'cloud.googleapis.com/region': 'us-central1'},
    #  'locationId': 'us-central1',
    #  'name': 'projects/dbux-test/locations/us-central1'}
    first_location = response['locations'][0]

    return project_id, first_location['locationId']


@app.route('/')
def home():
    return {
        'location_from_api': get_project_and_location_for_tasks_from_api(),
        'location_from_env': get_project_and_location_for_tasks_from_env(),
    }

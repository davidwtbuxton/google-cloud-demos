Datastore import demo
=====================

Demo showing how to load data into the App Engine datastore. This project shows using your personal credentials to insert data directly into production.

We assume you have been granted the required roles on the project (either roles/datastore.user or a role that includes those permissions such as roles/owner or roles/editor).

Tested with Python 3.8.

Setup:

    $ pip install google-cloud-ndb

Authenticate and set application default credentials:

    $ gcloud auth login --force --update-adc

Run the script pointing to your GCP project:

    $ export GOOGLE_CLOUD_PROJECT=my-foo-project
    $ python dataimport.py monopoly.csv

More documentation:

- https://cloud.google.com/sdk/gcloud/reference/auth/application-default
- https://cloud.google.com/iam/docs/understanding-roles#datastore-roles
- https://googleapis.dev/python/python-ndb/latest/index.html
- https://googleapis.dev/python/google-auth/latest/reference/google.auth.environment_vars.html

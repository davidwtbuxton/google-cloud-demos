App Engine's legacy API demo
============================

Google's [legacy App Engine API preview moved to beta in September 2021][1], making it available for all GCP projects (previously one had to join the alpha program and get an App Engine project whitelisted).

This project demonstrates using the [images API][2] to generate a public URL for an image stored in a private Cloud Storage bucket, and using the [memcache API][3] to cache output across requests.

See the [appengine-python-standard docs][4] for more information on setup, deployment and usage of the legacy APIs.


Deployment
----------

Use `gcloud beta app deploy` to deploy the project to App Engine - the beta version is required to enable the legacy APIs.


[1]: https://cloud.google.com/appengine/docs/standard/python3/release-notes#September_27_2021
[2]: https://cloud.google.com/appengine/docs/standard/python3/reference/services/bundled/google/appengine/api/images
[3]: https://cloud.google.com/appengine/docs/standard/python3/reference/services/bundled/google/appengine/api/memcache
[4]: https://github.com/GoogleCloudPlatform/appengine-python-standard

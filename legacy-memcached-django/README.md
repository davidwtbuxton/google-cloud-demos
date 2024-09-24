# Django with App Engine's memcached service

This project demonstrates using the [built-in memcached service][2] with the [Django framework][3] on App Engine's Python 3 runtime.

The demo has a custom Django cache backend that uses `google.appengine.api.memcache`. This custom cache backend is configured as the default cache backend in the project settings.

Google's [legacy App Engine API preview moved to beta in September 2021][1], making it available for all GCP projects. See the [appengine-python-standard docs][4] for more information on setup, deployment and usage of the legacy APIs.


## Deployment

Use `gcloud app deploy` to deploy the project to App Engine.

Once deployed, visit your app and compare the "/" and "/cache" end-points.


## Differences to standard memcached

### Setting values > 1 MB

Google's memcache library [raises ValueError if the value to cache is greater than 1 MB][5]. The custom cache backend in this demo catches the exception for `cache.set(..)` calls, but not for other cache operations like add, set_multi, etc.

You probably want to ignore that exception for all cases.

### Cannot store `None` as a value

The google.appengine.api.memcache API does not support storing a `None` value, and does not support the `default` keyword argument.


[1]: https://cloud.google.com/appengine/docs/standard/python3/release-notes#September_27_2021
[2]: https://cloud.google.com/appengine/docs/standard/python3/reference/services/bundled/google/appengine/api/memcache
[3]: https://www.djangoproject.com/
[4]: https://github.com/GoogleCloudPlatform/appengine-python-standard
[5]: https://github.com/GoogleCloudPlatform/appengine-python-standard/blob/cc19a2edb1907a8b91c6fb190760ade6ae249a08/src/google/appengine/api/memcache/__init__.py#L253

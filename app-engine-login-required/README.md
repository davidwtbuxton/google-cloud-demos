Securing App Engine with login required
=======================================

You can enforce basic access control for an App Engine application using `login: required` and `login: admin` in the app.yaml.

For a Python 3.9 application, this requires the App Engine bundled services SDK.

This Flask application has 3 routes:

- No sign in required (public): `/`
- Google auth required (any user): `/required`
- Google auth required, App Engine administrators only: `/admin`

When a route requires authentication, the HTTP request header includes authentication-related headers.

- "X-Appengine-User-Email": "[email]"
- "X-Appengine-User-Id": "[user-id]"
- "X-Appengine-User-Is-Admin": "1"

If the user previously signed in, those authentication-related headers may also be present for public routes (no `login: required`).


https://cloud.google.com/appengine/docs/standard/python3/config/appref
https://github.com/GoogleCloudPlatform/appengine-python-standard

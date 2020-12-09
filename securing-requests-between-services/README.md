Securing requests between App Engine services
=============================================

App Engine's Python 3 standard runtime does not include the Google urlfetch service, which means your App Engine service cannot assert identity using the X-Appengine-Inbound-Appid header when making a request to another service.

Instead one can use add an identity token for the App Engine service account. The caller service fetches a token,  adds it as a header to a request and makes the request to the other service. The receiving service takes the identity token from the incoming request, validates it with Google's certificates, and checks the credentials in the identity (i.e. whether this caller is known to the receving service).

When running on App Engine, your code calls the metadata service to obtain a fresh identity token for the default service account.


References
----------

- https://google-auth.readthedocs.io/en/latest/reference/google.oauth2.id_token.html#google.oauth2.id_token.verify_oauth2_token
- https://cloud.google.com/compute/docs/instances/verifying-instance-identity#request_signature
- https://cloud.google.com/iap/docs/authentication-howto
-  https://cloud.google.com/iap/docs/signed-headers-howto
- https://developers.google.com/identity/sign-in/web/backend-auth#using-a-google-api-client-library

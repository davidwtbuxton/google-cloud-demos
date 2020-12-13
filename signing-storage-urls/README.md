Signed storage URLs using default credentials on App Engine
=============================================================

You can generate short-lived download URLs for Google Cloud Storage objects. This is useful if you want to allow anonymous users to download objects in a private bucket for a short time.

However on App Engine the [`blob.generate_signed_url(..)` method](https://googleapis.dev/python/storage/latest/blobs.html#google.cloud.storage.blob.Blob.generate_signed_url) does not work with the default service account credentials [returned by `google.auth.default()`](https://google-auth.readthedocs.io/en/latest/reference/google.auth.html#google.auth.default).

_Using the default App Engine credentials with  `blob.generate_signed_url(..)` results in an `AttributeError` exception and the message "you need a private key to sign credentials"._

The documentation shows how to create a credentials instance from a secret key saved in a JSON credentials file. This has [disadvantages](https://medium.com/@jryancanty/stop-downloading-google-cloud-service-account-keys-1811d44a97d9).

- It is easy to publish your project's private key by mistake for anyone to use - think adding the credentials JSON to your GitHub repository.
- The iam.disableServiceAccountKeyCreation policy may [prevent you creating credentials](https://cloud.google.com/resource-manager/docs/organization-policy/restricting-service-accounts#disable_service_account_key_creation).
- It would be nicer if you did not have to handle secrets at all.


Instead one can use the default service account without having to export credentials as JSON, by granting the service account the token creator role and constructing the appropriate credentials instance.

- Enable the iamcredentials.googleapis.com API for your project (disabled by default).
- Grant the App Engine service account token creator role (`roles/iam.serviceAccountTokenCreator`) for the service account resource itself (not granted by default).
- In your Python code, create a credentials instance that uses the [projects.serviceAccounts.signBlob API](https://cloud.google.com/iam/docs/reference/credentials/rest/v1/projects.serviceAccounts/signBlob), and use this instance for your storage API requests (see code in `main.py`).

This works, and it is good because you no longer need to create a new private key for the service account, risking that someone may steal the credentials and take over your project.

One interesting detail is that [**temporary signed URLs created using the default credentials are effectively valid for at most 12 hours**](https://cloud.google.com/storage/docs/access-control/signed-urls#signing-iam). This is a consequence of the default credentials using short-lived private keys, versus user-created keys having a 10 year lifespan (which is nuts, and emphasizes why using default credentials is a very good idea).

I need to investigate if there is a way of doing this with less code.

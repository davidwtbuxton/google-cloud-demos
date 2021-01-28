Serving files from Cloud Storage using Python
=============================================

This example shows a Python 3 App Engine standard application that serves files stored in Google Cloud Storage.

For most cases it is simpler to serve those files directly from storage by making them public, but if that is not possible then this may be a sufficient workaround.

Caveats:

- Maximum 30 megabytes per file (App Engine's response limit).
- This example does not support transparently decoding gzip-compressed objects.
- This example does not support range requests.
- Reading the file from storage then sending it as a response is inefficient.

Other approaches:

- Add a public ACL to the objects, access directly via storage.googleapis.com.
- Create short-lived signed URLs to allow public access.
- Use the deprecated Python 2.7 runtime with the blobstore API.
- Serve static assets with App Engine's static_dir and static_files handlers.

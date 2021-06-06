Reading datastore backups
=========================

This demo shows how to read Google Cloud Datastore backup files and convert the encoded entities to Python objects.

    # First pip install google-cloud-ndb google-cloud-storage google-crc32c
    import dsexport

    # Can also be a single output file, or a local directory.
    source = 'gs://example.appspot.com/path/to/backup/directory'

    for entity_key, entity_props in dsexport.find_records(source):
        print(entity_key['path])

The dsexport package can also be used directly from the command line. In this mode, entities are output as JSON lines, with the key added as the "_key" property.

    $ python -m dsexport gs://example.appspot.com/path/to/backup/directory

By default all binary values are assumed to be UTF-8 strings. You can change the behaviour with `--bytes=base64` (values are Base-64 encoded) or `--bytes=ignore` ( emits a null if bytes are not UTF-8).

This code includes files copied from the Google Cloud SDK, updated for Python 3. The heavy lifting is done by the google-cloud-ndb package. The SDK version used a pure-Python implementation for calculating checksums. This version uses the google-crc32c implementation if it is installed, falling back to the pure Python version (which is much slower).


Alternative solutions
---------------------

Instead of this, you can load datastore exports directly into BigQuery and export them from there, or write a Dataflow pipeline to export entities.

# Backups for Google Cloud Datastore consist of multiple files with entities
# in LevelDB log format.
#
# https://cloud.google.com/datastore/docs/export-import-entities
import os
import pathlib
import re
import sys

from google.cloud import storage
from google.cloud.ndb import _legacy_entity_pb as entity_pb

from . import records


# I am guessing the overall_export_metadata and export_metadata files are also
# LevelDb format, with protobuf entities. There is no public documentation,
# but one can still read all the 'output-*' files.


def key_path_as_tuples(path):
    """Convert a legacy entity key to a list of tuples."""
    result = []

    for element in path.element_list():
        value = element.id if element.has_id() else element.name
        result.append((element.type, value))

    return result


def find_gcs_files(start: str):
    """Yield open file-like objects for matching GCS objects.

    Start must be a string like 'gs://<bucket>' or 'gs://<bucket>/<prefix>'.
    Object names are like "output-*".
    """
    resource_pattern = re.compile(r'^gs://([^/]+)/?(.*)$')
    backup_file_pattern = re.compile(r'/output-\d+$')

    match = resource_pattern.search(start)

    if not match:
        raise ValueError('GCS names must start with gs://')

    bucket, prefix = match.groups()
    client = storage.Client()

    for obj in client.list_blobs(bucket, prefix=prefix):
        if backup_file_pattern.search(obj.name):
            yield obj.open('rb')


def find_local_files(start: str):
    """Yield open file object for matching filenames.

    If start is a directory, find files named "output-*", else open the start
    file directly.
    """
    p = pathlib.Path(start).resolve()

    if p.is_dir():
        for filename in p.glob('**/output-*'):
            yield open(filename, 'rb')
    else:
        yield open(p, 'rb')


def read_records(fh):
    """Yield a pair of (key, properties) for each entity read from the file.

    The file is in LevelDB format, with each record a datastore entity proto.
    String values are always bytes, with unicode in UTF-8 encoding.
    """
    for rec in records.RecordsReader(fh):
        pb = entity_pb.EntityProto()
        pb.MergePartialFromString(rec)
        key = pb.key()

        # These are _properties_, which is different to the generic entity
        # reference type where the same things are explicit methods.
        entity_key = {
            'path': key_path_as_tuples(key.path),
            'name_space': key.name_space,
            'database_id': key.database_id,
            'app': key.app,
        }

        yield entity_key, pb.entity_props()


def find_records(start: str):
    # Either a GCS path, or local file or local directory.
    finder = find_gcs_files if start.startswith('gs://') else find_local_files

    for fileobj in finder(start):
        with fileobj as fh:
            yield from read_records(fh)

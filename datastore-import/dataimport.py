# Demo of inserting data to Datastore. Tested with Python 3.8.
# See README.md for setup.
import csv
import sys

from google.cloud import ndb


class MonopolySquare(ndb.Model):
    position = ndb.IntegerProperty()
    name = ndb.StringProperty()
    group = ndb.StringProperty()


CSV_FIELDS = ['Position', 'Name', 'Group']


def insert(data):
    print('Inserting %d rows' % len(data))

    client = ndb.Client()

    with client.context():
        for row in data:
            obj = MonopolySquare(position=int(row['Position']), name=row['Name'], group=row['Group'])
            obj.put()

            print('Put entity ID %r' % obj.key.id())


def read_csv(filename):
    expected_headers = dict(zip(CSV_FIELDS, CSV_FIELDS))

    with open(filename) as fh:
        reader = csv.DictReader(fh, fieldnames=CSV_FIELDS)
        # Check the header row is correct, remove it from results.
        assert next(reader) == expected_headers
        data = list(reader)

    return data


if __name__ == '__main__':
    data = read_csv(sys.argv[1])
    insert(data)

import datetime

from google.cloud import ndb


def now():
    return datetime.datetime.now()


def next_token_id(dt: datetime.datetime = None):
    """Generate a token ID. Maximum 1 per minute.

    >>> dt = datetime.datetime(1999, 12, 31, 11, 59, 59, 12345)
    >>> next_token_id(dt)
    'token-1999-12-31-11-59-00'
    """
    if dt is None:
        dt = now()
    token = dt.strftime('token-%Y-%m-%d-%H-%M-00')

    return token


class Token(ndb.Model):
    """The token's datastore ID is the token value (making it unique)."""
    updated = ndb.DateTimeProperty(auto_now=True)
    request_id = ndb.StringProperty()
    path = ndb.StringProperty()

    def to_dict(self):
        d = super().to_dict()
        d['id'] = self.key.id()
        d['updated'] = self.updated.strftime('%c %f')

        return d


class Claim(ndb.Model):
    """A record of when each token was claimed."""
    created = ndb.DateTimeProperty(auto_now_add=True)
    token_id = ndb.StringProperty()
    request_id = ndb.StringProperty()
    path = ndb.StringProperty()

    def to_dict(self):
        d = super().to_dict()
        d['id'] = self.key.id()
        d['created'] = self.created.strftime('%c %f')

        return d

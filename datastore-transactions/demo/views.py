import uuid

import flask
from google.cloud import ndb

from .models import Token, Claim, next_token_id


app = flask.Flask(__name__)
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True


def new_request_id():
    return str(uuid.uuid4())


@app.route('/')
def home():
    """Show the recent claims and tokens.

    There should be exactly 1 Claim for each Token entity. If you see more
    Claim entities, you have a bug.
    """
    limit = 200

    with ndb.Client().context():
        tokens = Token.query(order_by=['updated']).fetch(limit)
        claims = Claim.query(order_by=['created']).fetch(limit)

        data = {
            'limit': limit,
            'tokens': [o.to_dict() for o in tokens],
            'claims': [o.to_dict() for o in claims],
        }

    return data


def get_or_insert(token_id, request_id, path):
    """If a token doesn't exist, create it and record who it was issued to.

    This function has a potential bug where 2 or more concurrent requests
    cause a token to be issued to more than one request.

    The request_id and path are here so that it is easier to see what went
    wrong later.
    """
    token_obj = Token.get_by_id(token_id)
    new_claim = False

    if token_obj is None:
        token_obj = Token(id=token_id, request_id=request_id, path=path)
        # There should be exactly one Claim entity for each Token.
        claim_obj = Claim(token_id=token_id, request_id=request_id, path=path)

        # Using put_multi here is more efficient than separate datastore puts
        # but is not required to be transaction safe.
        ndb.put_multi([token_obj, claim_obj])
        new_claim = True

    return token_obj, new_claim


@app.route('/token')
def claim_token():
    """Claim a token and record the action, not using a transaction.

    Bug: with many concurrent requests, this function causes 1 token to be
    issued to more than 1 request.
    """
    client = ndb.Client()
    path = '/token'
    request_id = new_request_id()
    token_id = next_token_id()

    with client.context():
        token_obj, new_claim = get_or_insert(token_id, request_id, path)
        token = token_obj.to_dict()

    return {'token': token, 'new_claim': new_claim}


@app.route('/token-with-tx')
def claim_token_with_tx():
    """Claim a token and record the action, using a transaction.

    Because this function uses a datastore transaction, it can handle many
    concurrent requests claiming the same token, but ensure the token is
    issued to no more than 1 request.
    """
    client = ndb.Client()
    path = '/token-with-tx'
    request_id = new_request_id()
    token_id = next_token_id()

    with client.context():
        # This uses an inner function so that we can capture the function call
        # arguments from the calling scope.
        def _inner():
            return get_or_insert(token_id, request_id, path)

        token_obj, new_claim = ndb.transaction(_inner)
        token = token_obj.to_dict()

    return {'token': token, 'new_claim': new_claim}

Using transactions on the datastore
===================================

Demo for how to use transactions to enforce constraints with the datastore.

This is an App Engine website built with Flask on the Python 3 standard runtime.

Users can request a unique token. No more than 1 token should be issued per minute.

If a token has not been issued in that minute, then it is created and the website records who it was issued to (a random ID is generated for each request), and the new token is returned.

If a token has already been issued in that minute, then the existing token is returned.


End points
---------

- GET /

    Shows the tokens and claims.

- GET /token

    Claim a token and return the token data. This has a bug and fails to guarantee a token is issued at most once when serving concurrent requests.

- GET /token-with-tx

    Claim a token and return the token data. This uses a datastore transaction to guarantee a token is issued at most once when serving concurrent requests.

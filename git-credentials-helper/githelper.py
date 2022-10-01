#!/usr/bin/env python3
"""Git credentials helper for use with Google Cloud Build or Compute Engine.

Add this script to the source code repository. Then use this in a script step
in the Cloud Build job. Node images include Python 3, so you can use this
helper like:

    steps:
    - name: node:16
        script: |
        git config --system credential.helper /workspace/githelper.py
        npm ci
"""
import json
import io
import logging
import re
import sys
import urllib.error
import urllib.request


DEFAULT_USERNAME = "git-account"
METADATA_TOKEN_URL = "http://metadata.google.internal/computeMetadata/v1/instance/service-accounts/default/token"


class Helper:
    host_patterns = [
        # Domains take from the gcloud git-helper code.
        r"\.googlesource\.com$",
        r"^source\.developers\.google\.com$",
        r"\.sourcemanager\.dev$",
        r"\.blueoryx\.dev$",
    ]
    username = DEFAULT_USERNAME

    @classmethod
    def is_valid_host(cls, details):
        """True if this git host looks like one we want to authenticate."""
        for line in io.StringIO(details):
            key, _, host = line.strip().partition('=')

            if key == "host":
                for pattern in cls.host_patterns:
                    if re.search(pattern, host):
                        return True

        return False

    @classmethod
    def make_auth(cls, token):
        """Credentials formatted for a git helper."""
        # The node:8 image ships Python 3.5, so no f-strings.
        return "username={}\npassword={}\n\n".format(cls.username, token)


def fetch_auth_token(token_url=METADATA_TOKEN_URL):
    """Get an access token from the GCE metadata service."""
    headers = {"Metadata-Flavor": "Google"}
    request = urllib.request.Request(token_url, headers=headers)
    response = urllib.request.urlopen(request)
    data = json.load(response)

    return data["access_token"]


def git_helper(operation, details, out, helper_class=Helper):
    """Write username/password credentials if this is a valid git host."""
    if operation == "get" and helper_class.is_valid_host(details):
        token = fetch_auth_token()
        auth_lines = helper_class.make_auth(token)
        out.write(auth_lines)


def main(argv, stdin, stdout):
    operation = argv[1]
    details = stdin.read()
    try:
        git_helper(operation, details, stdout)
    except urllib.error.URLError as err:
        logging.error("Failed to fetch access token: %r", err)


if __name__ == "__main__":
    main(sys.argv, sys.stdin, sys.stdout)

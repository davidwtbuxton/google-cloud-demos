"""
Extend django-environ to read environment variables stored in Google Secret
Manager.

Create a secret named "app_environ". Set the value to [env-name]=[value]
pairs, one per line.

    gcloud secrets create app_environ
    gcloud secrets versions add app_environ
"""
import collections.abc
import configparser
import os

import environ
from google.cloud import secretmanager


DEFAULT_NAME = "app_environ"
DEFAULT_VERSION = "latest"
DEFAULT_SECTION = "environ"


class SecretManagerEnviron(collections.abc.Mapping):
    """Like os.environ, but falls back to checking Google Secret Manager.

    Keys/values are read from INI-format stored in 1 Secret. The secret must
    either have a section header of `[environ]` or no header at all.
    """
    def __init__(self, project, name, version, section=DEFAULT_SECTION):
        self.project = project
        self.name = name
        self.version = version
        self.section = section
        self.client = secretmanager.SecretManagerServiceClient()

        data = get_secret(self.client, self.project, self.name, self.version)
        self.config = parse_config(data, self.section)

    def __getitem__(self, key):
        try:
            return os.environ[key]
        except KeyError:
            return self.config[key]

    def __iter__(self):
        return iter(self.config)

    def __len__(self):
        return len(self.config)


def parse_config(data, section):
    """Parse a string as INI-style config, but allow no section headers.

    Return a configparser Section.
    """
    config = configparser.RawConfigParser(default_section=section)

    try:
        config.read_string(data)
    except configparser.MissingSectionHeaderError:
        config.read_string(f"[{section}]\n" + data)

    return config[section]


def get_secret(client, project, key, version="latest"):
    """Raises google.api_core.exceptions.NotFound for a missing secret."""
    name = client.secret_version_path(project, key, version)
    response = client.access_secret_version(name=name)
    data = response.payload.data

    try:
        return data.decode("utf-8")
    except UnicodeDecodeError:
        return data


class Env(environ.Env):
    def __init__(self, project=None, name=DEFAULT_NAME, version=DEFAULT_VERSION, **kwargs):
        if project is None:
            project = os.environ["GOOGLE_CLOUD_PROJECT"]
        self.ENVIRON = SecretManagerEnviron(project, name, version)
        super().__init__(**kwargs)

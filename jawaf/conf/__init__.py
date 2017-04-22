import os
from argon2 import PasswordHasher
from collections.abc import MutableMapping
from importlib import import_module
import tzlocal
from jawaf import __dir__

class Settings(MutableMapping):
    """Wrapper class for dict in case we want to do anything fancy down the line."""

    def __init__(self, *args, **kw):
        self._storage = dict(*args, **kw)

    def __delitem__(self, key):
        del self._storage[key]

    def __getattr__(self, key):
        return self._storage[key]

    def __getitem__(self, key):
        return self._storage[key]

    def __iter__(self):
        return iter(self._storage)

    def __len__(self):
        return len(self._storage)

    def __setitem__(self, key, value):
        self._storage[key] = value

settings = Settings()

settings['DEFAULT_DATABASE_KEY'] = 'default'

# TODO: Eventually make this something one can override to support other databases.
from jawaf.adapters.db.postgresql import PostgresqlBackend
settings['DB_BACKEND'] = PostgresqlBackend()
settings['BASE_DIR'] = __dir__

settings['INSTALLED_APPS'] = []

settings['WORKERS'] = 1

settings['CSRF_FIELD_NAME'] = 'csrf_token'

settings['CSRF_HEADER_NAME'] = 'X-CSRF-TOKEN'

settings['PASSWORD_HASHER'] = PasswordHasher(hash_len=24, salt_len=16)

settings['SESSION'] = {
    'host':'localhost',
    'interface': 'redis',
    'poolsize': 10,
    'port': 6379,
}

project_settings_module_var = os.environ.get('JAWAF_SETTINGS_MODULE')
if project_settings_module_var:
    project_settings_module = import_module(project_settings_module_var)
    for project_setting in dir(project_settings_module):
        settings[project_setting] = getattr(project_settings_module, project_setting)

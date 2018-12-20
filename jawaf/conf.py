import os
from argon2 import PasswordHasher
from collections.abc import MutableMapping
# from importlib import import_module
import importlib.util
from jawaf import __dir__
from jawaf.exceptions import ConfigurationError


class Settings(MutableMapping):
    """Wrapper class for dict."""

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

# For "from conf import settings".
settings = Settings() # noqa - not directly called in this file.

settings['DEFAULT_DATABASE_KEY'] = 'default'

settings['BASE_DIR'] = __dir__

settings['INSTALLED_APPS'] = []

settings['ADMIN_CONFIG'] = {
    'database': 'default',  # Specify the database jawaf.admin uses.
}

settings['AUTH_CONFIG'] = {
    'password_reset_expiration': 3,  # Hours
    'database': 'default',  # Specify the database jawaf.auth uses.
    'login_url': '/login/',
}

settings['WORKERS'] = 1

settings['CSRF_FIELD_NAME'] = 'csrf_token'

settings['CSRF_HEADER_NAME'] = 'X-CSRF-TOKEN'

settings['PASSWORD_HASHER'] = PasswordHasher(hash_len=24, salt_len=16)

project_settings_path = os.environ.get('JAWAF_SETTINGS_PATH')
if project_settings_path:
    project_settings_spec = importlib.util.spec_from_file_location(
        f'jawaf.project.settings', project_settings_path)
    if not project_settings_spec:
        raise ConfigurationError(
            f'Error processing jawaf settings: {project_settings_path}')
    project_settings_module = importlib.util.module_from_spec(
        project_settings_spec)
    project_settings_spec.loader.exec_module(project_settings_module)
    for project_setting in dir(project_settings_module):
        settings[project_setting] = getattr(
            project_settings_module, project_setting)

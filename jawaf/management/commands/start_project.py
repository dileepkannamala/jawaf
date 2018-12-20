import os
from secrets import token_hex
from alembic import command
from alembic.config import Config
from jawaf.management.base import TemplateCommand

METADATA_CODE = '''# Use Jawaf to retrieve metadata for all installed apps.
from jawaf.conf import settings
from jawaf.db import get_metadata
target_metadata = get_metadata(settings.INSTALLED_APPS)'''

SQL_CONNECT_OVERRIDE = '''config = context.config

# Override SQL Alchemy connection string in `ini` file using
`default` db connect string.
from jawaf.db import get_engine_url
config.set_main_option('sqlalchemy.url', get_engine_url())'''


class Command(TemplateCommand):
    """Start a new jawaf project."""

    def handle(self, **options):
        options['secret_key'] = token_hex(60)
        options['template'] = 'project_template'
        base_dir, name = super(Command, self).handle(**options)
        # Setup Alembic Migrations
        alembic_dir = os.path.join(base_dir, name, 'migrations')
        cfg = Config(os.path.join(alembic_dir, 'alembic.ini'))
        command.init(config=cfg, directory=alembic_dir)
        with open(os.path.join(alembic_dir, 'env.py'), 'r') as f:
            env_py = f.read()
        env_py = env_py.replace('target_metadata = None', METADATA_CODE)
        env_py = env_py.replace('config = context.config', SQL_CONNECT_OVERRIDE)
        with open(os.path.join(alembic_dir, 'env.py'), 'w') as f:
            f.write(env_py)

from jawaf.conf import settings
from jawaf.db import create_tables
from jawaf.management.base import BaseCommand


class Command(BaseCommand):
    """Create tables in tables.py files via SQLAlchemy
    **Note** This is mainly used internally for unit tests.
    Use alembic (via the `db` command) to manage table creation and migrations.
    """

    def add_arguments(self, parser):
        parser.add_argument('--app', help='App to initialize')

    def handle(self, **options):
        if options['app']:
            apps = [options['app']]
        else:
            apps = settings.INSTALLED_APPS
        create_tables(apps, warn=True)

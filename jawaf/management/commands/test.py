import os
import pytest
from sqlalchemy_utils import database_exists, create_database
from jawaf.conf import settings
from jawaf.db import create_tables, get_engine
from jawaf.management.base import BaseCommand
from jawaf.server import Jawaf

class Command(BaseCommand):
    """Run py.test framework, set up test databases."""

    def handle(self, **options):
        """Create test databases for all db connections."""
        # Create test db
        for key in settings.DATABASES:
            test_db = settings.DATABASES[key]
            test_db['database'] = 'test_' + test_db['database']
            engine = get_engine(key)
            if not database_exists(engine.url):
                create_database(engine.url)
        create_tables(settings.INSTALLED_APPS, warn=False)
        pytest.main(options['unknown'])

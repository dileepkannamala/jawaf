import os
from subprocess import call
from jawaf.conf import settings
from jawaf.management.base import BaseCommand


class Command(BaseCommand):
    """Run py.test framework, set up test databases."""

    def handle(self, **options):
        """Convenience for running alembic commands."""
        alembic_cmd = [
            'alembic',
            '--config={}'.format(
                os.path.join(settings.BASE_DIR, 'migrations', 'alembic.ini'))]
        alembic_cmd.extend(options['unknown'])
        call(alembic_cmd)

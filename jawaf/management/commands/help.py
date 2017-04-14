import os
from jawaf.server import Jawaf
from jawaf.management import discover
from jawaf.management.base import BaseCommand
from jawaf.conf import settings

help_text = '''
Available commands:

%s

Usage:

python manage.py [command]
'''

class Command(BaseCommand):
    """Jawaf help"""

    def handle(self, **options):
        commands = [command.replace('_', '-') for command in discover().keys()]
        commands.sort()
        print(help_text % '\n'.join(commands))
        print()
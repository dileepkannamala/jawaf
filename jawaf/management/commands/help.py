from jawaf.management import discover
from jawaf.management.base import BaseCommand

help_text = '''
Available commands:

{0}

Usage:

python manage.py [command]
'''


class Command(BaseCommand):
    """Jawaf help"""

    def handle(self, **options):
        commands = [command.replace('_', '-') for command in discover().keys()]
        commands.sort()
        print(help_text.format('\n'.join(commands)))
        print()

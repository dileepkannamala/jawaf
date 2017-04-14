from secrets import token_hex
from jawaf.management.base import TemplateCommand

class Command(TemplateCommand):
    """Start a new jawaf project."""

    def handle(self, **options):
        options['secret_key'] = token_hex(60)
        options['template'] = 'project_template'
        super(Command, self).handle(**options)
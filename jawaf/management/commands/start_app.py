from jawaf.management.base import TemplateCommand

class Command(TemplateCommand):
    """Start a new app within a jawaf project."""

    def handle(self, **options):
        options['template'] = 'app_template'
        super(Command, self).handle(**options)